import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_cutting_stock(stock_dimensions, stock_pieces):
    fig, ax = plt.subplots()
    ax.set_xlim([0, stock_dimensions[0]])
    ax.set_ylim([0, stock_dimensions[1]])

    for piece_list in stock_pieces:
        for piece in piece_list:
            rect = patches.Rectangle((piece[2], piece[3]), piece[0], piece[1], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def bottom_left_fill_2d(stock_dimensions, demand_dimensions):
    demand_dimensions.sort(key=lambda x: x[0], reverse=True)  # Talep boyutlarını büyükten küçüğe sırala
    stock_pieces = []  # Kesilmiş parçaları tutacak liste

    while demand_dimensions:
        stock_piece = []  # Bir stok parçası oluştur

        for demand_dim in demand_dimensions:
            if can_fit(stock_dimensions, stock_piece, demand_dim):
                stock_piece.append((demand_dim[0], demand_dim[1], stock_dimensions[0] - sum(p[0] for p in stock_piece), max((p[1] for p in stock_piece), default=0)))

        if stock_piece:
            stock_pieces.append(stock_piece)  # Stok parçasını listeye ekle
            # Sadece bir kere çıkar
            demand_dimensions = [dim for dim in demand_dimensions if dim != stock_piece[0]]

    return stock_pieces

def can_fit(stock_dimensions, stock_piece, demand_dim):
    remaining_width = stock_dimensions[0] - sum(p[0] for p in stock_piece)
    remaining_height = stock_dimensions[1] - max((p[1] for p in stock_piece), default=0)

    return remaining_width >= demand_dim[0] and remaining_height >= demand_dim[1]

# Örnek kullanım
stock_dimensions = (10, 5)
demand_dimensions = [(4, 3), (3, 2), (2, 1), (1, 1)]

result = bottom_left_fill_2d(stock_dimensions, demand_dimensions)
print("Optimal stock pieces:", result)

# Görselleştirme
plot_cutting_stock(stock_dimensions, result)
