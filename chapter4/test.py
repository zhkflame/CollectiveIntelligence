import urllib2
from BeautifulSoup import *
from urlparse import urljoin

ignorewords=set(['the','of','to','and','a','in','is','it'])

def gettextonly(soup):
    v=soup.string
    if v==None:
      c=soup.contents
      #print c
      resulttext=''
      for t in c:
        subtext=gettextonly(t)
        resulttext+=subtext+'\n'
      return resulttext
    else:
      return v.strip()

def separatewords(text):
    splitter=re.compile('\\W*')
    res=[s.lower() for s in splitter.split(text) if s!='']
    return res

def separatewords(text):
    splitter=re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if s!='']


page='http://yuedu.163.com/ycmm/rank'
c=urllib2.urlopen(page)
contents=c.read()
#contents=c.read()
soup=BeautifulSoup(contents)
#gettextonly(soup)
v=gettextonly(soup)
links=soup('a')
print len(links)
for link in links:
    if('href' in dict(link.attrs)):
        url=urljoin(page,link['href'])
        if url.find("'")!=-1: continue
        url=url.split('#')[0]  # remove location portion
        print url
        print link
        linkText=gettextonly(link)
        print linkText
        print separatewords(linkText)
        #addlinkref(page,url,linkText)