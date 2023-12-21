import turtle
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Sheet:
    def __init__(self, size):
        self.size = size
        self.pieces = []

    def fit_piece(self, piece):
        best_fit = None
        best_position = None

        for i in range(self.size[0] - piece.width + 1):
            for j in range(self.size[1] - piece.height + 1):
                if self.can_fit(piece, i, j):
                    if best_fit is None or self.calculate_waste(piece, i, j) < self.calculate_waste(piece, best_position[0], best_position[1]):
                        best_fit = (i, j)
                        best_position = (i, j)

        if best_fit is not None:
            piece.position = best_fit

        self.pieces.append(piece)

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

    def calculate_waste(self, piece, i, j):
        if piece.position is not None:
            waste_width = max(0, i + piece.width - piece.position[0] - piece.width)
            waste_height = max(0, j + piece.height - piece.position[1] - piece.height)
        else:
            waste_width = i + piece.width
            waste_height = j + piece.height

        return waste_width * waste_height
        
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


def best_fit_algorithm(sheet_size, piece_sizes):
    sheet = Sheet(sheet_size)

    for size in piece_sizes:
        piece = Piece(size[0], size[1])
        sheet.fit_piece(piece)

    return sheet


# # Example data
# sheet_size_example = (20, 20)
# piece_sizes_example = [(2, 12), (7, 12), (8, 6), (3, 6), (3, 5), (5, 5), (3, 12), (3, 7), (5, 7), (2, 6), (3, 2),
#                        (4, 2), (3, 4), (4, 4), (9, 2), (11, 2)]
#


file_name = 'C4_1'
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



result_sheet = best_fit_algorithm(sheet_size, pieces)

print("Sheet:")
for piece in result_sheet.pieces:
    print(f"Piece at position {piece.position} with size {piece.width}x{piece.height}")

result_sheet.draw()
