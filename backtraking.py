"""
Created on Tue Dec 26 22:06:04 2023

@author: filiz
"""

from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from tkinter import filedialog
import os
import time

class Rectangle:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width 
        self.height = height 
        self.isRotated = False
        
    
    def area(self):
        return self.width * self.height

    def isSquare(self):
        return self.width == self.height
    
    def clone(self):
        return Rectangle(self.id, self.width, self.height)
    
    def __repr__(self):
        return f"({self.id} -> {self.width} {self.height})"

class Position: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def clone(self):
        return Position(self.x, self.y)
        
    def __repr__(self):
        return f"[{self.x} {self.y}]"

class Rotate(Enum):
    ROTATE_0 = 0
    ROTATE_90 = 1

class Place(Enum):
    TOP = 0
    LEFT = 1


class Placement: 
    def __init__(self, rectangle, position, rotation, refercence_rectangle_id = None, placement_according_to_ref = None):
        self.rectangle = rectangle
        self.position = position
        self.rotation= rotation
        self.availableTop  = rectangle.width if rotation == Rotate.ROTATE_0 else rectangle.height
        self.availableLeft = rectangle.height if rotation == Rotate.ROTATE_0 else rectangle.width
        self.referenceRectangleId = refercence_rectangle_id
        self.placementAccordingToRef = placement_according_to_ref
    
    def clone(self):
        return Placement(self.rectangle.clone(), self.position.clone(), self.rotation, self.referenceRectangleId, self.placementAccordingToRef)
        
    def rotatedWidth(self):
        return self.rectangle.width if self.rotation == Rotate.ROTATE_0 else self.rectangle.height
    
    def rotatedHeight(self):
       return self.rectangle.height if self.rotation == Rotate.ROTATE_0 else self.rectangle.width
       
        
    def top_right(self):
        return Position(self.position.x + self.rotatedWidth(), self.position.y + self.rotatedHeight())

    def top_left(self):
        return Position(self.position.x, self.position.y + self.rotatedHeight())

    def bottom_right(self):
        return Position(self.position.x + self.rotatedWidth(), self.position.y)
      
    def bottom_left(self):
        return Position(self.position.x, self.position.y)

        
    def __repr__(self):
        return f"{{ {self.rectangle} - {self.position} - {self.rotation} - at: {self.availableTop} al:{self.availableLeft} }}"


class Sheet: 
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def clone(self):
        return Sheet(self.width, self.height)
    
    def __repr__(self):
        return f"(Width: {self.width}, Height: {self.height})"


