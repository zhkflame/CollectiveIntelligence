from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def simDistance(prefs,person1,person2):
    si={}
    for item in person1:
        if item in person2:
            si[item]=1
    if(len(si)==0):
        return
    sum_of_squres=sum([pow(prefs[person1][item]-prefs[person2][item],2)
         for item in prefs[person1] if item in prefs[person2]])
    #sum_of_squres=sum([pow(prefs[person1][item]-prefs[person2][item],2)
     #                 for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sum_of_squres)

def sim_pearson(prefs,p1,p2):

    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

        # if they are no ratings in common, return 0
    if len(si)==0: return 0

    # Sum calculations
    n=len(si)

    # Sums of all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    # Sums of the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    # Sum of the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    r=num/den

    return r

def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
                  for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}

    for other in prefs:
        if other==person: continue
        sim=similarity(prefs,person,other)

        if sim<=0:continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort();
    rankings.reverse();
    return rankings


def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

def calculateSimilarItems(prefs,n=10):
    result={}
    rprefs=transformPrefs(prefs)
    count=0
    for item in rprefs:
        count+=1
        if count%100==0: print "%d / %d" % (count,len(rprefs))
        scores=topMatches(rprefs,item)
        result[item]=scores
    return result

def getRecommendedItems(prefs,itemMatch,user):
    userItems=prefs[user]
    totals={}
    simSums={}

    for (item,user_score) in userItems.items():

        for (similarRating,item2) in itemMatch[item]:
            if item2 in userItems:continue
            totals.setdefault(item2,0)
            totals[item2]+=similarRating*user_score
            simSums.setdefault(item2,0)
            simSums[item2]+=similarRating

    rankings=[(total/(simSums[item]+0.0001),item) for item,total in totals.items( )]

    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings


def loadMovieLens(path='D:/workspace/gitspace/CollectiveIntelligence/data'):
    # Get movie titles
    movies={}
    for line in open(path+'/u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title
        #print id,title

    # Load data
    prefs={}
    for line in open(path+'/u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs

if __name__=="__main__":
    #print critics['Lisa Rose'],critics['Michael Phillips']
    print critics
    print getRecommendations(critics,'Toby')
    itemMatch=calculateSimilarItems(critics)
    print itemMatch
    movies=loadMovieLens()
    print movies['87']
    itemMovies=calculateSimilarItems(movies)
    print getRecommendedItems(movies,itemMovies,'87')
