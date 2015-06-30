__author__ = 'Kira'
import copy
class Kira():
    def __init__(self, thelist):
        self.thelist = thelist
    def doStuff(self):
        print("before: ", self.thelist)
        self.thelist[3] = 5
        print("after: ", self.thelist)

mylist2 = [0,0,3,0,3,0,3]
for i in range(0, 2):
    things = list(copy.copy(mylist2))
    it = Kira(things)
    print("wibble: ", mylist2)
    it.doStuff()
    print("wibbledeedo: ", things)


other = [1,2,3]
me = tuple(other)
print(me)