class PlacementEngine:
    
    def __init__(self, sheet, rectangles):
        self.sheet = sheet
        self.rectangles = dict(zip(map(lambda x: x.id , rectangles), rectangles))
        self.placements = dict([])
        self.score#idk

    def area(self):
        area = 0
        for placement in self.placements.values():
            area += placement.rectangle.area()
        return area
    
    def clone(self):
        placementEngine = PlacementEngine(self.sheet, list(self.rectangles.values()))
        
        result = dict([])
        for key, value in self.placements.items():
            result[key] = value.clone()
        placementEngine.placements = result

        return placementEngine
        
        
    def checkOverlappingRects(self, newPlacement):
        def intersects(first, second):
            return not (first.top_right().x <= second.bottom_left().x
                or first.bottom_left().x >= second.top_right().x
                or first.top_right().y <= second.bottom_left().y
                or first.bottom_left().y >= second.top_right().y)

        for placement in self.placements.values():
            #print(f"intersect - {placement}, {newPlacement}, {intersects(placement, newPlacement)}")
            if intersects(placement, newPlacement):
                return True # there are overlapping rectangles 
        return False

    def isInsideOfTheSheet(self, newPlacement):
        if newPlacement.top_left().y > self.sheet.height:
            return False
        
        if newPlacement.top_right().x > self.sheet.width:
            return False
        
        return True

    def getUnplacedRectangles(self):
        diff = []
        for rect_id in self.rectangles.keys():
                if rect_id not in self.placements.keys():
                    diff.append(rect_id)
        return diff

    def place(self, rectangle_id, referance_rectangle_id, place, rotation):
        if(self.placements.get(rectangle_id) != None):
            raise Exception("Rectangle already placed.")
            
        rect = self.rectangles.get(rectangle_id)
        if rect == None:
            raise "There are no rectangle with given id"
        
        if referance_rectangle_id == None:
            position = Position(0, 0)
            placement = Placement(rect, position, rotation)
            self.placements[rect.id] = placement
            # print("Place first to origin")
            if rotation == Rotate.ROTATE_90:
                rect.isRotated = True
            else:
                rect.isRotate = False
            return True
        
        refRectPlacement = self.placements.get(referance_rectangle_id)
        if (refRectPlacement == None):
            raise "Reference rectangle does not placed."
            
        rectWidth  = rect.width  if rotation == Rotate.ROTATE_0 else rect.height
        rectHeight = rect.height if rotation == Rotate.ROTATE_0 else rect.width
        
        #idk:
 #       print(rectWidth, rectHeight)
 #       print(refRectPlacement.rectangle.width, refRectPlacement.rectangle.height, refRectPlacement.rectangle.isRotated)
        
        #idk:
        if refRectPlacement.rectangle.isRotated:
            refRectangleWidth = refRectPlacement.rectangle.height
            refRectangleHeight = refRectPlacement.rectangle.width
        else:
            refRectangleWidth = refRectPlacement.rectangle.width
            refRectangleHeight = refRectPlacement.rectangle.height
            
        
            
        
        if place == Place.LEFT:
            if refRectPlacement.availableLeft <= 0:
                return False
            
            position = Position(
                        refRectPlacement.position.x + refRectPlacement.rotatedWidth(), 
                        refRectPlacement.position.y + (refRectPlacement.rotatedHeight() - refRectPlacement.availableLeft))
            
            
            placement = Placement(rect, position, rotation, referance_rectangle_id, place)
            #idk:
            if rotation == Rotate.ROTATE_0:
                 rect.isRotated = False
            else:
                 rect.isRotated = True
            
            if placement.top_left().y < 0 or placement.bottom_left().y < 0:
                pass 

            
            if self.checkOverlappingRects(placement):
                return False

            if not self.isInsideOfTheSheet(placement):
                return False

            self.placements[rect.id] = placement
            refRectPlacement.availableLeft = refRectPlacement.availableLeft - rectHeight
            return True
        else: 
            if refRectPlacement.availableTop <= 0:
                return False
            
            position = Position(
                        refRectPlacement.position.x + (refRectPlacement.rotatedWidth() - refRectPlacement.availableTop), 
                        refRectPlacement.position.y + refRectPlacement.rotatedHeight() )
            placement = Placement(rect, position, rotation, referance_rectangle_id, place)
            # print(f"\n\ncheck: {self.checkOverlappingRects(placement)}\n\n")
           
            if placement.top_left().y < 0 or placement.bottom_left().y < 0:
                pass 
           
            #idk:
            if rotation == Rotate.ROTATE_0:
                 rect.isRotated = False
            else:
                 rect.isRotated = True
            
            
            if self.checkOverlappingRects(placement):
                return False
            
            if not self.isInsideOfTheSheet(placement):
                return False
            
            self.placements[rect.id] = placement
            refRectPlacement.availableTop = refRectPlacement.availableTop- rectWidth
            return True

    def unplace(self, rectangle_id):
        rectanglePlacement = self.placements.get(rectangle_id)
        if rectanglePlacement == None:
            raise "Rectangle has been not placed."

        referenceRectanglePlacement = self.placements.get(rectanglePlacement.referenceRectangleId)
        if referenceRectanglePlacement != None:
            if rectanglePlacement.placementAccordingToRef == Place.LEFT:
                referenceRectanglePlacement.availableLeft += rectanglePlacement.rotatedHeight()
            else:
                referenceRectanglePlacement.availableTop += rectanglePlacement.rotatedWidth()
        
        del self.placements[rectangle_id]

    def draw(self, title = None):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.sheet.width)  
        ax.set_ylim(0, self.sheet.height)      

        
        # ax.grid(True)
        
        # ax.set_xticks(np.arange(-5, self.sheet.width * 1.5, 10))
        # ax.set_yticks(np.arange(-5, self.sheet.width * 1.5, 10))
        
        # # And a corresponding grid
        # ax.grid(which='both')
        
        # # Or if you want different settings for the grids:
        # ax.grid(which='major', alpha=0.5)

        
        
        for placement in self.placements.values():
            rect = patches.Rectangle(
                (placement.position.x, placement.position.y),  
                placement.rectangle.width if placement.rotation == Rotate.ROTATE_0 else placement.rectangle.height,
                placement.rectangle.height if placement.rotation == Rotate.ROTATE_0 else placement.rectangle.width,
                linewidth=1,
                edgecolor='r',
                facecolor='#FFE4C4'
                )
            ax.add_patch(rect)
            
        if not title is None:
            plt.title(title)
            
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        return fig
    
    def savePlot(self, filename):
        fig = self.draw()
        fig.savefig(filename, bbox_inches='tight')

        
    def score(self):
        a = list(self.placements.keys())
        b = list(range(len(self.rectangles)))        
        difference = list(set(b) - set(a))
        # print(difference)
        total_area = 0
        for indis in difference:
            missing = self.rectangles.get(indis)
            area = missing.height * missing.width
            total_area += area 
        #print(area, total_area)
        if total_area == 0:
            total_area = 1
        
        return 1/ total_area
        

