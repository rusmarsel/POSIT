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

imagePointsList = []

f = open('pointsFile.csv')
csv_f = csv.reader(f)
for row in csv_f:
    imagePointsList.append(np.asarray(row))
f.close()

imagePoints = [[float(num) for num in sub] for sub in imagePointsList]

print(imagePoints)