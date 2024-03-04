import numpy as np
from .function_operator import *

def mutation_individual_branch_replace(individual, functions, terminal_determining, 
                                      terminal_choosing, min_height, max_height):

    part_mutation = np.random.rand()
    # determining tree mutation
    if part_mutation < 1 / 3:
        o = mutation_tree_branch_replace(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o.GetHeight()
        if min_height <= height1 <= max_height:
            return Individual(o, individual.choosing_tree)
    # choosing tree mutation
    elif part_mutation > 2 / 3:
        o = mutation_tree_branch_replace(individual.choosing_tree, functions, terminal_choosing,
                        min_height, max_height)
        height2 = o.GetHeight()
        if min_height <= height2 <= max_height:
            return Individual(individual.determining_tree, o)
    # both trees mutation
    else:
        o1 = mutation_tree_branch_replace(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height <= height1 <= max_height:
            o2 = mutation_tree_branch_replace(individual.choosing_tree, functions, terminal_choosing,
                            min_height, max_height)
            height2 = o2.GetHeight()
            if min_height <= height2 <= max_height:
                return Individual(o1, o2)
    return individual

def mutation_individual_node_replace(individual, functions, terminal_determining, 
                                      terminal_choosing, min_height, max_height):
    part_mutation = np.random.rand()
    # determining tree mutation
    if part_mutation < 1 / 3:
        o = mutation_tree_node_replace(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o.GetHeight()
        if min_height <= height1 <= max_height:
            return Individual(o, individual.choosing_tree)
    # choosing tree mutation
    elif part_mutation > 2 / 3:
        o = mutation_tree_node_replace(individual.choosing_tree, functions, terminal_choosing,
                        min_height, max_height)
        height2 = o.GetHeight()
        if min_height <= height2 <= max_height:
            return Individual(individual.determining_tree, o)
    # both trees mutation
    else:
        o1 = mutation_tree_node_replace(individual.determining_tree, functions, terminal_determining,
                        min_height, max_height)
        height1 = o1.GetHeight()
        if min_height <= height1 <= max_height:
            o2 = mutation_tree_node_replace(individual.choosing_tree, functions, terminal_choosing,
                            min_height, max_height)
            height2 = o2.GetHeight()
            if min_height <= height2 <= max_height:
                return Individual(o1, o2)
    return individual