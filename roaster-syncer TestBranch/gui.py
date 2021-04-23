import tkinter as tk
from tkinter import StringVar
from tkinter import *
#for image
from PIL import Image
from PIL import ImageTk
import os

root = tk.Tk()

frame = tk.Canvas(root, width=300, height=300)
frame.pack()
#report = tk.Label(text="Hello, world!")
reporttext = StringVar()
reporttext.set("report Text!")
report = Label(root, textvariable=reporttext).pack()
frame.create_window(150, 10, window=report)
reporttext.set("more report Text!")

v = StringVar()
v.set("New Text!")
update = Label(root, textvariable=v).pack()
v.set("Newer Text!")
frame.create_window(150, 10, window=update)	

num = 0

testDFile = {"date":7.1, "roasts":0}
logDates = [testDFile]
# Storing newly made roasts for logs
# Also used to decide which files to upload
def addRoast(inputDate):
	# find day and it's index
	for entry in logDates:
		print(entry)
		if (entry['date'] == inputDate):
			entry['roasts'] = (entry['roasts'] +1)
			return True
	# if no date
	new = {"date":testDFile, "roasts":0}
	logDates.append(new)
	

num = 0

def run():
    # num = num+1
    print(logDates)
    print("clicked!" + str(num))
    v.set("run at" + str(num))

def callback(event):
    addRoast(7.1)
    print(logDates[0]['date'])
    print("clicked at", str(event.x), str(event.y))
    v.set("clicked at\n"+ str(event.x)+ str(event.y))
    # Update the image panel here
    panel.configure(image=img2)
    panel.image = img2
    #
    reporttext.set("reporting clicked at")

# Set base photo options w/ paths here
img1 = PhotoImage(file="img/loading.gif")      
img2 = PhotoImage(file="img/base.gif")   
imageLoad = img1   
# This one creates a background
#frame.create_image(20,20, anchor=NW, image=img1)   

# Sets location for the image slot
imageSlot = Label(root, textvariable=v).pack()
frame.create_window(150, 10, window=imageSlot)	

panel = tk.Label(root, image=imageLoad)
panel.pack(side="bottom", fill="both", expand="yes")

#def callback(e):
    #img2 = ImageTk.PhotoImage(Image.open(path2))
    #panel.configure(image=img2)
    #panel.image = img2

#
#
#img1 = PhotoImage(file="loading.gif")      
#img2 = PhotoImage(file="base.gif")      
#frame.create_image(20,20, anchor=NW, image=img1)   
#def run():
    #print ('yo')    
    #frame.create_image(20,20, anchor=NW, image=img2)   
#

#define buttons
buttonExit = tk.Button(root, text='Exit Application', command=root.destroy)
buttonRun = tk.Button(root, text='Run', command=run)
#place buttons in frame
frame.create_window(150, 275, window=buttonExit)
frame.create_window(150, 100, window=buttonRun)


#frame = Frame(root, width=100, height=100)
frame.bind("<Button-1>", callback)
frame.bind("<Button-2>", callback)
frame.bind("runroastupdate", callback)
#place frame
frame.pack()
root.mainloop()
# root.mainloop()
