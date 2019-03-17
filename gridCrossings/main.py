''' Main for Grid Crossing Generator
    Adrian Low
    Samuel Lemly
    2019 Undergraduate research for Martin Cenek
    Last Updated: 11 MAR 2019
'''

from gridcrossinggenerator import *
numCrossings = 4
numtoextrapolate = 18
errors = []
# eelID = input("Enter file eel's ID number: ")
if os.path.exists(os.getcwd() + "/results"):
    print("Warning: Results directory already exists \n")
else:
    os.mkdir(os.getcwd() + "/results")
for eelID in range(1, 258):
    fpath = os.getcwd()+('/E' + str(eelID)+ '_flocdata_reordered.txt')
    
    # outputFile = input("Please type a name for the output file: ")
    outputFile = os.getcwd() + '/results/'+str(eelID)+'output.txt'
    # numCrossings = int(input("Please enter the number of grid crossings to divide (4-360): "))
    fileLines = []  # variable for storing each line of the file
    if os.path.exists(fpath):
        with open(fpath) as inFile:
            for line in inFile:
                fileLines.append(line) # takes each line and appends to fileLines
        xandys = getCoordinates(fileLines)
        try:
            allPts = np.transpose(xandys)
            # try:
            #     allPts = extrapolatePoints(xandys, numtoextrapolate)
            # except Exception as e:
            #     print("Error in :" + str(eelID) )
            #     print(e)
            #     allPts = extrapolatePointsNonMonotonic(xandys, numtoextrapolate)

            numLines = len(allPts) # get the number of lines
            results = [] # array to store all the results to write to the final file

            for x in range(0, numLines-1):
                startEel = allPts[x]
                endEel = allPts[x+1]
                x1 = startEel[0]
                x2 = endEel[0]
                y1 = startEel[1]
                y2 = endEel[1]
                angle = findAngle(x1, x2, y1, y2)
                gridCrossing = findCrossingNum(angle, numCrossings)
                results.append([x, eelID, gridCrossing])

            resultWriter(outputFile, numCrossings, results)
        except Exception as e:
            print(e)
            print(eelID)
            errors.append(eelID)

reportWriter(numCrossings, errors)
