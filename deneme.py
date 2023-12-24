from bottomleftfill import Sheet, CuttingStockSolutions
import random
import numpy as np

rng = np.random.default_rng(9876)


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
    
    best_frog_order =[4, 5, 3, 2, 8, 1, 6, 7, 9]
    worst_frog_order = [1, 5 ,2, 4, 3, 6, 7, 9, 8] 
    
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
    
    print(len(new_order))
    counter = [0] * (len(new_order) +1)
    print(counter)
    for number in new_order:
        counter[number] +=1 
    print(counter)
    
    
    print(new_order)
    

    new_frog = csp.blf_algorithm_custom_order(new_order)
    
    return new_frog



file_name = 'C1_1'
file_path = 'original/' + file_name
csp = CuttingStockSolutions()
csp.extract_from_file(file_path, file_name)


sheet1 = csp.blf_algorithm_custom_order()
sheet2 = csp.blf_algorithm_custom_order()


new_step(sheet1, sheet2)