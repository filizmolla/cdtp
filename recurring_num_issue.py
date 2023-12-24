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


perm = permutations(repeating_indexes) 
# Print the obtained permutations 
#for i in list(perm): 
    #numbers[i[0]] = 3
    #numbers[i[1]] = 4
    #numbers[i[2]] = 6
    #numbers[i[3]] = 7
    #print (i)
    #print(numbers)

for i in list(perm): 
    if len(merged) == len(repeating_indexes):
        for j in range(len(i)):        
            numbers[i[j]] = merged[j]
    print (i)
    print(numbers)

#The closest one to the original invalid sequence is selected.

numbers = [1,5,2,4,4,5,7,9,8]
numbers2 = np.array([1, 5, 2, 4, 3, 6, 7, 9, 8])
dist = np.linalg.norm(numbers - numbers2)
print(dist)










































