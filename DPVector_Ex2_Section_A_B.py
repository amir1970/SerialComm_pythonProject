
import numpy as np
import operator

class DPVector(object):
    def __init__(self, *num):
        self.num = num

    def __repr__(self):
        return 'DPVector_obj{}'.format(self.num)

    def __add__(self, other):
        print("*** DEBUG ONLY ADD ***** Join list is : ", (self.num + other.num))
        total = sum(self.num + other.num)
        print("Total list sum is : ")
        return total

    def __mul__(self, other):
        print("*** DEBUG ONLY MULT ***** Join  list is : ",(self.num+other.num))
        print("*** DEBUG ONLY MULT *****  1st couple is : ",(self.num[0]),"*",(other.num[1]), "=",(self.num[0]) * (other.num[1]))
        print("*** DEBUG ONLY MULT *****  2nd couple is : ",(self.num[1]),"*",(other.num[0]), "=",(self.num[1]) * (other.num[0]))
        mul_one= ((self.num[0]) * (other.num[1])+(self.num[1]) * (other.num[0]))
        print("mul_one MULT list sum is : ")
        return mul_one


a= DPVector(1,4)
b= DPVector(2,5)

print(a+b)
print(a*b)
