import numpy as np
from ..basic import Indvdl



def initRandom(description, size:int):
    
    indvdls = []
    for _ in range(size):
        indvdl = Indvdl()
        for key in description:
            tmp_list = []
            for _ in range(np.random.choice(description[key]["quantity"])):
                tmp_list.append( [ values_list[np.random.randint(len(values_list))] for values_list in description[key]["values"] ] )
            indvdl[key] = tmp_list
        indvdls.append( indvdl )

    return indvdls