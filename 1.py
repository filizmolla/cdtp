import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


def draw_rectangle(uzunluk, genislik, x, y):
    fig, ax = plt.subplots()

    dikdortgen = patches.Rectangle((x, y), uzunluk, genislik, linewidth=1, edgecolor='r', facecolor='none')

    ax.add_patch(dikdortgen)

    ax.set_xlim(x-1, x+uzunluk+1)
    ax.set_ylim(y-1, y+genislik+1)


    plt.title('Dikdörtgen Çizimi')

    plt.show()

def draw_rectangle_list(rect_list):
    # Figure ve Axes oluştur
    fig, ax = plt.subplots()

    # Her dikdörtgen için
    for dikdortgen in rect_list:
        height, width, x, y = dikdortgen
        
        rect_obj = patches.Rectangle((x, y), height, width, linewidth=0.5, edgecolor='black', facecolor='#9BCD9B')

        ax.add_patch(rect_obj)

    ax.set_xlim(min([x for _, _, x, _ in rect_list]) - 1, max([x + uzunluk for uzunluk, _, x, _ in rect_list]) + 1)
    ax.set_ylim(min([y for _, _, _, y in rect_list]) - 1, max([y + genislik for _, genislik, _, y in rect_list]) + 1)


    plt.title('Dikdörtgenler Çizimi')

    plt.show()

def bottom_left_fill():
    return
    


sheet_size_example = (20, 20)
piece_sizes_example = [(2, 12), (7, 12), (8, 6), (3, 6), (3, 5), (5, 5), (3, 12), (3, 7), (5, 7), (2, 6), (3, 2),
                        (4, 2), (3, 4), (4, 4), (9, 2), (11, 2)]



rect_list = [(5, 3, 2, 4), (4, 2, 8, 6), (6, 4, 12, 2)]
draw_rectangle_list(rect_list)
