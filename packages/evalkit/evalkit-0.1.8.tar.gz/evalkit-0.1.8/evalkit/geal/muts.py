import numpy as np
import copy



def mutRand(indvdl, description, sel_keys = "all", mut_type="all", docopy=True):
    """
        mut_type: "add" or "del" or "rewrite" or "all" or "rand_once" or "rand_each_indvdl" or "rand_each_key"
        sel_keys: "all" or "rand", "rand_each_indvdl", <<dict key>>, <list>
    """
    indvdl = copy.deepcopy(indvdl) if docopy else indvdl
    count_change = 0
    while count_change == 0:
        mut_type = ["add", "del", "rewrite"] if mut_type is "all" else mut_type
        mut_type = np.random.choice(["add", "del", "rewrite"], size=np.random.randint(1,4)) if mut_type is "rand_once" else mut_type
        mut_type = np.random.choice(["add", "del", "rewrite"], size=np.random.randint(1,4)) if mut_type is "rand_each_indvdl" else mut_type

        if sel_keys == "rand":
            keys = np.random.choice(list(description.keys()), 
                                    size=np.random.randint(1,len(description.keys())+1), 
                                    replace=False)
        elif sel_keys == "all":
            keys = list(description.keys())

        elif sel_keys == "rand_each_indvdl":
            keys = np.random.choice(list(description.keys()), 
                                    size=np.random.randint(1,len(description.keys())+1), 
                                    replace=False)
        
        elif type(sel_keys) == int or type(sel_keys) == str:
            keys = sel_keys

        elif type(sel_keys) == list:
            keys = sel_keys

        for key in keys:
            mut_type = np.random.choice(["add", "del", "rewrite"], size=np.random.randint(1,4)) if mut_type is "rand_each_key" else mut_type
            if "rewrite" in mut_type:
                source_arrays = copy.deepcopy(indvdl[key])
                #if new array have not new values
                while indvdl[key] == source_arrays:

                    for array_indx in np.random.choice( a=range(len(indvdl[key])), 
                                                        size= np.random.randint(1,len(indvdl[key])+1),
                                                        replace=False):
                        indvdl[key][array_indx] = [ values_list[np.random.randint(len(values_list))] for values_list in description[key]["values"] ]
                count_change += 1

            if "add" in mut_type:
                if description[key]["quantity"] != [1]:
                    for _ in range(np.random.choice(description[key]["quantity"])):
                        indvdl[key].append( [ values_list[np.random.randint(len(values_list))] for values_list in description[key]["values"] ] )
                    count_change += 1


            if "del" in mut_type:
                if len(indvdl[key]) != 1:
                    del_array_indxs = np.random.choice( a=range(len(indvdl[key])), 
                                                        size= np.random.randint(1,len(indvdl[key])),
                                                        replace=False)
                    indvdl[key] = [ indvdl[key][indx] for indx in range(len(indvdl[key])) if indx not in del_array_indxs ]
                    count_change += 1


    indvdl.fitness = None
    return [indvdl]