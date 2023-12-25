from bottomleftfill import Sheet, CuttingStockSolutions
import random
import numpy as np
from itertools import permutations 

rng = np.random.default_rng(9876)
def has_duplicates(arr):
    seen = set()
    for elem in arr:
        if elem in seen:
            return True
        seen.add(elem)
    return False


def remove_duplicates(order):
    print("removing duplicates")
    numbers = np.array(order)

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

    # 1'den başlayarak dizinin en büyük elemanına kadar olan tüm sayıları içeren bir referans kümesi oluştur
    reference_set = set(range(0, len(numbers)))
    
    # Eksik numaraları bulmak için reference_set'ten unique_numbers'ı çıkart
    missing_numbers = list(reference_set - unique_numbers)
    print(f"Missing Numbers:{missing_numbers}")
    print(f"Duplicates:{duplicates}")
    
    
    merged = duplicates + missing_numbers
    print(merged)
    repeating_indexes = [index for indexes in duplicate_indexes.values() if len(indexes) > 1 for index in indexes]
    
    perm_matrice = np.empty((0, len(numbers)))

    perm = permutations(repeating_indexes) 

    for i in perm:
        if len(merged) == len(repeating_indexes):
            modified_numbers = numbers.copy()
            for j in range(len(i)):
                modified_numbers[i[j]] = merged[j]
            perm_matrice = np.vstack([perm_matrice, modified_numbers])
    
    print(perm_matrice)
    
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
    return np.array(new_order).astype(int).tolist()
        
        

def new_step(best_frog: Sheet, worst_frog: Sheet):
    """Calculates next step
        Args:
            best_frog: best frog 
            worst_frog: worst frog
        
        Returns:
            new_frog: mutated Bin Solution
    """
    
    
    Smax = 4
    best_frog_order = best_frog.order
    worst_frog_order = worst_frog.order
    
    #best_frog_order =[4, 5, 3, 2, 8, 1, 6, 7, 9]
    #worst_frog_order = [1, 5 ,2, 4, 3, 6, 7, 9, 8] 
    
    subtraction = [a - b for a, b in zip(best_frog_order, worst_frog_order)]
    print("Subtracting two orders:")
    print(subtraction)
    
    random_multiplier = 0.11#rng.random()
    print(f'Random={random_multiplier}')
    new_shift =[abs(number * random_multiplier)for number in subtraction] 
    new_shift = [eleman if eleman < Smax else Smax for eleman in new_shift]
    
    
    print(new_shift)
    
    
    new_order = [a + b for a, b in zip(new_shift, worst_frog_order)]
    
    print(new_order)
    new_order = [round(number) for number in new_order]
    
   
    print(new_order)
    result = has_duplicates(new_order)
    if result:    
        new_order = remove_duplicates(new_order)
    
    
    print(len(new_order))
    if len(new_order) in new_order:
        new_order = [x - 1 if x != 0 else x for x in new_order]
        print(new_order)

    new_frog = csp.blf_algorithm_custom_order(new_order)
    
    return new_frog



file_name = 'C0_0'
file_path = 'original/' + file_name
csp = CuttingStockSolutions()
csp.extract_from_file(file_path, file_name)


sheet1 = csp.blf_algorithm_custom_order()
sheet2 = csp.blf_algorithm_custom_order()


new_step(sheet1, sheet2)