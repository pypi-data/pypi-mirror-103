import numpy as np
from multiprocessing import Process, Queue, Pool
import time, multiprocessing
from enum import Enum



class Indvdl(dict):
    def __init__(self):
        self.__fitness = None
        self.__evaltime :float = None

    def __set_prop_fitness(self, value):
        if value == None:
            self.evaltime = None
        self.__fitness = value
    def __get_prop_fitness(self):
        return self.__fitness
    fitness = property(fset=__set_prop_fitness, fget=__get_prop_fitness)

    def __set_prop_evaltime(self,value):
        if type(value) is not float and type(value) != type(None):
            raise ValueError("Value of evaltime must be float or None.")
        self.__evaltime = value
    def __get_prop_evaltime(self):
        return self.__evaltime
    evaltime = property(fset=__set_prop_evaltime, fget=__get_prop_evaltime)

class TaskType(Enum):
    MIN = "MIN"
    MAX = "MAX"
    LIM = "LIM"

def minmaxlimstopf(self, statslog=None):
    if self.task_type == TaskType.MIN:
        iswhile = (self.get_fitnesses() <= self.fitness_target).any()
        if iswhile:
            return True
    elif self.task_type == TaskType.MAX:
        iswhile = (self.get_fitnesses() >= self.fitness_target).any()
        if iswhile:
            return True
    elif self.task_type == TaskType.LIM:
        iswhile = (np.abs(self.get_fitnesses() - np.abs(self.fitness_target)) <= self.max_deviation).any()
        if iswhile:
            return True

    return False

class Population(list):
    def __init__(self, description, evaluate, stopf=minmaxlimstopf, task_type = TaskType.MAX, fitness_target:float = 1, max_deviation:float=None):

        """
        Population of individuals.
        Arguments:
        :description = <dict>. 
            Template for example. description = {<str or int>:{"quantity":<list of ints>, "values":[<list>,<list>]}, ... ,<str or int>:{"quantity":<list of ints>, "values":[<list>,<list>,<list>]}}
        :evaluate = <def>. 
            Function for calculating fitness. The function should return <int>.
        :task_type = TaskType.MIN or TaskType.MAX or TaskType.LIM. 
            Type of task of the evolutionary algorithm..
        :fitness_target = <float>. 
            Target fitness that the evolutionary algorithm is trying to achieve.
        :max_deviation = <float>
            The permissible deviation of fitness. Only used when task_type = TaskType.LIM.
        :istop = <def>
            The argument takes a function defining the stopping condition of the algorithm. The function must return False to continue the algorithm or True to stop the algorithm.
        """

        if task_type != TaskType.MIN and task_type != TaskType.MAX and task_type != TaskType.LIM:
            raise ValueError("task_type != TaskType.MIN and TaskType.MAX and TaskType.LIM")
        if task_type != TaskType.LIM and max_deviation != None:
            raise ValueError("max_devation used only when task_type=TaskType.LIM.")

        self.task_type = task_type
        self.description :dict = description
        self.fitness_target :float = fitness_target
        self.max_deviation = max_deviation

        self.stopf = stopf #def
        self.evaluate  = evaluate # def

    def isstop(self, statslog=None):
        return self.stopf(self=self, statslog=statslog)

    def run_evaluate(self) -> list:
        """
        Run calculate of evaluate each individuals.
        Arguments:
        Return:
        :<list>
            List of fitnesses.
        """
        for indvdl in self:
            if indvdl.fitness == None:
                eval_strt = time.time()
                indvdl.fitness = self.evaluate(indvdl)
                indvdl.evaltime = time.time() - eval_strt
        return [ indvdl.fitness for indvdl in self ]

    def get_fitnesses(self) -> list:
        """
        Get fitness of all individuals.
        Return:
            list of fitness.
        """
        return np.array([ indvdl.fitness for indvdl in self ])

    def get_evaltimes(self) -> list:
        """
        Get evaltime of all individuals.
        Return:
        :<list>
            List of evaltime.
        """
        return [ indvdl.evaltime for indvdl in self ]

    def pure_fitnesses(self):
        """
        Pure fitness of all individuals.
        """
        for indvdl in self:
            indvdl.fitness = None
    
    def pure_evaltimes(self):
        """
        Pure evaltime of all individuals.
        """
        for indvdl in self:
            indvdl.evaltime = None

    def best_indvdls(self) -> list:
        """
        Returns a list of individuals with fitness in the interval fitness_target-max_deviation <= fitness <= fitness_target+max_deviation.
        Return:
        :<list>
        """
        if self.task_type == TaskType.MIN:
            return [ indvdl for indvdl in self if indvdl.fitness == min(self.get_fitnesses()) ]
        elif self.task_type == TaskType.MAX:
            return [ indvdl for indvdl in self if indvdl.fitness == max(self.get_fitnesses()) ]
        elif self.task_type == TaskType.LIM:
            best_indvdls = []
            for indvdl in self:
                if ((self.fitness_target-self.max_deviation) <= indvdl.fitness) and ((self.fitness_target+self.max_deviation) >= indvdl.fitness):
                   best_indvdls.append(indvdl)
            return best_indvdls