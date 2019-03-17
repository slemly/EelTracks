# eel data parser
# @Samuel Lemly, @slemly
# Undergraduate Research for Martin Cenek, Ph.D
# Begun 3 FEB 2019
#

import sys
import os
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from scipy import ndimage


# TODO: Add time, id, x, and y for GOBS to read
# TODO: Time and id are pulled file

def main():
    path = os.path.join(os.getcwd(),'data') #data')
    fig = plt.figure()
    fig.set_size_inches(35.5,22)
    cntBadFiles = 0;
    for i, file in enumerate(os.listdir(path),1):
        current = os.path.join(path, file)
        print(current)
        if os.path.isfile(current):
            data = pd.read_csv(current, delimiter='\t', header=None)
            rows = data.shape[0]  # get num of rows
            cols = data.shape[1]  # get num of cols
            data = data.values  # convert data to floats
            # print data
            X = data[:, 3]  # to get all rows by only the second column
            Y = data[:, 4]  # to get all rows by only the first column
            Z = data[:, 1]  # Getting all timestamps
            X = np.transpose(np.float64(X));
            Y = np.transpose(np.float64(Y));
            out=[];
            #print(X)
            try: #try tail
                tck, u, = splprep([X, Y], u=None, s=0.0) # fp, ier, msg
                unew = np.linspace(u.min(), u.max(), rows*100)
                out = splev(unew, tck)
            except:
                try: #try center
                    X = data[:, 5]  # to get all rows by only the second column
                    Y = data[:, 6]  # to get all rows by only the first column
                    X = np.transpose(np.float64(X));
                    Y = np.transpose(np.float64(Y));
                    tck, u, = splprep([X, Y], u=None, s=0.0) # fp, ier, msg
                    unew = np.linspace(u.min(), u.max(), rows*100)
                    out = splev(unew, tck)
                except:
                    try: #try head
                        X = data[:, 7]  # to get all rows by only the second column
                        Y = data[:, 8]  # to get all rows by only the first column
                        X = np.transpose(np.float64(X));
                        Y = np.transpose(np.float64(Y));
                        tck, u, = splprep([X, Y], u=None, s=0.0) # fp, ier, msg
                        unew = np.linspace(u.min(), u.max(), rows*100)
                        out = splev(unew, tck)
                    except: 
                        print('all failed');
                        cntBadFiles += 1
            if len(out)>0:
                plt.subplot(31,8,i - cntBadFiles)
                #plt.plot(X, Y, 'ro')
                plt.plot(out[0], out[1], 'r-')
                eel_name = str(file.split('_')[0])
                plt.legend([eel_name])
                plt.axis([12.5, 17, -1, 1])
                X = np.transpose(out[0]);
                Y = np.transpose(np.add(out[1], 1.5));
                fn = open("output/"+str(file),'w');
                for i, tpl in enumerate(zip(X,Y),1):
                    fn.write("%s\t%d\t%f\t%f\n"%(file.split('_')[0],i,tpl[0],tpl[1]));
                fn.close;
            data=[];
    plt.subplots_adjust(0.1, 0.1, 0.9, 0.9, 0.1, 0.4)
    plt.savefig('EEL_tracks.png')
main()
