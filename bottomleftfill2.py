import turtle

class Sheet:
    def __init__(self, size):
        self.size = size
        self.pieces = []

    def fit_piece(self, piece):
        position = self.find_bottom_left_position(piece)
        if position is not None:
            piece.position = position
            self.pieces.append(piece)

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

    def draw(self):
        turtle.clear()
        turtle.penup()
        turtle.goto(-self.size[0] // 2, self.size[1] // 2)

        for piece in self.pieces:
            if piece.position is not None:
                turtle.penup()
                turtle.goto(piece.position[0] - self.size[0] // 2, self.size[1] // 2 - piece.position[1])
                turtle.pendown()
                for _ in range(2):
                    turtle.forward(piece.width)
                    turtle.right(90)
                    turtle.forward(piece.height)
                    turtle.right(90)

        turtle.update()



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

file_path = 'original/C1_1'

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


# Set up Turtle screen coordinates
turtle.setworldcoordinates(-sheet_size[0] // 2, -sheet_size[1] // 2,
                           sheet_size[0] // 2, sheet_size[1] // 2)

result_sheet = best_fit_algorithm(sheet_size, pieces)

print("Sheet:")
for piece in result_sheet.pieces:
    print(f"Piece at position {piece.position} with size {piece.width}x{piece.height}")

result_sheet.draw()
turtle.done()
