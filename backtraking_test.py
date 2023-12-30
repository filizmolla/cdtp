"""çalışmıyor
currentBest yüzünden global variable"""
from backtraking import Rectangle, Position, Rotate, Place, Placement, Sheet, PlacementEngine, readData, backtrack, extract_from_file
import random


for j in range(20):
    filename = 'C0_0'
    file_path = 'original/' + filename
    data = extract_from_file(file_path, filename)
    
    sheet, rectangles = readData(data)
    random.shuffle(rectangles)

    engine = PlacementEngine(sheet, rectangles)
    
    i = 0
    currentBest = PlacementEngine(None, [])
    result = backtrack(engine, list(map(lambda x: x.id, rectangles)))
    currentBest.savePlot(f"plots/{j}.png")
    print(f"{filename} {i} {currentBest.area()}/{sheet.area()} {len(currentBest.getUnplacedRectangles())}/{len(rectangles)}")