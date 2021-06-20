# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:18:36 2021

@author: Rocky
"""

import sympy as sp
import numpy as np

def factory(n):
    
    x = n*3
    def product(a):
        print(a, x)
        
    return product

p1 = factory(10)
p2 = factory(20)

p1(2)


order = 4

xx_sp = [sp.Symbol('x'+ str(i)) for i in range(0, order)]
print(xx_sp)

testlist = np.array([["0", "1", "2", "3"], ["4", "5", "6", "7"], ["8", "9", "10", "11"]])
testlist = testlist.transpose()
print(testlist)

#print(testlist[2][3])
#test = [testlist[i][j] for (i, j) in (range(len(testlist)), range(len(testlist[0])))]
#print([  item for item in lst for lst in testlist ])

# res = []
# for i in range(len(testlist[0])):
#     res.append([])
#     for j in range(len(testlist)):
#         res[i] = res[i] + [testlist[j][i]]
