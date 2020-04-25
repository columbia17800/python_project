from struct import *
from ast import literal_eval

c = ("123", 90)

b = str(c)

c2 = literal_eval(b)

print(b)
print(c2[0])