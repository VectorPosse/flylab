__author__ = 'Kira'
[x,y,z] = [1,2,3]
#print (x)
import pprint
from collections import Counter
data = [[0,1,2],[0,1,2],[1,2,3]]
yes = Counter(str(e) for e in data)
#pprint.pprint(yes)
#print("\n".join("{}: {}".format(k, v) for k, v in yes.items()))

l = [""]
l2 = ["1"]
print(l[0] or l2[0])