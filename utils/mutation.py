import numpy as np
from .function_operator import *
from gp.population.individual import Individual

def mutation_individual_branch_replace(individual: Individual, functions, 
                                       terminal_determining, terminal_ordering, terminal_choosing, 
                                       min_height, max_height, determining_tree):
    o1 = deepcopy(determining_tree)
    if o1 is None:
    # determining tree mutation
        o1 = mutation_tree_branch_replace(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.determining_tree)
    
    # ordering tree mutation
    o2 = mutation_tree_branch_replace(individual.ordering_tree, functions, terminal_ordering,
                    min_height, max_height)
    height2 = o2.GetHeight()
    if min_height > height2 or height2 > max_height:
        o2 = deepcopy(individual.ordering_tree)
    # choosing tree mutation
    o3 = mutation_tree_branch_replace(individual.choosing_tree, functions, terminal_choosing,
                    min_height, max_height)
    height3 = o3.GetHeight()
    if min_height > height3 or height3 > max_height:
        o3 = deepcopy(individual.choosing_tree)
    # both trees mutation
    return Individual(o1, o2, o3)

def mutation_individual_node_replace(individual: Individual, functions, 
                                    terminal_determining, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, determining_tree):
    o1 = deepcopy(determining_tree)
    if o1 is None:
        # determining tree mutation
        o1 = mutation_tree_node_replace(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.determining_tree)
    # ordering tree mutation
    o2 = mutation_tree_node_replace(individual.ordering_tree, functions, terminal_ordering,
                    min_height, max_height)
    height2 = o2.GetHeight()
    if min_height > height2 or height2 > max_height:
        o2 = deepcopy(individual.ordering_tree)
    # choosing tree mutation
    o3 = mutation_tree_node_replace(individual.choosing_tree, functions, terminal_choosing,
                    min_height, max_height)
    height3 = o3.GetHeight()
    if min_height > height3 or height3 > max_height:
        o3 = deepcopy(individual.choosing_tree)
    # both trees mutation
    return Individual(o1, o2, o3)


def mutation_individual_branch_swap(individual: Individual, functions, 
                                    terminal_determining, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, determining_tree):
    o1 = deepcopy(determining_tree)
    if o1 is None:
    # determining tree mutation
        o1 = mutation_tree_branch_swap(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height > height1 or height1 > max_height:
            o1 = deepcopy(individual.determining_tree)
    # ordering tree mutation
    o2 = mutation_tree_branch_swap(individual.ordering_tree, functions, terminal_ordering,
                    min_height, max_height)
    height2 = o2.GetHeight()
    if min_height > height2 or height2 > max_height:
        o2 = deepcopy(individual.ordering_tree)
    # choosing tree mutation
    o3 = mutation_tree_branch_swap(individual.choosing_tree, functions, terminal_choosing,
                    min_height, max_height)
    height3 = o3.GetHeight()
    if min_height > height3 or height3 > max_height:
        o3 = deepcopy(individual.choosing_tree)
    # both trees mutation
    return Individual(o1, o2, o3)