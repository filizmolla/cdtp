#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 20:56:26 2023

@author: filiz
"""

def list_permutations(elements):
    if len(elements) <= 1:
        yield elements
    else:
        for p in list_permutations(elements[1:]):
            for i in range(len(elements)):
                yield p[:i] + elements[0:1] + p[i:]

# Accept input from the user
# nums = [1,2] 
# nums = [1,2,3]
nums = [2,4,3,7,11,16,13,9]
print("Original list of elements:",nums)

# Generate and print all permutations
print("All permutations:")
permutatîons = list_permutations(nums)
    
from timeit import default_timer as timer

start = timer()
for p in permutatîons:
    print(p)
    p2 = p.copy()
    pass
end = timer()

print(end - start) # Time in seconds, e.g. 5.38091952400282
