import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://www.baidu.com")
soup = BeautifulSoup(page)
for incident in soup('div', style="display:none;"):
    print len(incident)
    print incident.prettify()
    inci =incident.contents[0]
    print inci.contents[0].strip()
    #print inci.strip()