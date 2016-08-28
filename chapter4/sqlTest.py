from pysqlite2 import dbapi2 as sqlite

class crawler:
  # Initialize the crawler with the name of database
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def calculatepagerank(self,iterations=20):
        # clear out the current page rank tables
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')

        # initialize every url with a page rank of 1
        for (urlid,) in self.con.execute('select rowid from urllist'):
            self.con.execute('insert into pagerank(urlid,score) values (%d,1.0)' % urlid)
            self.dbcommit()

        for i in range(iterations):
            print "Iteration %d" % (i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15

            # Loop through all the pages that link to this one
            for (linker,) in self.con.execute(
                'select distinct fromid from link where toid=%d' % urlid):
                # Get the page rank of the linker
                linkingpr=self.con.execute(
                'select score from pagerank where urlid=%d' % linker).fetchone()[0]

                # Get the total number of links from the linker
                linkingcount=self.con.execute(
                    'select count(*) from link where fromid=%d' % linker).fetchone()[0]
                pr+=0.85*(linkingpr/linkingcount)
            self.con.execute(
                'update pagerank set score=%f where urlid=%d' % (pr,urlid))
        self.dbcommit()

cr=crawler('searchindex.db')
table='wordlist'
field='word'
value='zhk999999'

a=1;
if(a!=1):
    cur=cr.con.execute(
        "select rowid from %s where %s='%s'" % (table,field,value))
    res=cur.fetchone()
    print cur
    if res==None:
        cur=cr.con.execute(
            "insert into %s (%s) values ('%s')" % (table,field,value))
        cr.dbcommit()
        print cur.lastrowid
    else:
        print res[0]

cc=crawler('nn.db')
#cc.con.execute('create table wordd(wordid primary key,score)')
cn=cc.con.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
res=cn.fetchall()
print res