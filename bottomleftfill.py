import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np
import time 
import sys, logging

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
        # Benimki --> Bottom Left Heurristic 
        
        
        

        return 


class Sheet:
    def __init__(self, size):
        self.size = size
        self.pieces = []

    def fit_piece(self, piece):
        position = self.find_bottom_left_position(piece)
        if position is not None:
            piece.position = position
            self.pieces.append(piece)
            self.draw()#her parcayi ekledikten sonra yazdirdim.
            

    def find_bottom_left_position(self, piece):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.can_fit(piece, i, j):
                    return i, j
        return None

    def can_fit(self, piece, i, j):
        for existing_piece in self.pieces:
            if existing_piece.position and self.overlaps(piece, existing_piece, i, j):
                return False
        return True

    def overlaps(self, piece1, piece2, i, j):
        pos1 = piece1.position
        pos2 = piece2.position
        return not (i + piece1.width <= pos2[0] or j + piece1.height <= pos2[1] or
                    i >= pos2[0] + piece2.width or j >= pos2[1] + piece2.height)

    def get_sheet_edges_distances(self):
        right_edge_distance = 0
        top_edge_distance = 0

        for piece in self.pieces:
            if piece.position is not None:
                right_edge_distance = max(right_edge_distance, piece.position[0] + piece.width)
                top_edge_distance = max(top_edge_distance, piece.position[1] + piece.height)


        return right_edge_distance, top_edge_distance

    
    def draw(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.size[0] * 1.5)  
        ax.set_ylim(0, self.size[1] * 1.5)      
        for piece in self.pieces:
            if piece.position is not None:
                rect = patches.Rectangle(
                    (piece.position[0], piece.position[1]),  
                    piece.width,
                    piece.height,
                    linewidth=1,
                    edgecolor='r',
                    facecolor='#FFE4C4'
                    )
                ax.add_patch(rect)

        # Debugging information
        #print("Sheet size:", self.size)
        #for piece in self.pieces:
        #    print(f"Piece at position {piece.position} with size {piece.width}x{piece.height}")
        plt.title(f'{file_name}')

        plt.show()

class Piece:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = None


def blf_algorithm(sheet_size, piece_sizes):
    sheet = Sheet(sheet_size)

    for size in piece_sizes:
        piece = Piece(size[0], size[1])
        sheet.fit_piece(piece)

    return sheet

def blf_algorithm_custom_order(sheet_size, piece_sizes, order):
    sheet = Sheet(sheet_size)
    
    for piece_index in order:
        size = piece_sizes[piece_index]
        piece = Piece(size[0], size[1])
        sheet.fit_piece(piece)
    return sheet




file_name = 'C1_1'
file_path = 'original/' + file_name

try:
    with open(file_path, 'r') as file:
        piece_number = int(file.readline().strip())
        sheet_size = tuple(map(int, file.readline().split()))
        pieces = [tuple(map(int, line.split())) for line in file]

    print("piece_number =", piece_number)
    print("sheet_size =", sheet_size)
    print("pieces =", pieces)
except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")
except IOError as e:
    print(f"An error occurred while reading the file: {e}")


print(piece_number)
order = list(range(piece_number))
random.shuffle(order)
print("Shuffled numbers:", order)

#result_sheet = blf_algorithm(sheet_size, pieces)
result_sheet = blf_algorithm_custom_order(sheet_size, pieces, order)

print("Sheet:")
for piece in result_sheet.pieces:
    print(f"Piece at position {piece.position} with size {piece.width}x{piece.height}")
    

# Tüm parçalar yerleştirildikten sonra kenar uzaklıklarını al
right_edge, top_edge = result_sheet.get_sheet_edges_distances()

print(f"En sağdaki dikdörtgenin en sağ kenarı: {right_edge}")
print(f"En yukarıdaki dikdörtgenin en üst kenarı: {top_edge}")
    
    
print(f'Result set length:{len(result_sheet.pieces)}')
result_sheet.draw()

