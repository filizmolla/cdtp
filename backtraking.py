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
            raise "Rectangle already placed."
            
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
        ax.set_xlim(0, self.sheet.width * 1.5)  
        ax.set_ylim(0, self.sheet.height * 1.5)      
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
        



def track(rectangle_id, reference_rectangle_id, placement, rotation):
    
    for placedRectangles in list(engine.placements.values()) + [None]:
        for placement in [Place.LEFT, Place.TOP]:
            for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90]:
                engine.place(rectangle.id, placedRectangles, placement, rotation)

    result = engine.place(rectangle_id, reference_rectangle_id, placement, rotation)
    
    if result == True:
        for rectnagle in engine.getUnplacedRectangles():
            track()
    else: 
        return False
    
def backtrack(sheet, rectangles):
    engine = PlacementEngine(sheet, rectangles)
    
    for rectangle in rectangles:
        for placedRectangles in list(engine.placements.values()) + [None]:
            for placement in [Place.LEFT, Place.TOP]:
                for rotation in [Rotate.ROTATE_0, Rotate.ROTATE_90]:
                    engine.place(rectangle.id, placedRectangles, placement, rotation)
    



# sheet, rectangles = readData(data)
# print(sheet, rectangles)

# engine = PlacementEngine(sheet, rectangles)
# print(engine.rectangles)

# # print(engine.place(1, None, Place.TOP, Rotate.ROTATE_90))
# # print(engine.place(3, 1, Place.LEFT, Rotate.ROTATE_90))
# # print(engine.place(4, 1, Place.LEFT, Rotate.ROTATE_90))
# # print(engine.place(0, 1, Place.TOP, Rotate.ROTATE_0))

# print(engine.place(1, None, Place.TOP, Rotate.ROTATE_90))
# print(engine.place(3, 1, Place.TOP, Rotate.ROTATE_90))
# print(engine.place(0, 1, Place.LEFT, Rotate.ROTATE_90))
# print(engine.placements)
# print(engine.getUnplacedRectangles())
# engine.unplace(0)
# engine.unplace(3)

# print(engine.placements)
# engine.draw()

backtrack(sheet, rectangles)

