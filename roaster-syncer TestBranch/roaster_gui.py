## create a gui for reviewing status of upload ##
import tkinter as tk
from tkinter import StringVar
from tkinter import *

root = tk.Tk()

frame = tk.Canvas(root, width=300, height=150)
frame.pack()
#report = tk.Label(text="Hello, world!")
report_print = StringVar()
report_print.set("put this in the middle!")
update = Label(root, textvariable=report_print).pack()
report_print.set("middle Text!")
frame.create_window(0, 0, window=update)


def run():
    google_init()
    files = get_roaster_files()
    print('These files are downloaded:')
    reportData = ('These files are downloaded:')
    for element in files:
        reportData = (reportData + "\n" + str(element))
    #reportData = (files + '\n These files are downloaded:')
    report_print.set(str(report_print.get()) + str(reportData))
    print(files)


buttonExit = tk.Button(root, text='Exit Application', command=root.destroy)
buttonRun = tk.Button(root, text='Run', command=run)
frame.create_window(175, 10, window=buttonExit)
frame.create_window(40, 10, window=buttonRun)


def callback(event):
    print("clicked at", event.x, event.y)
    report_print.set("clicked at\n" + str(event.x) + str(event.y))
    frame.create_window(10, 10, window=report)
    frame.create_window(15, 10, window=buttonExit)

frame.bind("<Button-1>", callback)
frame.bind("<Button-2>", callback)


reporttext = StringVar()
reporttext.set("report Text!")
report = Label(root, textvariable=reporttext).pack()
frame.create_window(0, 0, window=report)
reporttext.set("more report Text!")


frame.pack()
root.mainloop()
