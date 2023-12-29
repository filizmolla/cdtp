import numpy as np
import sys, logging
import time
from itertools import permutations 
from backtraking import Sheet, PlacementEngine
from backtraking import readData
from backtraking import backtrack
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s: %(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class CuttingStockSolutions:
    def __init__(self):
        self.sheet_solutions: dict[int, PlacementEngine(self.sheet, self.rectangles)] = {}
        self.sheet = Sheet
        self.rectangles = []
        self.placementEngine = PlacementEngine(self.sheet, self.rectangles)
        self.no_of_items = 0
        self.rng = np.random.default_rng(12345)
        
    def __repr__(self):
        return f"CuttingStockSolutions (No_of_items = {self.no_of_items}, Sheet Width = {self.sheet.width}, Sheet Height = {self.sheet.height})"
    
    def __str__(self):
        return f"CuttingStockSolutions (No_of_items = {self.no_of_items}, Sheet Width= {self.sheet.width}, Sheet Height = {self.sheet.height})"
    
    def extract_from_file(self, file_path, file_name):
        with open(file_path, 'r') as file:
            data = ' \n'.join(line.strip() for line in file)
        self.sheet, self.rectangles = readData(data)
        self.no_of_items = len(self.rectangles)
        #print(self.rectangles)
        #print(self.sheet)
        return data
    
    def backtrack_algortihm(self):
        engine = PlacementEngine(self.sheet, self.rectangles)
        self.placementEngine = engine
        result = self.placementEngine.backtrack(engine, list(map(lambda x: x.id, self.rectangles)))
        self.placementEngine.draw()
        print(engine.placements.keys())
        return result
        
    
    def backtrack_algorithm_custom_order(self, order=None):
        pass

    
    

class SFLA:
    def __init__(self, frogs, mplx_no, no_of_iteration, no_of_mutation, q):
        self.frogs = frogs
        self.mplx_no = mplx_no
        self.FrogsEach = int(self.frogs/self.mplx_no)
        self.weights = [2*(self.FrogsEach + 1 - j)/(self.FrogsEach * (self.FrogsEach+1)) for j in range(1, self.FrogsEach+1)] 
        self.no_of_iteration = no_of_iteration
        self.no_of_mutation = no_of_mutation
        self.q = q
        self.sheet_data = CuttingStockSolutions()
        self.rng = np.random.default_rng(98765)

        
    def __repr__(self):
        return f"SFLA (Frogs = {self.frogs}, Memeplexes = {self.mplx_no})"
    
    def __str__(self):
        return f"SFLA (Frogs = {self.frogs}, Memeplexes = {self.mplx_no})"
    
    @property
    def memeplexes(self) -> np.ndarray:
        return self._memeplexes
    
    @memeplexes.setter
    def memeplexes(self, memeplexes: np.ndarray):
        self._memeplexes = memeplexes 

    def find_score(self, sheet_sol: PlacementEngine=None):
        """Find score using the formula: Get the missing pieces and calculate their score.
        """
        score = sheet_sol.score()
        return score
        
    
    def generate_one_frog(self):
        random.shuffle(self.sheet_data.rectangles)
        engine = PlacementEngine(self.sheet_data.sheet, self.sheet_data.rectangles)
        result = backtrack(engine, list(map(lambda x: x.id, self.sheet_data.rectangles)))
        score = self.find_score(engine)
        return engine




    def generate_init_population(self):
        """Generation of initial population
        """
        logger.info(f"Generating initial population (Number of frogs: {self.frogs})")
                
        for frog_id in range(self.frogs):
            res_sheet = self.generate_one_frog()
            self.sheet_data.sheet_solutions[frog_id] = res_sheet

    def sort_frog(self):
        logger.info(f"Sorting the frogs and making {self.mplx_no} memeplexes with {self.frogs} frogs each")
        sorted_fitness = np.array(sorted(
            self.sheet_data.sheet_solutions, key=lambda x: self.sheet_data.sheet_solutions[x].score))
        
        memeplexes = np.empty((self.mplx_no, self.FrogsEach))
        for j in range(self.FrogsEach):
            for i in range(self.mplx_no):
                memeplexes[i, j] = sorted_fitness[i + (self.mplx_no*j)]
        return memeplexes
    
    
    def is_within_constraints(self, value, constraint):
        lower_limit, upper_limit = min(constraint), max(constraint)
        return lower_limit <= value <= upper_limit

    def permutations_with_constraints(self, lst, constraints):
        if not lst or len(lst) != len(constraints):
            return []

        valid_permutations = []
        
        i = 0 
        for perm in permutations(lst):
            #if i >= 10000:
               # break
            valid = all(self.is_within_constraints(float(perm[i]), constraints[i]) for i in range(len(perm)))
            if valid:
                valid_permutations.append(list(perm))
            i +=1
        
        print(i)
        return valid_permutations
    
    def has_duplicates(self, arr):
        seen = set()
        for elem in arr:
            if elem in seen:
                return True
            seen.add(elem)
        return False

    def normalize_numbers_to_range_int(self, numbers, new_min, new_max):
        # Find the minimum and maximum values in the array
        min_value = min(numbers)
        max_value = max(numbers)
        
        # Calculate the range of values
        value_range = max_value - min_value
        
        # Normalize each number to the new range and round to the nearest integer
        normalized_numbers = [round((num - min_value) / value_range * (new_max - new_min) + new_min) for num in numbers]
        
        return normalized_numbers
    
    def remove_duplicates(self, order, best_frog_order, worst_frog_order):
        print("removing duplicates")
        numbers = np.array(order)

        unique_numbers = set()
        duplicates = []
        duplicate_indexes = {}
        missing_numbers = []
        indexes =[]
        comparison_info = []


        # Diziyi tarayarak tekrar eden numaraları bul ve unique_numbers kümesine ekle
        for index, num in enumerate(numbers):
            if num in unique_numbers:
                duplicates.append(num)
                duplicate_indexes.setdefault(num, []).append(index)
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
        
        merged = list(set(merged))
        print(merged)
        repeating_indexes = [index for indexes in duplicate_indexes.values() if len(indexes) > 1 for index in indexes]
        
        perm_matrice = np.empty((0, len(numbers)))

        #print(f"REPEATING INDICES {repeating_indexes}")
        #CHECK OTHER LISTS 
        constraints = {}

        for index in repeating_indexes:
            constraints[index] = (best_frog_order[index], worst_frog_order[index])

        print("Comparison Info:", [f"{key}: {value}" for key, value in constraints.items()])
        
        valid_combinations = []

        perms = self.permutations_with_constraints(merged, list(constraints.values())) 
        #if len(perms) == 0:
            #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            #return worst_frog_order

        for perm in perms:
            if len(merged) == len(repeating_indexes):
                modified_numbers = numbers.copy()
                for j in range(len(perm)):
                    #print(modified_numbers, repeating_indexes, j, perm)
                    modified_numbers[repeating_indexes[j]]= perm[j]
                perm_matrice = np.vstack([perm_matrice, modified_numbers])
        
        print(perm_matrice)
        
        min_dist = 99999
        min_index = -1
        for index, row in enumerate(perm_matrice):
            dist = np.linalg.norm(numbers - row)
            #print(dist)
            if dist < min_dist:
                min_dist = dist
                min_index = index
        if min_index == -1:
             print("")   
        new_order = perm_matrice[min_index]
        
        
        print(new_order)
        return np.array(new_order).astype(int).tolist()
    
    def new_step(self, best_frog: Sheet, worst_frog: Sheet):
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

    
        subtraction = [a - b for a, b in zip(best_frog_order, worst_frog_order)]
        print(f"Subtracting two orders:{subtraction}")
    
        random_multiplier = self.rng.random()
        print(f'Random={random_multiplier}')
        new_shift =[abs(number * random_multiplier)for number in subtraction] 
        new_shift = [eleman if eleman < Smax else Smax for eleman in new_shift]
    
        new_order = [a + b for a, b in zip(new_shift, worst_frog_order)]
        new_order = [round(number) for number in new_order]
        new_order = self.normalize_numbers_to_range_int(new_order, 0, len(new_order) - 1)
        
        print(f"Pwnew {new_order}")
        
        
        
        result = self.has_duplicates(new_order)
        if result:
            #new_order = self.normalize_numbers_to_range_int(new_order, 0, len(new_order) - 1)
            print(f"Normalized:{new_order}")
            new_order = self.remove_duplicates(new_order, best_frog_order, worst_frog_order)
    
        print(len(new_order))
        if len(new_order) in new_order:
            new_order = [x - 1 if x != 0 else x for x in new_order]
            print(new_order)

        new_frog = self.sheet_data.blf_algorithm_custom_order(new_order)
    
        return new_frog



    def local_search_one_memeplex(self, ls_args):
        """
        Burada sıralamalarını değiştirmesi ve skorlarını ona göre karşılaştırması lazım.

        Args:
            im: current memeplex index
            iter_idx: current iteration index
        
        Returns:
            extracted_bin_sols: modified bin solutions
            im: current memeplex index
            memeplex: modified memeplex
        """
        im, iter_idx = ls_args
        memeplex = self.memeplexes[im]
        extracted_bin_sols = {int(item):self.sheet_data.sheet_solutions.get(item) for item in memeplex}
        print("aaaaaa")
        print(extracted_bin_sols)
        # Assuming extracted_bin_sols is a dictionary
        for key, value in extracted_bin_sols.items():
            print(f"Bin ID: {key}, Bin Solution: {value}")
        for bin_id, sheet_details in extracted_bin_sols.items():
            print(f"Bin ID: {bin_id}, Score: {sheet_details.score}, No_of_pieces: {sheet_details.no_of_pieces}")


        for idx in range(self.no_of_mutation):
            logger.info(f"Iteration {iter_idx} -- Local Search of Memeplex {im + 1}: Mutation {idx + 1}/{self.no_of_mutation}")
            rValue = self.rng.random(self.FrogsEach) * self.weights
            subindex = np.sort(np.argsort(rValue)[::-1][0:self.q])
            submemeplex = memeplex[subindex] 

            Pb = extracted_bin_sols[int(submemeplex[0])]
            Pw = extracted_bin_sols[int(submemeplex[self.q - 1])]
            
            globStep = False
            censorship = False
            
            logger.info(f"Iteration {iter_idx} -- Memeplex {im + 1}: Learn from local best Pb")
            new_frog = self.new_step(Pb, Pw)
            self.find_score(new_frog)
            if new_frog.score > Pw.score:
                globStep = True     
            
            if globStep:
                logger.info(
                    f"Iteration {iter_idx} -- Memeplex {im + 1}: Score didn't improve... Learn from global best Pb")
                new_frog = self.new_step(self.frog_gb, Pw)
                self.find_score(new_frog)
                if new_frog.score > Pw.score:
                    censorship = True

            if censorship:
                logger.info(f"Iteration {iter_idx} -- Memeplex {im + 1}: Still score didn't improve... generating a new frog")
                new_frog = self.generate_one_frog()

            extracted_bin_sols[int(submemeplex[self.q-1])] = new_frog
            memeplex = np.array(sorted(extracted_bin_sols, key = lambda x: extracted_bin_sols[x].score))
            logger.info(f"Iteration {iter_idx} -- Local Search of Memeplex {im + 1}: Bin Solution moved to Bin_ID -> {int(submemeplex[self.q-1])} ::: {new_frog} ::: Mutation {idx + 1}/{self.no_of_mutation} finished!!")
        
        return (extracted_bin_sols, im, memeplex)

    def local_search(self, iter_idx):
        """Local Search
        Args:
            iter_idx: current iteration index
        """
        self.frog_gb = self.sheet_data.sheet_solutions.get(int(self.memeplexes[0][0]))
        for frog_id in range(self.mplx_no):
            res = self.local_search_one_memeplex([frog_id, iter_idx])
            self.sheet_data.sheet_solutions.update(res[0])
            self.memeplexes[res[1]] = res[2]

    def shuffle_memeplexes(self):
        """Shuffles the memeplexes and sorting them.
        """
        logger.info("Shuffling the memeplexes and sorting them")
        temp = self.memeplexes.flatten()
        temp = np.array(sorted(temp, key = lambda x: self.sheet_data.sheet_solutions.get(x).score))
        for j in range(self.FrogsEach):
            for i in range(self.mplx_no):
                self.memeplexes[i, j] = temp[i + (self.mplx_no * j)]
                
    def run_sfla(self, data_path, data_name):
        logger.info("Starting SFLA algorithm")
        self.data_path = data_path
        self.sheet_data.extract_from_file(self.data_path, data_name)
        print(self.sheet_data)
        
        
        s1 = time.time()
        self.generate_init_population()
        print(self.frogs)
        self.memeplexes = self.sort_frog()
        print(self.memeplexes)
        
        
        for idx in range(self.no_of_iteration):
            logger.info(f"Local Search: {idx+1}/{self.no_of_iteration}")
            self.local_search(idx+1)
            self.shuffle_memeplexes()
        e1 = time.time()
        best_solution = self.sheet_data.sheet_solutions.get(self.memeplexes[-1][-1])
        logger.info(f"Time taken: {e1-s1}s")
        logger.info(f"Memeplexes :::\n{self.memeplexes} ::: Best Frog => {best_solution}")
        logger.info(f"Best Frog Order => {best_solution.order}")
        logger.info(f"Best Frog Score => {best_solution.score}")
        
        # with open("Result.txt", 'w') as result:
        #     result.write("<==== RESULTS ====>\n")
        #     result.write(f"Best minimum no of bins and Bin Efficiency by SFLA (Best Frog):- {best_solution}\n")
        #     result.write(f"<--- Best Frog Bin Solution --->\n")
        #     result.write(f"Best Frog Order for {data_name} is: {best_solution.order}\n")
        #     #for bin_id, bin in enumerate(best_solution.bins):
        #     #    result.write(f"Bin {bin_id + 1}: {bin}\n")
        #     #result.write(f"Free capacities in each bins: {best_solution.free_bin_caps}\n")
        
        # return best_solution, (e1 - s1)

if __name__ == "__main__":
    n = 10
    file_name = 'C1_1'
    path = 'original/' + file_name

    
    sfla = SFLA(frogs=40, mplx_no=5, no_of_iteration=n, no_of_mutation=5, q=8)   # 250, 5, 5, 8 and 500, 10, 10, 16
    sfla.run_sfla(path, file_name)
    #sfla.generate_one_frog()
    
    
    
    
