#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 01:12:44 2023

@author: filiz
"""

import numpy as np
from itertools import permutations

def remove_duplicates(order, best_frog_order, worst_frog_order):
    print("Removing duplicates")

    numbers = np.array(order)

    unique_numbers = set()
    duplicates = []
    duplicate_indexes = {}
    missing_numbers = []

    # Traverse the array to find duplicates and unique numbers
    for index, num in enumerate(numbers):
        if num in unique_numbers:
            duplicates.append(num)
            duplicate_indexes.setdefault(num, []).append(index)
        else:
            unique_numbers.add(num)
            duplicate_indexes[num] = [index]

    # Create a reference set containing all numbers from 1 to the maximum element in the array
    reference_set = set(range(0, len(numbers)))

    # Find missing numbers by subtracting unique_numbers from reference_set
    missing_numbers = list(reference_set - unique_numbers)
    print(f"Missing Numbers: {missing_numbers}")
    print(f"Duplicates: {duplicates}")

    merged = duplicates + missing_numbers
    merged = list(set(merged))
    print(f"Merged: {merged}")

    repeating_indexes = [index for indexes in duplicate_indexes.values() if len(indexes) > 1 for index in indexes]

    perm_matrice = np.empty((0, len(numbers)))

    # Generate permutations only for repeating indexes
    perm = permutations(repeating_indexes)
    
    for i in perm:
        if len(merged) == len(repeating_indexes):
            modified_numbers = numbers.copy()
            for j in range(len(i)):
                modified_numbers[i[j]] = merged[j]

            # Check if the modified order satisfies the constraints
            if all(best_frog_order[index] <= modified_numbers[index] <= worst_frog_order[index] for index in repeating_indexes):
                perm_matrice = np.vstack([perm_matrice, modified_numbers])

    print(perm_matrice)

    min_dist = 99999
    min_index = -1
    for index, row in enumerate(perm_matrice):
        dist = np.linalg.norm(numbers - row)
        if dist < min_dist:
            min_dist = dist
            min_index = index
    new_order = perm_matrice[min_index]

    print(f"New Order: {new_order}")
    return np.array(new_order).astype(int).tolist()

# Example usage:
order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 3, 4]
best_frog_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1]
worst_frog_order = [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3]

result = remove_duplicates(order, best_frog_order, worst_frog_order)
print(f"Result: {result}")
