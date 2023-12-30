import os
from rectpack import newPacker
import matplotlib.pyplot as plt
from pygcode import GCode
import random
import time  # Eklenen kısım




def plot_solution(packed_rectangles, bin_width, bin_height, size, save_path=None):
    plt.figure()
    ax = plt.gca()

    for rect in packed_rectangles:
        x, y, w, h = rect[1], rect[2], rect[3], rect[4]
        rect = plt.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='w')
        ax.add_patch(rect)

    plt.xlim(0, bin_width)
    plt.ylim(0, bin_height)
    plt.gca().set_aspect('equal', adjustable='box')

    # Turn off axis numbering (ticks)
    ax.set_xticks([])
    ax.set_yticks([])

    # Save and/or show the plot
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    plt.show()

    # Wait briefly
    time.sleep(0.1)



def run_test(file_name, save_png_path=None):
    rectangles = []
    size = 0
    bin_width, bin_height = 0, 0

    try:
        with open(file_name, 'r') as file:
            size = int(file.readline().strip('\n'))
            line = file.readline().strip('\n')  # '\n' gerekebilir
            bin_width, bin_height = map(int, line.split())
            rectangles = [(int(x), int(y)) for x, y in (line.split() for line in file)]
        print("Successfully read the file and created the array of tuples:", rectangles)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Create a new packer BBF
    packer = newPacker(rotation=True)

    # Add rectangles to pack
    for r in rectangles:
        packer.add_rect(*r)

    # Add a single bin with the size of the area
    packer.add_bin(bin_width, bin_height)

    # Pack the rectangles
    packer.pack()

    # Get the packed rectangles
    packed_rectangles = packer.rect_list()

    # Create results folder if it doesn't exist
    results_folder = "results"
    os.makedirs(results_folder, exist_ok=True)

    # Create file paths in the results folder
    if save_png_path:
        png_path = os.path.join(results_folder, save_png_path)
        plot_solution(packed_rectangles, bin_width, bin_height, size, png_path)

  

if __name__ == "_main_":
    basename = "/original/C"
    for i in range(1, 8):
        for j in range(1, 4):
            filename = basename + str(i) + "_" + str(j)
            print("Testing: ", str(i) + "_" + str(j))
            save_png_path = f"{filename}.png"
            run_test(filename, save_png_path)
