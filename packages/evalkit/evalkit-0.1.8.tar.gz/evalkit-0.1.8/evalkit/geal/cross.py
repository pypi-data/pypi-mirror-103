import numpy as np
import copy



def crosOnePoint(indvdl1, indvdl2, docopy = True):
    if docopy:
        indvdl1 = copy.deepcopy(indvdl1)
        indvdl2 = copy.deepcopy(indvdl2)
    keys = indvdl1.keys()
    for key in keys:
        if len(indvdl1[key]) > len(indvdl2[key]):
            crsvr_point = np.random.randint( len(indvdl1[key]) )
        else:
            crsvr_point = np.random.randint( len(indvdl1[key]) )

        tmp_arrays = indvdl1[key][:crsvr_point+1]
        indvdl1[key][:crsvr_point+1] = indvdl2[key][:crsvr_point+1]
        indvdl2[key][:crsvr_point+1] = tmp_arrays

    indvdl1.fitness = None
    indvdl2.fitness = None
    return [indvdl1, indvdl2]