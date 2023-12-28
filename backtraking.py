#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 22:06:04 2023

@author: filiz
"""

from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.patches as patches

data = """6 
10 10
2 6
4 4
3 3
2 7 
3 3
2 4"""

data = """16 
20 20
2 12
7 12
8 6
3 6
3 5
5 5
3 12
3 7
5 7
2 6
3 2
4 2
3 4
4 4
9 2
11 2"""

data="""17
20 20
4 1
4 5
9 4
3 5
3 9
1 4
5 3
4 1
5 5
7 2
9 3
3 13
2 8
15 4
5 4
10 6
7 2"""

data="""16 
20 20
4 14
5 2
2 2
9 7
5 5
2 5
7 7
3 5
6 5
3 2
6 2
4 6
6 3
10 3
6 3
10 3"""

#C2_1
data="""28
60 30
7 5
14 5
14 8
4 8
21 13
7 11
14 11
14 5
4 5
18 3
21 3
17 11
4 11
7 4
5 4
6 7
18 5
3 5
7 3
5 3
18 4
3 4
12 2
6 2
18 5
21 5
17 3
4 3"""

#C4_2
data="""49
60 60
10 14
3 13
28 5
5 8
14 9
12 14
13 10
3 17
1 5
4 1
18 4
1 1 
2 6
4 14 
3 18
4 14
8 17
11 5
9 12
4 7
25 8
7 5
24 9
9 14
12 19
2 4
2 7
3 4
5 30
5 3
10 26
6 5
4 9
1 4
9 2
4 17
5 2
4 4
6 2
4 10
2 4
3 12
6 5
3 9
7 18
6 6
18 7
13 9
25 7"""

class Rectangle:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

    def isSquare(self):
        return self.width == self.height
    
    def __repr__(self):
        return f"({self.id} -> {self.width} {self.height})"

class Position: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
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

    def __repr__(self):
        return f"(Width: {self.width}, Height: {self.height})"


class PlacementEngine:
    
    def __init__(self, sheet, rectangles):
        self.sheet = sheet
        self.rectangles = dict(zip(map(lambda x: x.id , rectangles), rectangles))
        self.placements = dict([])

    def checkOverlappingRects(self, newPlacement):
        def intersects(first, second):
            return not (first.top_right().x <= second.bottom_left().x
                or first.bottom_left().x >= second.top_right().x
                or first.top_right().y <= second.bottom_left().y
                or first.bottom_left().y >= second.top_right().y)

        for placement in self.placements.values():
            # print(f"intersect - {placement}, {newPlacement}, {intersects(placement, newPlacement)}")
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
            print("Place first to origin")
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
                        refRectPlacement.position.x + refRectPlacement.rectangle.width, 
                        refRectPlacement.position.y + (refRectPlacement.rectangle.height - refRectPlacement.availableLeft))
            placement = Placement(rect, position, rotation, referance_rectangle_id, place)
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
                        refRectPlacement.position.x + (refRectPlacement.rectangle.width - refRectPlacement.availableTop), 
                        refRectPlacement.position.y + refRectPlacement.rectangle.height )
            placement = Placement(rect, position, rotation, referance_rectangle_id, place)
            # print(f"\n\ncheck: {self.checkOverlappingRects(placement)}\n\n")
            
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

    def draw(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-1, self.sheet.width * 1.5)  
        ax.set_ylim(-1, self.sheet.height * 1.5)      
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
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    



def readData(data):
    lines = data.split("\n");
    rectangle_count = int(lines[0])
    sheet = list(map(lambda x: int(x), lines[1].strip(" ").split(" ")))
    sheet = Sheet(sheet[0], sheet[1])
    rectangles = []
    for i in range(len(lines) - 2):
        rectangle = list(map(lambda x: int(x), lines[i+2].strip(" ").split(" ")))
        rectangles.append(Rectangle(i, rectangle[0], rectangle[1]))
    return sheet, rectangles
        



# def track(rectangle_id, reference_rectangle_id, placement, rotation):
    
#     for placedRectangles in list(engine.placements.values()) + [None]:
#         for placement in [Place.LEFT, Place.TOP]:
#             for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90]:
#                 engine.place(rectangle_id, placedRectangles, placement, rotation)

#     result = engine.place(rectangle_id, reference_rectangle_id, placement, rotation)
    
#     if result == True:
#         for rectangle in engine.getUnplacedRectangles():
#             track()
#     else: 
#         return False
    
# def backtrack(sheet, rectangles):
#     engine = PlacementEngine(sheet, rectangles)
    
#     for rectangle in rectangles:
#         for placedRectangles in list(engine.placements.values()) + [None]:
#             for placement in [Place.LEFT, Place.TOP]:
#                 for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90]:
#                     engine.place(rectangle.id, placedRectangles, placement, rotation)
    


def backtrack(engine, rectangles):
    if len(rectangles) == 0:
        return True
    
    i = 0
    for rectangle in rectangles:
        for placed in ([None] if engine.placements.__len__() == 0 else []) + list(engine.placements.keys()):
            for placement in [Place.LEFT, Place.TOP]:
                for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90]:
                    # print(rectangle, placed)
                    result = engine.place(rectangle, placed, placement, rotation)
                    print(engine.placements.keys(), rectangles)
                    if i % 1000 == 0:
                        engine.draw()
                    i += 1
                    
                    if result:
                        unplaced = engine.getUnplacedRectangles()
                        result2 = backtrack(engine, unplaced)
                        if result2 == False:
                            engine.unplace(rectangle)
                        else: 
                            return True
        
  
# def backtrack(engine, rectangles):
#     #print(rectangles)
#     if not rectangles:
#         print("Solution found:")
#         engine.draw()
#         return True
    
#     current_rectangle = rectangles[0]
#     engine.place(current_rectangle.id, None, Place.TOP, Rotate.ROTATE_0)
#     rectangles.pop(0)
#     engine.draw()
    
#     #print(current_rectangle)

#     for rectangle in rectangles:
#         print(f"{rectangle}")
#         for placed_rectangle_id, placed_rectangle in engine.placements.items():
#             print(f"Placed: {placed_rectangle}, {placed_rectangle_id}")
#             for placement in [Place.LEFT, Place.TOP]:
#                 print(placement)
#                 for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90]:
#                      print(rotation)
                     
#                      result = engine.place(rectangle.id, placed_rectangle_id, placement, rotation)
#                      engine.draw()
#                      if result:
#                         print(f"Placed rectangle {current_rectangle.id} successfully.")
#                         print("Current placements:", engine.placements)
#                         res = backtrack(engine, rectangles[1:])
#                         if not res:
#                             print(f"Backtracked from rectangle {current_rectangle.id}.")
#                             engine.unplace(current_rectangle.id)
                        

def extract_from_file(file_path, file_name):
    with open(file_path, 'r') as file:
        data = ' \n'.join(line.strip() for line in file)
    #data = '"""' + data + '"""'
    return data
   
filename = 'C7_3'
file_path = 'original/' + filename
data = extract_from_file(file_path, filename)

print(data)



sheet, rectangles = readData(data)
# print(sheet, rectangles)



#rectangles = sorted(rectangles, key=lambda rect: (rect.width, rect.height), reverse=True)




engine = PlacementEngine(sheet, rectangles)
print(engine.rectangles)



# print(engine.place(1, None, Place.TOP, Rotate.ROTATE_90))
# print(engine.place(3, 1, Place.LEFT, Rotate.ROTATE_90))
# print(engine.place(4, 1, Place.LEFT, Rotate.ROTATE_90))
# print(engine.place(0, 1, Place.TOP, Rotate.ROTATE_0))
# engine.draw()
# print(engine.placements)


# print(engine.place(1, None, Place.TOP, Rotate.ROTATE_90))
# print(engine.place(3, 1, Place.TOP, Rotate.ROTATE_90))
# print(engine.place(0, 1, Place.LEFT, Rotate.ROTATE_90))
# print(engine.placements)
# print(engine.getUnplacedRectangles())
# engine.unplace(0)
# engine.unplace(3)



engine.draw()

result = backtrack(engine, list(map(lambda x: x.id, rectangles)))
print(result)
print(engine.placements.keys())