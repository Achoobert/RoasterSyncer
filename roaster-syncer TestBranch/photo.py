import tkinter as tk
from tkinter import StringVar
from tkinter import *
#for image
from PIL import Image
from PIL import ImageTk
import os

root = tk.Tk()

frame = tk.Canvas(root, width=900, height=300)
frame.pack()
reporttext = StringVar()
report = Label(root, textvariable=reporttext).pack()
frame.create_window(150, 10, window=report)

#

img1 = PhotoImage(file="loading.gif")      
img2 = PhotoImage(file="base.gif")      
frame.create_image(20,20, anchor=NW, image=img1)   

def run():
    print ('yo')    
    frame.create_image(20,20, anchor=NW, image=img2)   

#

#define buttons
buttonExit = tk.Button(root, text='Exit Application', command=root.destroy)
buttonRun = tk.Button(root, text='Run', command=run)
#place buttons in frame
frame.create_window(150, 275, window=buttonExit)
frame.create_window(150, 100, window=buttonRun)


#place frame
frame.pack()
root.mainloop()
# root.mainloop()

