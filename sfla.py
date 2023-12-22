import numpy as np
import sys, logging
import time


class SFLA:
    def __init__(self, frogs, mplx_no, no_of_iteration, no_of_mutation, q, sheet):
        self.frogs = frogs
        self.mplx_no = mplx_no
        self.FrogsEach = int(self.frogs/self.mplx_no)
        self.weights = [2*(self.FrogsEach + 1 - j)/(self.FrogsEach * (self.FrogsEach+1)) for j in range(1, self.FrogsEach+1)] 
        self.no_of_iteration = no_of_iteration
        self.no_of_mutation = no_of_mutation
        self.q = q
        self.sheet = sheet
        #self.bins_data = BinPackingSolutions()
        #self.rng = np.random.default_rng(98765)
        
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

    def find_score():
        #Computes a score for a given bin solution. Benimki --> height

        return 0
    
    def generate_one_frog(self):
        # Generates a frog using a best-fit heuristic and computes its score.
        # Benimki --> Bottom Left Heuristic 
        
        
        

        return 
    
    
    def generate_init_population(self):
        """Generation of initial population
        """
        logger.info(f"Generating initial population (Number of frogs: {self.frogs})")
                
        for frog_id in range(self.frogs):
            res_bin = self.generate_one_frog()
            self.bins_data.bin_solutions[frog_id] = res_bin

    def sort_frog(self):
        logger.info(f"Sorting the frogs and making {self.mplx_no} memeplexes with {self.frogs} frogs each")
        sorted_fitness = np.array(sorted(
            self.bins_data.bin_solutions, key=lambda x: self.bins_data.bin_solutions[x].score))
        
        memeplexes = np.empty((self.mplx_no, self.FrogsEach))
        for j in range(self.FrogsEach):
            for i in range(self.mplx_no):
                memeplexes[i, j] = sorted_fitness[i + (self.mplx_no*j)]
        return memeplexes
    
    
    
    
    