import numpy as np
import sys, logging
import time

from bottomleftfill import Sheet,CuttingStockSolutions


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s: %(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SFLA:
    def __init__(self, frogs, mplx_no, no_of_iteration, no_of_mutation, q):
        self.frogs = frogs
        self.mplx_no = mplx_no
        self.FrogsEach = int(self.frogs/self.mplx_no)
        self.weights = [2*(self.FrogsEach + 1 - j)/(self.FrogsEach * (self.FrogsEach+1)) for j in range(1, self.FrogsEach+1)] 
        self.no_of_iteration = no_of_iteration
        self.no_of_mutation = no_of_mutation
        self.q = q
        #self.sheet = sheet
        self.sheet_data = CuttingStockSolutions()
        #self.bins_data = BinPackingSolutions()
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

    #Total of height of that solution.
    def find_score(self, sheet_sol: Sheet=None):
        """Find score using the formula:
            score = 1 - (sum((sum_of_weight[i]/c)^2 for each bin i)/no_of_bins)
        """
        #no_of_bins = bin_sol.no_of_bins
        #bin_sum = self.bins_data.max_bin_capacity - np.array(bin_sol.free_bin_caps)
        #score = 1 - (np.sum((bin_sum/self.bins_data.max_bin_capacity) ** k)/no_of_bins)
        #bin_sol.score = score
        width, height = sheet_sol.get_sheet_edges_distances()
        score_maybe = sheet_sol.score
        return height
        

    def generate_one_frog(self):
        sheet_sol = self.sheet_data.blf_algorithm_custom_order() 
        #self.find_score(bin_sol)
        return sheet_sol




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
    
    def new_step(self, best_frog: Sheet, worst_frog: Sheet):
        """Calculates next step
        Args:
            best_frog: best frog 
            worst_frog: worst frog
        
        Returns:
            new_frog: mutated Bin Solution
        """
        new_shift = self.rng.random() * (best_frog.rov_continous - worst_frog.rov_continous)
        new_rov_continous = worst_frog.rov_continous + new_shift
        new_frog = self.bins_data.best_fit_algorithm(new_rov_continous)
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
        print("haymk")
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
            self.bins_data.sheet_solutions.update(res[0])
            self.memeplexes[res[1]] = res[2]

    def shuffle_memeplexes(self):
        """Shuffles the memeplexes and sorting them.
        """
        logger.info("Shuffling the memeplexes and sorting them")
        temp = self.memeplexes.flatten()
        temp = np.array(sorted(temp, key = lambda x: self.bins_data.bin_solutions.get(x).score))
        for j in range(self.FrogsEach):
            for i in range(self.mplx_no):
                self.memeplexes[i, j] = temp[i + (self.mplx_no * j)]
                
    def run_sfla(self, data_path, data_name):
        logger.info("Starting SFLA algorithm")
        self.data_path = data_path
        self.sheet_data.extract_from_file(self.data_path,data_name)
        s1 = time.time()
        self.generate_init_population()
        print(self.frogs)
        
        print("OFFMK")
        self.memeplexes = self.sort_frog()
        print(self.memeplexes)
        
        
        for idx in range(self.no_of_iteration):
            logger.info(f"Local Search: {idx+1}/{self.no_of_iteration}")
            self.local_search(idx+1)
            self.shuffle_memeplexes()
        e1 = time.time()
        best_solution = self.bins_data.bin_solutions.get(self.memeplexes[0][0])
        logger.info(f"Time taken: {e1-s1}s")
        logger.info(f"Memeplexes :::\n{self.memeplexes} ::: Best Frog => {best_solution}")
        logger.info(f"Best Frog Bins => {best_solution.bins}")
        logger.info(f"Best Frog free capacities in bins => {best_solution.free_bin_caps}")
        
        with open("Result.txt", 'w') as result:
            result.write("<==== RESULTS ====>\n")
            result.write(f"Best minimum no of bins and Bin Efficiency by SFLA (Best Frog):- {best_solution}\n")
            result.write(f"<--- Best Frog Bin Solution --->\n")
            for bin_id, bin in enumerate(best_solution.bins):
                result.write(f"Bin {bin_id + 1}: {bin}\n")
            result.write(f"Free capacities in each bins: {best_solution.free_bin_caps}\n")
        
        return best_solution, (e1 - s1)

if __name__ == "__main__":
    n = 100
    # path = "./../data/bin1data/N3C2W4_T.BPP"
    # path = "./../data/bin2data/N2W1B1R7.BPP"
    # path = "./../data/bin2data/N3W1B3R0.BPP"
    # path = "./../data/bin2data/N1W1B1R5.BPP"
    file_name = 'C1_1'
    path = 'original/' + file_name

    
    sfla = SFLA(frogs=40, mplx_no=5, no_of_iteration=n, no_of_mutation=5, q=8)   # 250, 5, 5, 8 and 500, 10, 10, 16
    sfla.run_sfla(path, file_name)
    #sfla.generate_one_frog()
    
    
    
    