def readData(data):
    lines = data.split("\n");
    rectangle_count = int(lines[0])
    sheet = list(map(lambda x: int(x), lines[1].strip(" ").split(" ")))
    sheet = Sheet(sheet[0], sheet[1])
    rectangles = []
    for i in range(len(lines) - 2):
        ln = lines[i+2].strip(" ")
        if len(ln) == 0:
            continue 
        rectangle = list(map(lambda x: int(x), ln.split(" ")))
        rectangles.append(Rectangle(i, rectangle[0], rectangle[1]))
    return sheet, rectangles

currentBest = PlacementEngine(None, [])
i = 0

def backtrack(engine, rectangles):
    global i
    global currentBest

    if len(rectangles) == 0:
        return True
    
    for rectangle in rectangles:
        for placed in ([None] if engine.placements.__len__() == 0 else []) + list(engine.placements.keys()):
            for placement in [Place.LEFT, Place.TOP]:
                for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90] if not engine.rectangles[rectangle].isSquare() else [Rotate.ROTATE_0]:
                    # print(rectangle, placed)
                    result = engine.place(rectangle, placed, placement, rotation)
                    
                    if engine.area() > currentBest.area():
                        currentBest = engine.clone()
                    
                    if i % 1000 == 0:
                       engine.draw(f"{i} - {engine.area()} - {rectangle} {placed} {placement} {rotation}")
                       print(i, engine.placements.keys(), rectangles, len(engine.placements.keys()), len(rectangles))
                    i += 1
                    
                    if i >= 500_0:
                        return True

                    if result:
                        unplaced = engine.getUnplacedRectangles()
                        result2 = backtrack(engine, unplaced)
                        if result2 == False:
                            engine.unplace(rectangle)
                        else: 
                            return True
                        
    return False

                        

def extract_from_file(file_path, file_name):
    with open(file_path, 'r') as file:
        data = ' \n'.join(line.strip() for line in file)
    return data
   
""" GUI"""




# def plot(): 

# 	# the figure that will contain the plot 
# 	fig = Figure(figsize = (5, 5), 
# 				dpi = 100) 

