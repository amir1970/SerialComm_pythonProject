
import numpy as np
import operator

class DPVector(object):
    def __init__(self, *num):
        self.num = num

    def __repr__(self):
        return 'DPVector_obj{}'.format(self.num)

    def __add__(self, other):
        print("Join list is : ",(self.num+other.num))
        total = sum(self.num+other.num)
        print("Total list sum is : ")
        return total


a= DPVector(1,4)
b= DPVector(2,5)

print(a+b)
