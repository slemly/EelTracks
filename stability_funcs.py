import sys
import numpy as np
import pandas as pd
import scipy as sp
import os
import seaborn as sns
import matplotlib.pyplot as plt


def calc_stability(in_array):
    val = in_array[0]
    to_ret = 0
    for i in range(1, len(in_array)):
        to_ret = to_ret+(abs(val - in_array[i]))
    to_ret = to_ret/len(in_array)
    return to_ret

def generate_heatmap(in_array):
    #print(in_array)
    #all_stabils = in_array[:,1] #fetch all stabilities
    
    new_plot = []
    in_array = np.sort(in_array[:,1], axis=-1)
    print(in_array)
    xaxis = in_array
    yaxis = in_array
    # print(in_array)
    for i in range(0,len(in_array)):
        row = []
        for k in range(0, len(in_array)):
            index_val = ((abs(xaxis[i] - yaxis[k])) * 0.1)
            # use this if IDs are also pulled from table and passed in
            #index_val = ((abs(xaxis[i][1] - yaxis[k][1])) * 0.1) 
            row.append(index_val)
        new_plot.append(row)
    
    ax = sns.heatmap(new_plot)
    ax = ax.invert_yaxis()
    plt.show()
    # for i in range(0, xaxis):
    #     for j in range(0, yaxis):
            