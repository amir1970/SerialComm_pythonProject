
import numpy as np
import operator

class DPVector(object):
    global number
    def __init__(self, *num):
        self.num = num
        self.number=num
        #print("_init_ num prt : ", self.num)

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

class DPMatrix(DPVector):
    def __init__(self,*num):
        DPVector.__init__(self,*num)

    def __repr__(self):
        return "Test()"
    def __str__(self):
        print(self.number[0].number,self.number[1].number)
        list_tmp:list=[self.number[0].number,self.number[1].number]
        str = ''.join(self.number)
        #for item in list_tmp:
       #     str = str + item
        return str#(self.number[0].number,self.number[1].number)
        #return (string)(list_tmp)
        #str1 = ""
        #str1 = ''.join(list_tmp)
        # traverse in the string
        #for ele in list_tmp:
            #str1 += ele
            #print("list=",list_tmp)
        #return str1
            #print(item)
        #loacl_list=self.number[0]
        #for i in loacl_list:
           # print(i)
        #for j in self.number[1]:
            #print(j)
        #print(self.number[0],self.number[1])
        #super(DPVector, self).
    #      return print("In Class DPMatrix",self.DPVector)
    # def __repr__(self):
    #     return 'DPMatrix_obj{}'.format(self.num)
    # def m(self):
    #     print("In Class DPMatrix",self.DPVector)
    #


a= DPVector(1,4)
b= DPVector(2,5)
c=DPMatrix(a,b)
#print("DPVector = ",a.number)
print(a+b)
print(a*b)
print(c)
#print(c.number[0].number,c.number[1].number)
#c.write()
