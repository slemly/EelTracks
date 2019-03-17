''' Grid Crossing Generator
    Adrian Low
    Samuel Lemly
    2019 Undergraduate research for Martin Cenek
    Last updated: 11 MAR 2019
'''

from math import atan2, degrees
import os
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy.interpolate import splprep, splev

def findAngle(x1, x2, y1, y2):
    '''Returns the angle an eel is heading from t1 to t2'''
    xDif = x2 - x1
    yDif = y2 - y1
    calcAngle = degrees(atan2(yDif, xDif))
    if calcAngle < 0:
        return calcAngle + 360
    else:
        return calcAngle

def findCrossingNum(angleFound, num_crossings):
    '''Returns the crossing number'''
    crossing_angle = 360.0 / float(num_crossings)
    count = 1
    while count <= num_crossings:
        temp = count * crossing_angle
        if angleFound <= temp:
            break;
        else:
            count+=1
    return count

def lineParser(line):
    '''Returns a list of relevant data from the line of an eel file'''
    temp = []
    lineNoWS = line.split() #removes whitespace from lines
    # temp.append(lineNoWS[1]) #time
    temp.append(float(lineNoWS[2])) #center x position
    temp.append(float(lineNoWS[3])) #c enter y position
    return temp

def getCoordinates(data):
    eel_x_pos = []
    eel_y_pos = []
    for i in range(0, len(data)):
        parsedData = lineParser(data[i])
        eel_x_pos.append(parsedData[0])
        eel_y_pos.append(parsedData[1])
    return [eel_x_pos, eel_y_pos]

def plotEelWithSpline(eelcoordinates, numPts):
    '''Generates graph of eel with the extrapolated points'''
    f = interpolate.interp1d(eelcoordinates[0], eelcoordinates[1], kind='cubic')
    for pt in range(len(eelcoordinates[0])-1):
        new_xs = np.linspace(eelcoordinates[0][pt], eelcoordinates[0][pt+1], numPts)
        new_ys = f(new_xs)
        plt.plot(new_xs, new_ys, 'bo')
    plt.plot(eelcoordinates[0], eelcoordinates[1], 'ro')
    plt.show()
    return

def plotSplineNonMonotonic(eelcoordinates, numPts):
    tck, u = splprep([eelcoordinates[0], eelcoordinates[1]], u=None, s=0.0)
    unew = np.linspace(u.min(), u.max(), numPts)
    out = splev(unew, tck)

    fig, ax = plt.subplots()
    ax.plot(out[0], out[1], 'r-')
    print(out[0])
    #ax.plot(out[0], out[1], 'ro')
    ax.plot(eelcoordinates[0], eelcoordinates[1], 'bo')
    plt.legend(['Cubic Spline'])
    plt.show()

def extrapolatePointsNonMonotonic(eelcoordinates, numPts):
    points = []
    tck, u = splprep([eelcoordinates[0], eelcoordinates[1]], u=None, s=0.0)
    unew = np.linspace(u.min(), u.max(), numPts)
    out = splev(unew, tck)
    for x in range(len(out[0])):
        points.append([out[0][x], out[1][x]])
    return points

def extrapolatePoints(eelcoordinates, numPts):
    points = []
    f = interpolate.interp1d(eelcoordinates[0], eelcoordinates[1], kind = 'cubic')
    for pt in range(len(eelcoordinates[0])-1):
        new_xs = np.linspace(eelcoordinates[0][pt], eelcoordinates[0][pt+1], numPts)
        new_ys = f(new_xs)
        if pt > 0:
            for j in range(1, len(new_xs)):
                points.append([new_xs[j], new_ys[j]])
        else:
            for j in range(len(new_xs)):
                points.append([new_xs[j], new_ys[j]])
    return points

def resultWriter(out_file, num_crossings, results):
    anglePerCrossing = 360.0 / float(num_crossings)
    if os.path.exists(out_file):
        key = 'a' #append if the file is already created
    else:
        key = 'w' #write a new file
    outFile = open(out_file, key)
    for tup in results:
        outFile.write(str(tup) + "\n")
    outFile.close()

def reportWriter(num_crossings, failedfiles):
    outFile = open("report.txt", 'w')
    crossing_angle = 360.0 / float(num_crossings)
    outFile.write("Crossing Numbers = { ")
    for x in range(num_crossings):
        outFile.write(str(x+1) + ": " + str(crossing_angle * x) + " - " + str(crossing_angle * (x+1)) + ", ")
    outFile.write(" } \n")
    for fnum in failedfiles:
        outFile.write("Error in file E" + str(fnum) + "_flocdata_reordered.txt \n")
    outFile.close()

def test(eelnumber):
    '''creates a test situation for a given file number'''
    numCrossings = 4
    numtoextrapolate = 18
    fpath = 'E' + str(eelnumber)+ '_flocdata_reordered.txt'
    fileLines = []
    with open(fpath) as inFile:
        for line in inFile:
            fileLines.append(line)
    xandys = getCoordinates(fileLines)
    plotSplineNonMonotonic(xandys, numtoextrapolate)
    try:
        allPts = extrapolatePoints(xandys, numtoextrapolate)
    except ValueError:
        allPts = extrapolatePointsNonMonotonic(xandys, numtoextrapolate)
    print(allPts)
