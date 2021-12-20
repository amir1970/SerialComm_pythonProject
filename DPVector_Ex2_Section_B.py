import numpy as np

class DPVector(object):

    def __init__(self, x: int, y: int) :
        self.first_num = x
        self.second_num = y

    def add_numbers(self):
        result = np.add(self.first_num, self.second_num)
        print("Adding 2 numbers = ", result)


DPVector_obj = DPVector(4,5)
DPVector_obj.add_numbers()