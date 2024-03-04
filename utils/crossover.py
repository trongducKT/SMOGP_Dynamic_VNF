import numpy as np
from copy import deepcopy
from .function_operator import *

def __crossover_branch_individual_swap(individual, donor,min_height,  max_height):
    part_crossover = np.random.rand()
    # determining tree crossover
    if part_crossover < 1 / 3:
        o1 = crossover_tree_branch_swap(individual.determining_tree, donor.determining_tree, max_height)
        height1 = o1.GetHeight()
        if min_height <= height1 <= max_height:
            return Individual(o1, individual.choosing_tree)
    # choosing tree crossover
    elif part_crossover > 2 / 3:
        o1 = crossover_tree_branch_swap(individual.choosing_tree, donor.choosing_tree, max_height)
        height2 = o1.GetHeight()
        if min_height <= height2 <= max_height:
            return Individual(individual.determining_tree, o1)
    # both trees crossover
    else:
        o1 = crossover_tree_branch_swap(individual.determining_tree, donor.determining_tree, max_height)
        height1 = o1.GetHeight()
        if min_height <= height1 <= max_height:
            o2 = crossover_tree_branch_swap(individual.choosing_tree, donor.choosing_tree, max_height)
            height2 = o2.GetHeight()
            if min_height <= height2 <= max_height:
                return Individual(o1, o2)
    return individual

def crossover_branch_individual_swap(individual1, individual2, min_height, max_height):
    child1 = __crossover_branch_individual_swap(individual1, individual2, min_height, max_height)
    child2 = __crossover_branch_individual_swap(individual2, individual1, min_height, max_height)
    return child1, child2