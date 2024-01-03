data = [
    [[0, 0], [0, 10], [2, 10], [2, 0]],
    [[2, 0], [2, 4], [6, 4], [6, 0]],
    [[6, 0], [6, 7], [8, 7], [8, 0]],
    [[8, 0], [8, 6], [10, 6], [10, 0]],
    [[2, 4], [2, 7], [6, 7], [6, 4]],
    [[2, 7], [2, 10], [5, 10], [5, 7]],
    [[5, 7], [5, 10], [8, 10], [8, 7]],
    [[8, 6], [8, 10], [10, 10], [10, 6]]
]

results = []
data = sorted(data, key=lambda x: x[0][0])


filename = 'C0_0'

with open(filename + "_GCode.gcode", "w") as f:
    ##ÖNEMLİ DEĞİŞTİRME: G91. Incremental mode.
    f.write("G21 G91 G94;Start code\n" + 
            "G00 Z20\nG00 X0 Y0 \nG01 Z-19\nG01 Z-1 F250 ;FEED RATE\nG01 X0 Y0 ;\n" )

        
    for i in range(len(data)):
        
        rectangle_positions = data[i]    
        current_first_element = data[i][0]
        if i < len(data) - 1:
            next_first_element = data[i + 1][0]
        subtracted_result = [b - a for a, b in zip(current_first_element, next_first_element)]
        results.append(subtracted_result)
        
        for i in range(len(rectangle_positions)):
            if i == (len(rectangle_positions) - 1):
                x1, y1 = rectangle_positions[i]
                x2, y2 = rectangle_positions[0]
            else:
                x1, y1 = rectangle_positions[i]
                x2, y2 = rectangle_positions[i + 1]
            
            dx = x2 - x1
            dy = y2 - y1
            #print(f"G01 X{dx} Y{dy}; \n")

            f.write(f"G01 X{dx} Y{dy} ;\n")     #KAREYİ ÇİZ
            
        f.write(f"G01 Z5;\n")       #ELİNİ KALDIR 
        f.write(f"G01 X{results[-1][0]} Y{results[-1][1]};\n") #BAŞKA KAREYE GİT 
        f.write(f"G01 Z-5; \n") #ELİNİ İNDİR
    f.write("G00 Z0 F70\n") #ne yapıyorlar bilmiyorum
    f.write("M30\n")



            