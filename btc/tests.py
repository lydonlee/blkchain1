from django.test import TestCase
li = ['aa','bb','cc']
# Create your tests here.
def testlist(l=[]):
    print(l)
    l[0]='dd'
    return

print(li)