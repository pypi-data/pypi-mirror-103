import copy
import numpy as np
from evalkit.geal.inits import initRandom
from evalkit.geal.cross import crosOnePoint
from evalkit.geal.muts import mutRand
from evalkit.geal.sels import selTournament
from evalkit.tools.statslog import StatsLog
from evalkit.basic import TaskType


def randwhilefalse(initial_pop, sel_size, tour_size, cros_size, mut_size, statslog=None):
    """
    Generates new generations using randomness until the target fitness value is reached.
    Arguments:
    :initial_pop = <Population>
        Initial population.
    :sel_size = <int>
        The size of the selected individuals.
    :tour_size = <int>
        Tournament size during selection.
    :cros_size = <int>
        The number of crossing pairs.
    :mut_size = <int>
        The number of mutating individuals.
    :statslog = <StatsLog>
        Instance <StatsLog> for calculating statistical information and logs based on this information.
    :prcss = False or <int> or "auto"
        Defines the number of processes for calculating parallel fitness calculations. 
        If False, it is calculated using a single process. 
        If <int>, then with multiple processes. 
        If "auto", the number of processes on your device is determined and all found processes on the device are used.
    Return:
    :<Population>
        A population with an individual that has the best fitness.
    """

    if type(statslog) == StatsLog:
        print(statslog.headers)

    initial_pop.run_evaluate()

    if type(statslog) == StatsLog:
        print(statslog.write(initial_pop))

    #check
    if initial_pop.isstop(statslog=statslog):
        return initial_pop  


    new_pop = copy.deepcopy(initial_pop)
    new_pop.clear()

    while True:

        #selection
        for indvdls in np.random.choice(initial_pop, size=(sel_size, tour_size), replace=False):
            sel_indvdl = selTournament(indvdls, initial_pop.fitness_target, initial_pop.task_type )
            new_pop += sel_indvdl 

        #crossover
        for indvdl1, indvdl2 in np.random.choice(initial_pop, size=(cros_size,2), replace=False):
            cros_indvls = crosOnePoint( indvdl1, indvdl2 )
            new_pop += cros_indvls

        mutation_indxs = np.random.choice(range(len(new_pop)), size=mut_size, replace=False)
        #mutation
        for indx in mutation_indxs:
            mutRand(new_pop[indx], initial_pop.description, docopy=False)


        initial_pop = copy.deepcopy(new_pop)
        new_pop.clear()
        initial_pop.run_evaluate()


        if type(statslog) == StatsLog:
            print(statslog.write(initial_pop))

        #check
        if initial_pop.isstop(statslog=statslog):
            return initial_pop  



def randngen(initial_pop, ngen, sel_size, tour_size, cros_size, mut_size, statslog=None):
    """
        :prcss = False or <int> or "auto"
    """

    if type(statslog) == StatsLog:
        print(statslog.headers)

    initial_pop.run_evaluate()

    #check
    if initial_pop.isstop(statslog=statslog):
        return initial_pop  

    new_pop = copy.deepcopy(initial_pop)
    new_pop.clear()

    for n in range(ngen-1):

        #selection
        for indvdls in np.random.choice(initial_pop, size=(sel_size, tour_size), replace=False):
            sel_indvdl = selTournament(indvdls, initial_pop.fitness_target, initial_pop.task_type )
            new_pop += sel_indvdl 

        #crossover
        for indvdl1, indvdl2 in np.random.choice(initial_pop, size=(cros_size,2), replace=False):
            cros_indvls = crosOnePoint( indvdl1, indvdl2 )
            new_pop += cros_indvls

        mutation_indxs = np.random.choice(range(len(new_pop)), size=mut_size, replace=False)
        #mutation
        for indx in mutation_indxs:
            mutRand(new_pop[indx], initial_pop.description, docopy=False)


        initial_pop = copy.deepcopy(new_pop)
        new_pop.clear()
        initial_pop.run_evaluate()


        if type(statslog) == StatsLog:
            print(statslog.write(initial_pop))

        #check
        if initial_pop.isstop(statslog=statslog):
            return initial_pop   
            
    return initial_pop   