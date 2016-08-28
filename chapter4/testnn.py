def test(a):
    if a==1:
        return 10
    if a=='b':
        return 'hello word'

#print test(1)
#print test('b')

wordids=[101, 102,103]
createkey='_'.join(sorted([str(wi) for wi in wordids]))
a=sorted([str(wi) for wi in wordids])
print createkey
print a