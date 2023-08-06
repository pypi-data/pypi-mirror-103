import numpy as np
import copy
from evalkit.basic import TaskType


def selTournament(indvdls, fitness_target, task_type, replace=False):
        if task_type == TaskType.MIN:
            return [ [ indvdl for indvdl in indvdls if indvdl.fitness == min([indvdl.fitness for indvdl in indvdls]) ][0] ]
        elif task_type == TaskType.MAX:
            return [ [ indvdl for indvdl in indvdls if indvdl.fitness == max([indvdl.fitness for indvdl in indvdls]) ][0] ]
        elif task_type == TaskType.LIM:
            fitnesses = np.array([indvdl.fitness for indvdl in indvdls])
            return [ [ indvdl for indvdl in indvdls if np.abs(indvdl.fitness - fitness_target) == min(np.abs(fitnesses - fitness_target)) ][0] ]