from itertools import permutations 
import numpy as np

numbers = np.array([1, 5, 2, 4, 4, 7, 7, 9, 8])

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
        indexes.append(index)
    else:
        unique_numbers.add(num)
        duplicate_indexes[num] = [index]

# 1'den başlayarak dizinin en büyük elemanına kadar olan tüm sayıları içeren bir referans kümesi oluştur
reference_set = set(range(1, max(numbers) + 1))

# Eksik numaraları bulmak için reference_set'ten unique_numbers'ı çıkart
missing_numbers = list(reference_set - unique_numbers)

print("Tekrar eden numaraların indexleri:", duplicate_indexes)
print("Tekrar eden numaralar:", duplicates)
print("Eksik numaralar:", missing_numbers)
merged = duplicates + missing_numbers
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






































