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
import tkinter.ttk as ttk
import threading
from collections import deque
plt.switch_backend('agg')


class Rectangle:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width 
        self.height = height 
        
        
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
    
    def copyOfPlacements(self):
        result = dict([])
        for key, value in self.placements.items():
            result[key] = value.clone()

        return result
    
        
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
            return True
        
        refRectPlacement = self.placements.get(referance_rectangle_id)
        if (refRectPlacement == None):
            raise "Reference rectangle does not placed."
            
        rectWidth  = rect.width  if rotation == Rotate.ROTATE_0 else rect.height
        rectHeight = rect.height if rotation == Rotate.ROTATE_0 else rect.width
            
        
            
        
        if place == Place.LEFT:
            if refRectPlacement.availableLeft <= 0:
                return False
            
            position = Position(
                        refRectPlacement.position.x + refRectPlacement.rotatedWidth(), 
                        refRectPlacement.position.y + (refRectPlacement.rotatedHeight() - refRectPlacement.availableLeft))
            
            
            placement = Placement(rect, position, rotation, referance_rectangle_id, place)
            
            
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
        #plt.show()
        return fig, ax
    
    def savePlot(self, filename):
        fig, ax = self.draw()
        fig.savefig(filename, bbox_inches='tight')

    
        

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







class Context:
    
    def __init__(self, best, inform_callback = None):
        self.best = best
        self.iteration = 0
        self.inform_callback = inform_callback


def backtrack(engine, rectangles, context):
    # global i
    # global currentBest

    if len(rectangles) == 0:
        return True
    
    for rectangle in rectangles:
        for placed in ([None] if engine.placements.__len__() == 0 else []) + list(engine.placements.keys()):
            for placement in [Place.LEFT, Place.TOP]:
                for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90] if not engine.rectangles[rectangle].isSquare() else [Rotate.ROTATE_0]:
                    # print(rectangle, placed)
                    result = engine.place(rectangle, placed, placement, rotation)
                    
                    if engine.area() > context.best.area():
                        context.best = engine.clone()
                        
                    # print(context.iteration, context.best.area(), context.best)
                    # if context.iteration % 10000 == 0:
                    #     if context.inform_callback != None:
                    #         context.inform_callback(context.iteration, context.best)
                        #engine.draw(f"{context.iteration} - {engine.area()} - {rectangle} {placed} {placement} {rotation}")
                        #print(context.iteration, engine.placements.keys(), rectangles, len(engine.placements.keys()), len(rectangles))
                    
                    context.iteration += 1
                    
                    if context.iteration >= 500_000:
                        return True

                    if result:
                        unplaced = engine.getUnplacedRectangles()
                        result2 = backtrack(engine, unplaced, context)
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
#Coordinates to GCode
def print_rectangles():
    SCALE_FACTOR = 4
    results = []
    data = rectangles_to_print
    data = sorted(data, key=lambda position_list: position_list[0].x)    
    dataset_name = label_file_explorer.cget("text")
    dataset_name = dataset_name.split()[-1]   
    file_name = dataset_name + "_GCode.gcode"
    if file_name[:2] == 'C1':
        rec_width = 20
        rec_height = 20
    
    with open(file_name, "w") as f:
        ##G91. Incremental mode!
        f.write("G21 G91 G94;Start code\n" + 
                "M3 S90\nG00 X0 Y0 \nM3 S250\n")
        if rec_height != None and rec_width != None:
            f.write(f"G01 X0 Y0 F250;\nG01 X0 Y{rec_height*SCALE_FACTOR};Outer Rec Height\nG01 X{rec_width*SCALE_FACTOR} Y0 ;Outer Rectangle Width\nG01 X0 Y-{rec_height*SCALE_FACTOR} ;Outer Rectangle Height\nG01 X-{rec_width*SCALE_FACTOR} Y0 ;Outer Rectangle Width\n")
        f.write("G01 X0 Y0 ;\n" )

            
        for i in range(len(data)):
            
            rectangle_positions = data[i]    
            current_first_element = data[i][0]
            if i < len(data) - 1:
                next_first_element = data[i + 1][0]
                subtracted_result = Position(next_first_element.x - current_first_element.x, 
                                             next_first_element.y - current_first_element.y)
                results.append(subtracted_result)

            
            for i in range(len(rectangle_positions)):
                if i == (len(rectangle_positions) - 1):
                    x1, y1 = rectangle_positions[i].x, rectangle_positions[i].y
                    x2, y2 = rectangle_positions[0].x, rectangle_positions[0].y
                else:
                    x1, y1 = rectangle_positions[i].x, rectangle_positions[i].y
                    x2, y2 = rectangle_positions[i + 1].x, rectangle_positions[i + 1].y
                    
                
                dx = (x2 - x1)*SCALE_FACTOR
                dy = (y2 - y1)*SCALE_FACTOR
                #print(f"G01 X{dx} Y{dy}; \n")

                f.write(f"G01 X{dx} Y{dy} ;\n")     #KAREYİ ÇİZ
                
            f.write(f"M3 S90;\n")       #ELİNİ KALDIR 
            f.write(f"G01 X{results[-1].x*SCALE_FACTOR} Y{results[-1].y*SCALE_FACTOR};\n") #BAŞKA KAREYE GİT 
            f.write(f"M3 S250; \n") #ELİNİ İNDİR
        f.write("M3 S90\n") # en son elini kaldırsın
        f.write("G21G90 G0Z5\nG90 G0 X0 Y0\nG90 G0 Z0\nM30\n")
    print(f"Solution is saved to {file_name}!")
    print_done_label.config(text=f"Solution \nis \nsaved \nto \n{file_name}")

