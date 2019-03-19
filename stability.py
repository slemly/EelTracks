# calculating data set stability
# @Samuel Lemly, @slemly
# Undergraduate Research for Martin Cenek, Ph.D
# Begun 17 MAR 2019
#

from stability_funcs import *


def main():
        file_name = sys.argv[1]
        data = pd.read_csv(file_name, header=None)
        dimensions = np.shape(data)
        stabilities=[]
        for p in range(0, dimensions[0]):
                id_to_find = data[0][p]
                places=[] # row appearances of value in set of GOBS results
                for i in range(0, dimensions[0]):
                        for k in range(0, dimensions[1]):
                                if id_to_find == data[k][i]:
                                       places.append(i) 
                        i+=2 # avoid columns with data, only need columns with IDs
                stability = calc_stability(places)
                # stabilities.append([stability,id_to_find]) # create array of all stabilities
                stabilities.append([id_to_find, stability]) #creates array of all stabilites, but with swapped columns   
        reshaped = np.reshape(stabilities,(-1, 2))
        reshaped = reshaped[reshaped[:,0].argsort(kind='mergesort')] # sort by eel ID
        generate_heatmap(reshaped)
main()