# 	# list of squares 
# 	y = [i**2 for i in range(101)] 

# 	# adding the subplot 
# 	plot1 = fig.add_subplot(111) 

# 	# plotting the graph 
# 	plot1.plot(y) 

# 	# creating the Tkinter canvas 
# 	# containing the Matplotlib figure 
# 	canvas = FigureCanvasTkAgg(fig, master = lower_frame) 
# 	canvas.draw() 

# 	# placing the canvas on the Tkinter window 
# 	canvas.get_tk_widget().pack() 

# 	# creating the Matplotlib toolbar 
# 	toolbar = NavigationToolbar2Tk(canvas, lower_frame) 
# 	toolbar.update() 

# 	# placing the toolbar on the Tkinter window 
# 	canvas.get_tk_widget().pack() 

def print_rectangles():
    # png to gcla 
    pass 



def start():
    chart_frame1 = tk.Frame(lower_frame) #, bg="#EB2645"
    #chart_frame1.pack(side="right")  
    chart_frame1.grid(row=0, column=0, sticky="nsew")
    
    chart_frame2 = tk.Frame(lower_frame) #, bg="#235FCA"
    #chart_frame2.pack(side="left")
    chart_frame2.grid(row=0, column=1, sticky="nsew")
    
   
    filename = 'C0_0'
    file_path = 'original/' + filename
    data = extract_from_file(file_path, filename)
    sheet, rectangles = readData(data)
    rectangles = sorted(rectangles, key=lambda rect: rect.area(), reverse=True)
    print(rectangles)
    engine = PlacementEngine(sheet, rectangles)
    t = time.process_time()
    result = backtrack(engine, list(map(lambda x: x.id, rectangles)))
    elapsed_time = time.process_time() - t
