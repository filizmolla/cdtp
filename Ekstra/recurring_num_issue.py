from itertools import permutations 
import numpy as np

numbers = np.array([1, 5, 2, 4, 4, 7, 7, 9, 8])
numbers = np.array([2, 0, 2, 5, 2, 3])



unique_numbers = set()
duplicates = []
duplicate_indexes = {}
missing_numbers = []
indexes =[]

# Diziyi tarayarak tekrar eden numaraları bul ve unique_numbers kümesine ekle
for index, num in enumerate(numbers):
    if num in unique_numbers:
        duplicates.append(num)
        duplicate_indexes[num].append(index)
    else:
        unique_numbers.add(num)
        duplicate_indexes[num] = [index]


reference_set = set(range(0, len(numbers) ))
missing_numbers = list(reference_set - unique_numbers)

print("Tekrar eden numaraların indexleri:", duplicate_indexes)


for key, value in duplicate_indexes.items():
    print(f"For {key}, indexes {value}")






print("Tekrar eden numaralar:", duplicates)
print("Eksik numaralar:", missing_numbers)
merged = duplicates + missing_numbers

merged = list(set(merged))
print(merged)

repeating_indexes = [index for indexes in duplicate_indexes.values() if len(indexes) > 1 for index in indexes]
print(repeating_indexes)



perm_matrice = np.empty((0, len(numbers)))

perm = permutations(repeating_indexes) 

for i in perm:
    if len(merged) == len(repeating_indexes):
        modified_numbers = numbers.copy()
        for j in range(len(i)):
            modified_numbers[i[j]] = merged[j]
        perm_matrice = np.vstack([perm_matrice, modified_numbers])


print(perm_matrice)


#The closest one to the original invalid sequence is selected.
min_dist = 99999
min_index = -1
for index, row in enumerate(perm_matrice):
    dist = np.linalg.norm(numbers - row)
    print(dist)
    if dist < min_dist:
        min_dist = dist
        min_index = index


new_order = perm_matrice[min_index]
print(new_order)






































