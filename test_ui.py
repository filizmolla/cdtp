from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk) 
from tkinter import filedialog
import matplotlib.pyplot as plt 

# plot function is created for 
# plotting the graph in 
# tkinter window 
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
	canvas = FigureCanvasTkAgg(fig, 
							master = window) 
	canvas.draw() 

	# placing the canvas on the Tkinter window 
	canvas.get_tk_widget().pack() 

	# creating the Matplotlib toolbar 
	toolbar = NavigationToolbar2Tk(canvas, 
								window) 
	toolbar.update() 

	# placing the toolbar on the Tkinter window 
	canvas.get_tk_widget().pack() 


def selectFiles():
    filename = filedialog.askopenfilename(initialdir = "/home/filiz/Desktop/CDTP/original",
                                      title = "Select a File",
                                      filetypes=[("All files", "*")])
  
    label_file_explorer.configure(text="File Opened: "+filename)


# the main Tkinter window 
window = Tk() 

# setting the title 
window.title('Cutting Stock Problem Solution') 

# dimensions of the main window 
window.geometry("800x500") 




# # button that displays the plot 
# plot_button = Button(master = window, 
# 					command = plot, 
# 					height = 2, 
# 					width = 10, 
# 					text = "Plot") 


# file_select_button = Button(master= window, 
#                             command= selectFiles, 
#                             height=2, width= 10, 
#                             text = "Select File"
#                             )

# file_select_button.place(x=25, y=25)

# label_file_explorer = Label(window, 
#                             text = "File Explorer using Tkinter",
#                             width = 100, height = 4, 
#                             fg = "blue")
# label_file_explorer.place(x = 50, y = 60)


side_frame = Frame(window, bg="#4C2A85")
side_frame.pack(side="right", fill="y")


label = Label(side_frame, text="Dashboard", bg="#4C2A85", fg="#FFF", font=25)
label.pack(pady=20, padx=20)




charts_frame = Frame(window, bg="#342A85")
charts_frame.pack()
lower_frame = Frame(charts_frame)
lower_frame.pack(fill='both', expand=True)



fig = Figure(figsize = (5, 5), dpi = 100) 
y = [i**2 for i in range(101)] 
plot1 = fig.add_subplot(111) 
plot1.plot(y) 
canvas = FigureCanvasTkAgg(fig, lower_frame)


canvas.draw()
canvas.get_tk_widget().pack(side='left')

fig2 = plt.figure()
canvas2= FigureCanvasTkAgg(fig2, lower_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", expand=True)





# plot_button.pack() 


window.mainloop() 
