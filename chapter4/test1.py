from BeautifulSoup import BeautifulSoup
import re

doc = ['<html><head><title>Page title</title></head>',
       '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
       '<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
       '</html>']
soup = BeautifulSoup(''.join(doc))

print soup.contents[0].name
#print soup.contents[0].contents[0].name
print soup.contents[0]
head=soup.contents[0].contents[0]
print head.parent.name
print head.next
print head.nextSibling.contents[0].nextSibling
print len(soup('title'))
print soup.findAll('p',align="blah")

pTag=soup.html.body.p
print pTag.string
print pTag
titleTag=soup.html.head.title
print titleTag.string
print titleTag

print soup('p')[1].b.string