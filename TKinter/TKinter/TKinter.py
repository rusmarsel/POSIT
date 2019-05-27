import numpy as np
import cv2 as cv
import csv
import PIL.Image as im
import PIL.ImageTk as imt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque as dq
from tkinter import filedialog
from tkinter import *

if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = filedialog.askopenfilename(parent=root, initialdir="E:\Dokumenti\Faks\2018-2019\Robotski vid\POSIT\POSIT",title='Choose an image.')
    img = imt.PhotoImage(im.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    canvasPoints = []
    def printcoords(event):
        #outputting x and y coords to console
        canvasPoints.append((event.x,event.y))
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()

dolz = len(canvasPoints)

pointsFile = open('pointsFile.csv','w+')

for i in range(dolz):
    pointsFile.write("%d," %canvasPoints[i][0])
    pointsFile.write("%d\r\n" %canvasPoints[i][1])
    #if (i < (dolz-1)):
    #    pointsFile.write("\n")

pointsFile.close()
