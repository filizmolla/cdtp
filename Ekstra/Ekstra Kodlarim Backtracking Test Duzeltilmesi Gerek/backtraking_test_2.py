from backtraking import Rectangle, Position, Rotate, Place, Placement, Sheet, PlacementEngine, readData, backtrack, extract_from_file
import os
import sys
path = "/home/filiz/Desktop/CDTP/original/"

results = []

for file in sorted(os.listdir(path)):
    data = extract_from_file(path+file, file)
    sheet, rectangles = readData(data)
    rectangles = sorted(rectangles, key=lambda rect: min(rect.width, rect.height), reverse=True)

    
    currentBest = PlacementEngine(None, [])
    i = 0

    engine = PlacementEngine(sheet, rectangles)
    result = backtrack(engine, list(map(lambda x: x.id, rectangles)))

    results.append((file, context.best.area(), len(context.best.getUnplacedRectangles())))
    print(f"{file} {currentBest.area()}/{sheet.area()} {len(currentBest.getUnplacedRectangles())}/{len(rectangles)}")

    # area = 0
    # for rect in rects:
    #     area += rect.area()
    # print(file, sheet.height*sheet.width, area, len(rects))
        

for result in results:
    print(result)
sys.exit(0)
