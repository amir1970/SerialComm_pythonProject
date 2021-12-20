import numpy as np
#
# class DPVector(object):
#
#     def __init__(self, x: int, y: int) :
#         self.first_num = x
#         self.second_num = y
#
#     def add_numbers(self):
#         result = np.add(self.first_num, self.second_num)
#         print("Adding 2 numbers = ", result)
#
#     def __add__(self, other):
#         return self+other
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
        return total#self.__class__(sum(self.num+other.num))


a= DPVector(2,5)
b= DPVector(4,7)

print(a+b)
