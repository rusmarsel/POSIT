import numpy as np
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

    # Priprava "kanvasa" z drsniki - ideja je, da izberemo točke v pravem vrstnem redu (po trije sprednji robovi zgoraj od leve proti desni in spodaj od leve proti desni)
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

    # Tukaj dodamo skalirano sliko - izberemo med datotekami, ki so na voljo
    File = filedialog.askopenfilename(parent=root, initialdir="E:\Dokumenti\Faks\2018-2019\Robotski vid\POSIT\POSIT",title='Choose an image.')
    img = imt.PhotoImage(im.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    # Funkcija, ki čaka na klik miške
    canvasPoints = []
    def printcoords(event):
        # Dodajanje koordinat na sliki - koordinate služijo kot vhod algoritmu POSIT
        canvasPoints.append((event.x,event.y))
        x1, y1 = (event.x - 10), (event.y - 10)
        x2, y2 = (event.x + 10), (event.y + 10)
        canvas.create_oval(x1, y1, x2, y2, fill=python_green)
    
    # "Mouse-click event"
    python_green = "#476042"
    canvas.bind("<Button 1>",printcoords)
    
    
    root.mainloop()

dolz = len(canvasPoints)

pointsFile = open('pointsFile.csv','w+')

for i in range(dolz):
    pointsFile.write("%d," %canvasPoints[i][0])
    pointsFile.write("%d\r" %canvasPoints[i][1])
    #if (i < (dolz-1)):
    #    pointsFile.write("\n")

pointsFile.close()

# Goriščna razdalja leče fotoaparata v pikslih
focLen = 5
sensW = 6.13
picW = 1000
focLength = np.round((focLen/sensW)*picW)

# Začetni parametri
converged = False
count = 0

# Definicija uporabljenih vektorjev:
imagePointsList = []
objectPointsList = []
objectVectors = []

# Podatki so podani v CSV datotekah: 
f = open('objectPoints.csv')
csv_f = csv.reader(f)
for row in csv_f:
    objectPointsList.append(row)
f.close()

f = open('pointsFile.csv')
csv_f = csv.reader(f)
for row in csv_f:
    imagePointsList.append(np.asarray(row))
f.close()

objectPoints = [[float(num) for num in sub] for sub in objectPointsList]
imagePoints = [[float(num) for num in sub] for sub in imagePointsList]

# Object Points
objectPoints = np.asarray(objectPoints)
imagePoints = np.asarray(imagePoints)
obMatrixPoints = np.linalg.pinv(objectPoints)
csize = len(imagePoints)

# Točke SOP (scaled ortographic projection)
oldSOPImagePoints = imagePoints

# OBJECT POINTS
for i in range(csize):
    objectVectors.append(objectPoints[i] - objectPoints[0])

imTrans = np.transpose(imagePoints)

def shift(key, array):
    a = dq(array)       # turn list into deque
    a.rotate(key)       # rotate deque by key
    return list(a) 

# Image vectors
imageVectors = []
for i in range(csize):
    imageVectors.append(imagePoints[i] - imagePoints[0])

while (~converged):
    # Enotski vektorji
    IVect = []
    JVect = []
    [IVect, JVect] = np.transpose(np.matmul(obMatrixPoints, imageVectors))

    ISquare = np.matmul(IVect, IVect)
    JSquare = np.matmul(JVect, JVect)
    IJ = np.matmul(IVect, JVect)

    [scale1, scale2] = np.sqrt([ISquare, JSquare])
    [row1, row2] = [IVect/scale1, JVect/scale2]

    row1 = np.asarray(row1)
    row2 = np.asarray(row2)
    row3 = np.asarray(shift(-1, row1))*np.asarray(shift(1,row2)) - np.asarray(shift(-1, row2))*np.asarray(shift(1,row1))

    # Izračun rotacije
    rotation = []
    rotation.append(row1)
    rotation.append(row2)
    rotation.append(row3)
    rotation = np.asarray(rotation)

    scale = (scale1 + scale2)/2

    # Izračun translacije
    translation = []
    translation.append(imagePoints[0][0])
    translation.append(imagePoints[0][1])
    translation.append(focLength)

    translation = translation/scale
    translation = np.asarray(translation)

    objectVectors = np.asarray(objectVectors)
    SOPImagePointsCalc = np.matmul(objectVectors, row3)/translation[2] + 1 

    result = np.multiply(imTrans, SOPImagePointsCalc)

    # Izpis novih SOP točk
    SOPImagePoints = []
    for i in range(csize):
        SOPImagePoints.append((result[0][i],result[1][i]))

    SOPImagePoints = np.asarray(SOPImagePoints)
    imageDifference = np.sum(np.abs(np.round(np.ndarray.flatten(SOPImagePoints)) - np.round(np.ndarray.flatten(oldSOPImagePoints))))

    oldSOPImagePoints = SOPImagePoints

    # Image vectors
    imageVectors = []
    for i in range(csize):
        imageVectors.append(SOPImagePoints[i] - SOPImagePoints[0])

    print(imageDifference)
               
    count = count + 1

    converged = (count > 0) & (imageDifference < 1)

print(rotation, translation)

