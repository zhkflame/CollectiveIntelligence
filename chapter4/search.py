from pysqlite2 import dbapi2 as sqlite

class searcher:
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)
    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()

    def getmatchrows(self,q):

        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        # Split the words by spaces
        words=q.split(' ')
        tablenumber=0

        for word in words:
            # Get the word ID
            wordrow=self.con.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1

        # Create the query from the separate parts
        fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        print fullquery
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]
        print rows
        print wordids

        return rows,wordids

    def getscoredlist(self,rows,wordids):
        print len(rows)
        totalscores=dict([(row[0],0) for row in rows])
        print len(totalscores)

        # This is where we'll put our scoring functions
        weights=[(1.0,self.inboundlinkscore(rows)),
                 (1.0,self.locationscore(rows)),
                 (1.0,self.pagerankscore(rows))]
        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]

        return totalscores

    def geturlname(self,id):
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self,q):
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=[(score,url) for (url,score) in scores.items()]
        rankedscores.sort()
        rankedscores.reverse()
        for (score,urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score,self.geturlname(urlid))
        print wordids
        print rankedscores
        [r[1] for r in rankedscores[0:10]]
        return wordids,[r[1] for r in rankedscores[0:10]]

    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0: maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows:
            counts[row[0]]+=1
        return self.normalizescores(counts)

    def locationscore(self,rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]: locations[row[0]]=loc
        return self.normalizescores(locations,smallIsBetter=1)

    def inboundlinkscore(self,rows):
        uniqueurls=dict([(row[0],1) for row in rows])
        inboundcount=dict([(u,self.con.execute(
            'select count(*) from link where toid=%d' % u).fetchone()[0])
                           for u in uniqueurls])
        return self.normalizescores(inboundcount)

    def pagerankscore(self,rows):
        pageranks=dict([(row[0],self.con.execute(
            'select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        print pageranks
        maxrank=max(pageranks.values())
        normalizedscores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
        return normalizedscores

    def calculatepagerank(self,iterations=20):
        # clear out the current page rank tables
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')

        # initialize every url with a page rank of 1
        #for (urlid,) in self.con.execute('select rowid from urllist'):
        #    self.con.execute('insert into pagerank(urlid,score) values (%d,1.0)' % urlid)
        #    self.dbcommit()
        self.con.execute('insert into pagerank select rowid,1.0 from urllist')
        self.dbcommit()
        print self.con.execute('select count(*) from pagerank').fetchone()[0]

        for i in range(iterations):
            print "Iteration %d" % (i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15

                # Loop through all the pages that link to this one
                for (linker,) in self.con.execute(
                    'select distinct fromid from link where toid=%d' % urlid):
                    # Get the page rank of the linker
                    print linker
                    linkingpr=self.con.execute(
                        'select score from pagerank where urlid=%d' % linker).fetchone()[0]
                    print linkingpr
                    # Get the total number of links from the linker
                    linkingcount=self.con.execute(
                        'select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    print linkingcount
                    pr+=0.85*(linkingpr/linkingcount)
                self.con.execute(
                    'update pagerank set score=%f where urlid=%d' % (pr,urlid))
            self.dbcommit()

s=searcher('searchindex_prime.db')
res=s.query('functional programming')
#s.calculatepagerank()