rectangles_to_print= []


def start():
    global rectangles_to_print
    print_done_label.config(text="")
    rectangles_to_print= []
    chart_frame1 = tk.Frame(lower_frame)
    chart_frame1.grid(row=0, column=0, sticky="nsew")
    
    chart_frame2 = tk.Frame(lower_frame)
    chart_frame2.grid(row=0, column=1, sticky="nsew")
    
   
    filename = label_file_explorer.cget("text")
    filename = filename.split()[-1]        
    file_path = 'original/' + filename
    data = extract_from_file(file_path, filename)
    sheet, rectangles = readData(data)
    rectangles = sorted(rectangles, key=lambda rect: rect.area(), reverse=True)
    engine = PlacementEngine(sheet, rectangles)
    
    # def inform_fn(iteration, best):
    #     fig, ax = best.draw(f"{iteration} - {best.area()} - {len(best.getUnplacedRectangles())}")
    #     def fn():
    #         canvas = FigureCanvasTkAgg(fig, chart_frame1)
    #         canvas.draw()
    #         canvas.get_tk_widget().pack(side='top', expand=True, padx=10, pady=10)
    #         toolbar = NavigationToolbar2Tk(canvas, chart_frame1)
    #         toolbar.update() 
    #         toolbar.pack(side="bottom")
    #     message_queue.append(fn)
        
        
    t = time.process_time()
    context = Context(PlacementEngine(sheet, []))
    result = backtrack(engine, list(map(lambda x: x.id, rectangles)), context)
    elapsed_time = time.process_time() - t
    
    clock_label.configure(text=str(round(elapsed_time, 2)) + "s") 
    #print(elapsed_time)
    # print(result)
    # print(engine.placements.keys())
    # print(engine.placements.items())
    
    fig, ax = context.best.draw(f"Best Solution Area: {context.best.area()}, Remining Rect Count: {len(context.best.getUnplacedRectangles())}")    
    for placement in context.best.placements.values():
        #print(f"[{placement.bottom_left()}, {placement.top_left()}, {placement.top_right()}, {placement.bottom_right()}]")
        rectangles_to_print.append([placement.bottom_left(),placement.top_left(), placement.top_right(), placement.bottom_right()])
    
    #Figure 2 için kalanları çizdir.
    kalan_rectangles = []
    for x in context.best.getUnplacedRectangles():
        kalan_rectangles.append(context.best.rectangles.get(x))
    #print(kalan_rectangles)   
    engine2 = PlacementEngine(sheet, kalan_rectangles)
    context = Context(PlacementEngine(sheet, []))
    result2 = backtrack(engine2, list(map(lambda x: x.id, kalan_rectangles)), context)
    fig2, ax = context.best.draw(f"Remaining Rectangles Area: {context.best.area()} - {len(context.best.getUnplacedRectangles())}")
    
    
    canvas = FigureCanvasTkAgg(fig, chart_frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', expand=True, fill=tk.BOTH,padx=10, pady=10)
    toolbar = NavigationToolbar2Tk(canvas, chart_frame1)
    toolbar.update() 
    toolbar.pack(side="bottom")
    
    
    canvas2= FigureCanvasTkAgg(fig2, chart_frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="top", expand=True,  fill=tk.BOTH, padx=10, pady=10)
    toolbar2 = NavigationToolbar2Tk(canvas2,chart_frame2) 
    toolbar2.update() 
    toolbar2.pack(side="bottom")


def selectFiles():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    filename = filedialog.askopenfilename(initialdir = current_directory + "/original",
                                      title = "Select a File",
                                      filetypes=[("All files", "*")])
    filepath = filename
    filename=os.path.basename(filename).split('/')[-1]
    label_file_explorer.configure(text="File Selected: "+filename)
    


window = tk.Tk() 
window.title('Cutting Stock Problem Solution') 
window.geometry("1000x580") 

upper_frame = tk.Frame(window) 
upper_frame.pack(side="top", fill="x")

file_select_button = tk.Button(master= upper_frame, 
                            command= selectFiles, 
                            height=2, width= 10, 
                            text = "Select File"
                            )

file_select_button.pack(side="left", padx=25, pady=25)

label_file_explorer = tk.Label(upper_frame, 
                            text = "Please Select a File and Press Start!",
                            width = 40, height = 4, 
                            fg = "blue")
label_file_explorer.pack(side="left", padx = 5, pady = 5)

start_button = tk.Button(master = upper_frame, 
 					command = start, 
 					height = 2, 
 					width = 10, 
 					text = "Start")
start_button.pack(side="right", padx=20, pady=20) 


side_frame = tk.Frame(window) 
side_frame.pack(side="right", fill="y")

print_button = tk.Button(master = side_frame, 
 					command = print_rectangles, 
 					height = 2, 
 					width = 10, 
 					text = "Print") 
print_button.pack(side="bottom", padx=20, pady=20)


clock_label = tk.Label(side_frame, text="0s", font=25)
clock_label.pack(side="top", pady=20, padx=20)

print_done_label = tk.Label(side_frame, fg = "blue")
print_done_label.pack(side="top", pady=20, padx=20)

lower_frame = tk.Frame(window) 
lower_frame.pack(fill='both', expand=True)
lower_frame.grid_columnconfigure(0, weight=1, uniform="group1")
lower_frame.grid_columnconfigure(1, weight=1, uniform="group1")
lower_frame.grid_rowconfigure(0, weight=1)




# chart_frame1 = tk.Frame(lower_frame) #, bg="#EB2645"
# #chart_frame1.pack(side="right")  
# chart_frame1.grid(row=0, column=0, sticky="nsew")

# chart_frame2 = tk.Frame(lower_frame) #, bg="#235FCA"
# #chart_frame2.pack(side="left")
# chart_frame2.grid(row=0, column=1, sticky="nsew")






# canvas = FigureCanvasTkAgg(fig, chart_frame1)
# canvas.draw()
# canvas.get_tk_widget().pack(side='top', expand=True, padx=10, pady=10)
# toolbar = NavigationToolbar2Tk(canvas, chart_frame1)
# toolbar.update() 
# toolbar.pack(side="bottom")


# canvas2= FigureCanvasTkAgg(fig2, chart_frame2)
# canvas2.draw()
# canvas2.get_tk_widget().pack(side="top", expand=True,  padx=10, pady=10)

# toolbar2 = NavigationToolbar2Tk(canvas2,chart_frame2) 
# toolbar2.update() 
# toolbar2.pack(side="bottom")





# Periodically check for text updates, in the gui thread.
# Where 'gui thread' is the main thread,
# that is running the gui event-loop.
# Should only access the gui, in the gui thread/event-loop.

# def consume_text():
#     try:
#         fn = message_queue.popleft()
#         fn()
#     except IndexError:
#         pass  # Ignore, if no text available.
#     # Reschedule call to consumeText.
#     window.after(ms=1000, func=consume_text)


# consume_text()  # Start the consumeText 'loop'.


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
#     context.best = PlacementEngine(None, [])
#     result = backtrack(engine, list(map(lambda x: x.id, rectangles)))
#     #context.best.savePlot(f"plots/{j}.png")
#     print(f"{filename} {i} {context.best.area()}/{sheet.area()} {len(context.best.getUnplacedRectangles())}/{len(rectangles)}")




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
# context.best.draw(f"context.best - {context.best.area()} - {len(context.best.getUnplacedRectangles())}")
# for placement in context.best.placements.values():
#     print(placement.bottom_left(), placement.top_right())


