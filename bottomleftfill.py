import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np

class Sheet:
    def __init__(self, size):
        self.size = size
        self.pieces = []
        self.no_of_pieces = len(self.pieces)
        self.order = [0, 1, 2, 3]
        self.score = -1

    def __repr__(self):
        return f"SheetDetails (Score = {self.score}, No_of_pieces = {self.no_of_pieces})"
    
    def __str__(self):
        return f"SheetDetails (Score = {self.score}, No_of_pieces = {self.no_of_pieces})"

    def fit_piece(self, piece):
        position = self.find_bottom_left_position(piece)
        if position is not None:
            piece.position = position
            self.pieces.append(piece)
            #self.draw()  #her parcayi ekledikten sonra yazdirdim.
            

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

        #print(f"En sağdaki dikdörtgenin en sağ kenarı: {right_edge_distance}")
        #print(f"En yukarıdaki dikdörtgenin en üst kenarı: {top_edge_distance}")
        return right_edge_distance, top_edge_distance

    
    def draw(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-1, self.size[0] * 1.5)  
        ax.set_ylim(-1, self.size[1] * 1.5)      
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
            #print(f"Piece at position {piece.position} with size {piece.width}x{piece.height}")
            

        plt.title(f'{file_name}')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

class Piece:
    def __init__(self, width, height):
        self.width = width #if width < height else height       #kareleri döndürmek için kullandım
        self.height = height #if width < height else width
        self.position = None
        


class CuttingStockSolutions:
    def __init__(self):
        self.sheet_solutions: dict[int, Sheet] = {}
        self.sheet_size = (20, 20)
        self.sheet = Sheet(self.sheet_size)
        self.pieces = None
        self.no_of_pieces = 16
        self.rng = np.random.default_rng(12345)
        
    def __repr__(self):
        return f"CuttingStockSolutions (No_of_items = {self.no_of_items}, Max_bin_capacity = {self.max_bin_capacity})"
    
    def __str__(self):
        return f"CuttingStockSolutions (No_of_items = {self.no_of_items}, Max_bin_capacity = {self.max_bin_capacity})"
    
    def extract_from_file(self, file_path, file_name):
        try:
            with open(file_path, 'r') as file:
                piece_count = int(file.readline().strip())
                sheet_size = tuple(map(int, file.readline().split()))
                pieces = [tuple(map(int, line.split())) for line in file]

            #print("piece_number =", piece_count)
            #print("sheet_size =", sheet_size)
            #print("pieces =", pieces)
        except FileNotFoundError:
            print(f"The file '{file_path}' does not exist.")
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
        
        self.no_of_pieces = piece_count
        self.sheet_size = sheet_size
        self.sheet = Sheet(sheet_size)
        self.pieces = pieces
        
    def blf_algorithm(self):
        sheet_size = self.sheet_size
        piece_sizes = self.pieces
        
        sheet = Sheet(sheet_size)

        for size in piece_sizes:
            piece = Piece(size[0], size[1])
            sheet.fit_piece(piece)
        self.sheet=sheet
        print(f'Result set length:{len(sheet.pieces)}')
        sheet.draw()
        self.set_score()
        print(f'Skor={self.sheet.score}')
        
        return sheet


    def blf_algorithm_custom_order(self, order=None):
        sheet_size = self.sheet_size
        piece_sizes = self.pieces
        if order is None: 
            order = list(range(self.no_of_pieces))
            random.shuffle(order)
        print("Shuffled numbers:", order)
        sheet = Sheet(sheet_size)
        
        for piece_index in order:
            size = piece_sizes[piece_index]
            piece = Piece(size[0], size[1])
            sheet.fit_piece(piece)
            
        self.sheet = sheet
        self.sheet.order = order
        self.sheet.no_of_pieces  = len(sheet.pieces)
        
        #print(f'Result set length:{len(sheet.pieces)}')
        sheet.draw()
        self.set_score()
        print(f'Skor={self.sheet.score}')
        return sheet
    
    def set_score(self):
        # Tüm parçalar yerleştirildikten sonra kenar uzaklıklarını al
        right_edge, top_edge = self.sheet.get_sheet_edges_distances()
        print(f"En sağ: {right_edge} En yukarı: {top_edge}")
        sheet_width = self.sheet_size[0]
        sheet_height = self.sheet_size[1]
        
        
        if right_edge > sheet_width and top_edge > sheet_height :
            self.sheet.score = 0
        elif right_edge > sheet_width and top_edge <= sheet_height :
            self.sheet.score = 1
        elif top_edge > sheet_height and right_edge <= sheet_width : 
            self.sheet.score = 2
        else:
            self.sheet.score = 3
            
        self.sheet.score = 1 / top_edge


file_name = 'C1_1'
file_name = 'C0_0'
file_path = 'original/' + file_name


order=[7, 15, 8, 10, 11, 6, 5, 1, 14, 13, 3, 12, 0, 9, 2, 4]
order = [4, 0, 3, 1, 5, 2]





csp = CuttingStockSolutions()
csp.extract_from_file(file_path, file_name)
csp.blf_algorithm_custom_order(order)


#for i in range(10):
#    csp.blf_algorithm_custom_order()



    


