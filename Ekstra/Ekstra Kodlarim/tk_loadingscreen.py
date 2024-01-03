import tkinter as tk
import tkinter.ttk as ttk

ws=tk.Tk()
Progress_Bar=ttk.Progressbar(ws,orient=tk.HORIZONTAL,length=250,mode='determinate')

def Slide():
    import time
    Progress_Bar['value']=20
    ws.update_idletasks()
    time.sleep(1)
    Progress_Bar['value']=50
    ws.update_idletasks()
    time.sleep(1)
    Progress_Bar['value']=80
    ws.update_idletasks()
    time.sleep(1)
    Progress_Bar['value']=100

Progress_Bar.pack()
tk.Button(ws,text='Run',command=Slide).pack(pady=10)
tk.mainloop()


