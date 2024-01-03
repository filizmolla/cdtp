from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk) 
from tkinter import filedialog
import matplotlib.pyplot as plt 
import os
from backtraking import Rectangle, Position, Rotate, Place, Placement, Sheet, PlacementEngine, readData, backtrack, extract_from_file, currentBest, i
import time



def plot(): 

	# the figure that will contain the plot 
	fig = Figure(figsize = (5, 5), 
				dpi = 100) 

	# list of squares 
	y = [i**2 for i in range(101)] 

	# adding the subplot 
	plot1 = fig.add_subplot(111) 

	# plotting the graph 
	plot1.plot(y) 

	# creating the Tkinter canvas 
	# containing the Matplotlib figure 
	canvas = FigureCanvasTkAgg(fig, master = lower_frame) 
	canvas.draw() 

	# placing the canvas on the Tkinter window 
	canvas.get_tk_widget().pack() 

	# creating the Matplotlib toolbar 
	toolbar = NavigationToolbar2Tk(canvas, lower_frame) 
	toolbar.update() 

	# placing the toolbar on the Tkinter window 
	canvas.get_tk_widget().pack() 



def start():
    chart_frame1 = Frame(lower_frame, bg="#EB2645")
    chart_frame1.pack(side="right")  
    chart_frame2 = Frame(lower_frame, bg="#235FCA")
    chart_frame2.pack(side="left")
    
    
   
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
    print(elapsed_time)
    print(result)
    print(engine.placements.keys())
    print(engine.placements.items())
    engine.draw(f"last - {engine.area()} - {len(engine.getUnplacedRectangles())}")
    currentBest.draw(f"currentBest - {currentBest.area()} - {len(currentBest.getUnplacedRectangles())}")


    fig = Figure(figsize = (5, 5), dpi = 100) 
    y = [i*2 for i in range(101)] 
    plot1 = fig.add_subplot(111) 
    plot1.plot(y) 
    canvas = FigureCanvasTkAgg(fig, chart_frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', expand=True, padx=20, pady=20)
    toolbar = NavigationToolbar2Tk(canvas, chart_frame1)
    toolbar.update() 
    toolbar.pack(side="bottom")
    
    fig2 = Figure(figsize = (5, 5), dpi = 100) 
    y = [i**2 for i in range(101)] 
    plot2 = fig2.add_subplot(111) 
    plot2.plot(y) 
    canvas2= FigureCanvasTkAgg(fig2, chart_frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="top", expand=True, padx=20, pady=20)
    
    toolbar2 = NavigationToolbar2Tk(canvas2,chart_frame2) 
    toolbar2.update() 
    toolbar2.pack(side="bottom")

    

def selectFiles():
    filename = filedialog.askopenfilename(initialdir = "/home/filiz/Desktop/CDTP/original",
                                      title = "Select a File",
                                      filetypes=[("All files", "*")])
    filepath = filename
    filename=os.path.basename(filename).split('/')[-1]
    label_file_explorer.configure(text="File Opened: "+filename)
    


window = Tk() 
window.title('Cutting Stock Problem Solution') 
window.geometry("1000x600") 




upper_frame = Frame(window, bg="#BD99D9")
upper_frame.pack(side="top", fill="x")

file_select_button = Button(master= upper_frame, 
                            command= selectFiles, 
                            height=2, width= 10, 
                            text = "Select File"
                            )

file_select_button.pack(side="left", padx=25, pady=25)

label_file_explorer = Label(upper_frame, 
                            text = "File Explorer using Tkinter",
                            width = 40, height = 4, 
                            fg = "blue")
label_file_explorer.pack(side="left", padx = 5, pady = 5)

plot_button = Button(master = upper_frame, 
 					command = plot, 
 					height = 2, 
 					width = 10, 
 					text = "Plot") 
plot_button.pack(side="right", padx=20, pady=20) 

start_button = Button(master = upper_frame, 
 					command = start, 
 					height = 2, 
 					width = 10, 
 					text = "Start")
start_button.pack(side="right", padx=20, pady=20) 


side_frame = Frame(window, bg="#4C2A85")
side_frame.pack(side="right", fill="y")

print_button = Button(master = side_frame, 
 					command = plot, 
 					height = 2, 
 					width = 10, 
 					text = "Print") 
print_button.pack(side="bottom", padx=20, pady=20)


label = Label(side_frame, text="İşlem \ndevam \nediyor\n", bg="#4C2A85", fg="#FFF", font=25)
label.pack(pady=20, padx=20)




# charts_frame = Frame(window, bg="#EB2645") #pink
# charts_frame.pack()

lower_frame = Frame(window, bg="#4EDED6") #turkuasz
lower_frame.pack(fill='both', expand=True)


window.mainloop() 