#    print(elapsed_time)
    # print(result)
    # print(engine.placements.keys())
    # print(engine.placements.items())
    
    fig = currentBest.draw(f"currentBest - {currentBest.area()} - {len(currentBest.getUnplacedRectangles())}")
    #print(currentBest.getUnplacedRectangles())    
    
    #Figure 2 için kalanları çizdir.
    kalan_rectangles = []
    for x in currentBest.getUnplacedRectangles():
        kalan_rectangles.append(currentBest.rectangles.get(x))
    #print(kalan_rectangles)   
    engine2 = PlacementEngine(sheet, kalan_rectangles)
    result2 = backtrack(engine2, list(map(lambda x: x.id, kalan_rectangles)))
    fig2 = engine2.draw(f"last - {engine.area()} - {len(engine.getUnplacedRectangles())}")
    
    # fig = Figure(figsize = (5, 5), dpi = 100) 
    # y = [i**2 for i in range(101)] 
    # plot1 = fig.add_subplot(111) 
    # plot1.plot(y) 
    canvas = FigureCanvasTkAgg(fig, chart_frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', expand=True, padx=10, pady=10)
    # toolbar = NavigationToolbar2Tk(canvas, chart_frame1)
    # toolbar.update() 
    # toolbar.pack(side="bottom")
    
    # fig2 = Figure(figsize = (5, 5), dpi = 100) 
    # y = [i*2 for i in range(101)] 
    # plot2 = fig2.add_subplot(111) 
    # plot2.plot(y) 
    canvas2= FigureCanvasTkAgg(fig2, chart_frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="top", expand=True,  padx=10, pady=10)
    
    # toolbar2 = NavigationToolbar2Tk(canvas2,chart_frame2) 
    # toolbar2.update() 
    # toolbar2.pack(side="bottom")

    

def selectFiles():
    filename = filedialog.askopenfilename(initialdir = "/home/filiz/Desktop/CDTP/original",
                                      title = "Select a File",
                                      filetypes=[("All files", "*")])
    filepath = filename
    filename=os.path.basename(filename).split('/')[-1]
    label_file_explorer.configure(text="File Opened: "+filename)
    


window = tk.Tk() 
window.title('Cutting Stock Problem Solution') 
window.geometry("1000x400") 

upper_frame = tk.Frame(window) #, bg="#BD99D9" 
upper_frame.pack(side="top", fill="x")

file_select_button = tk.Button(master= upper_frame, 
                            command= selectFiles, 
                            height=2, width= 10, 
                            text = "Select File"
                            )

file_select_button.pack(side="left", padx=25, pady=25)

label_file_explorer = tk.Label(upper_frame, 
                            text = "File Explorer using Tkinter",
                            width = 40, height = 4, 
                            fg = "blue")
label_file_explorer.pack(side="left", padx = 5, pady = 5)

# plot_button = tk.Button(master = upper_frame, 
#  					command = plot, 
#  					height = 2, 
#  					width = 10, 
#  					text = "Plot") 
# plot_button.pack(side="right", padx=20, pady=20) 

start_button = tk.Button(master = upper_frame, 
 					command = start, 
 					height = 2, 
 					width = 10, 
 					text = "Start")
start_button.pack(side="right", padx=20, pady=20) 


side_frame = tk.Frame(window) # , bg="#4C2A85"
side_frame.pack(side="right", fill="y")

print_button = tk.Button(master = side_frame, 
 					command = print_rectangles, 
 					height = 2, 
 					width = 10, 
 					text = "Print") 
print_button.pack(side="bottom", padx=20, pady=20)


label = tk.Label(upper_frame, text="0:00", font=25)
label.pack(side="right", pady=20, padx=20)


lower_frame = tk.Frame(window) #turkuasz  , bg="#4EDED6"
lower_frame.pack(fill='both', expand=True)
lower_frame.grid_columnconfigure(0, weight=1, uniform="group1")
lower_frame.grid_columnconfigure(1, weight=1, uniform="group1")
lower_frame.grid_rowconfigure(0, weight=1)


window.mainloop() 




"""
C0_0 isimli dosyaya erişerek, her döngüde dikdörtgenleri random sırada veriyor ve başarısını kontrol ediyor.
"""
# import random

# for j in range(20):
#     filename = 'C0_0'
#     file_path = 'original/' + filename
#     data = extract_from_file(file_path, filename)
    
#     sheet, rectangles = readData(data)
#     random.shuffle(rectangles)

#     engine = PlacementEngine(sheet, rectangles)
    
#     i = 0
#     currentBest = PlacementEngine(None, [])
#     result = backtrack(engine, list(map(lambda x: x.id, rectangles)))
#     #currentBest.savePlot(f"plots/{j}.png")
#     print(f"{filename} {i} {currentBest.area()}/{sheet.area()} {len(currentBest.getUnplacedRectangles())}/{len(rectangles)}")




"""C0_0 dosyası için çalıştırılması"""
# filename = 'C0_0'
# file_path = 'original/' + filename
# data = extract_from_file(file_path, filename)
# sheet, rectangles = readData(data)
# print(sheet, rectangles)
# # rectangles = sorted(rectangles, key=lambda rect: max(rect.width, rect.height), reverse=True)
# rectangles = sorted(rectangles, key=lambda rect: rect.area(), reverse=True)
# engine = PlacementEngine(sheet, rectangles)
# import time
# t = time.process_time()
# result = backtrack(engine, list(map(lambda x: x.id, rectangles)))
# elapsed_time = time.process_time() - t
# print(i, elapsed_time)
# print(result)
# print(engine.placements.keys())
# print(engine.placements.items())
# engine.draw(f"last - {engine.area()} - {len(engine.getUnplacedRectangles())}")
# currentBest.draw(f"currentBest - {currentBest.area()} - {len(currentBest.getUnplacedRectangles())}")
# for placement in currentBest.placements.values():
#     print(placement.bottom_left(), placement.top_right())


