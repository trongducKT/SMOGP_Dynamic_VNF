import numpy as np
import random
from numpy.random import randint
from copy import deepcopy
from gp.population.individual import Individual


# Randomly individual initialization
def individual_init(min_height, curr_max_depth, determining_tree,
                    functions, determining_terminals, ordering_terminals, choosing_terminals):
        determining_tree = deepcopy(determining_tree)
        if determining_tree is None:
            determining_tree = GenerateRandomTree(functions, determining_terminals, curr_max_depth, 
                                                curr_height=0, 
                                                method='grow' if np.random.random() < .5 else 'full', 
                                                min_height= min_height )
        ordering_tree = GenerateRandomTree(functions,ordering_terminals, curr_max_depth, 
                                        curr_height=0, 
                                        method='grow' if np.random.random() < .5 else 'full', 
                                        min_height= min_height )
        choosing_tree = GenerateRandomTree(functions,choosing_terminals, curr_max_depth, 
                                            curr_height=0, 
                                            method='grow' if np.random.random() < .5 else 'full', 
                                            min_height= min_height )
        inv = Individual(determining_tree, ordering_tree, choosing_tree)
        return inv

# Randomly population initialization 
def random_population_init(pop_size, min_height, initialization_max_tree_height,
                           determining_tree,
                           functions, determining_terminals, ordering_terminals, choosing_terminals):
    indi_list = []
    curr_max_depth = min_height
    init_depth_interval = pop_size / (initialization_max_tree_height - min_height + 1)
    next_depth_interval = init_depth_interval
    for i in range(pop_size ):
        if i >= next_depth_interval:
            next_depth_interval += init_depth_interval
            curr_max_depth += 1
        inv = individual_init(min_height, curr_max_depth, determining_tree, functions,
                              determining_terminals, ordering_terminals, choosing_terminals)
        indi_list.append(inv)
    return indi_list


def GenerateRandomTree(functions, terminals, max_height, curr_height=0, method='grow', min_height=2):
    if curr_height == max_height:
        idx = randint(len(terminals))
        n = deepcopy( terminals[idx] )
    else:
        if method == 'grow' and curr_height	>= min_height:
            term_n_funs = terminals + functions
            idx = randint( len(term_n_funs) )
            n = deepcopy( term_n_funs[idx] )
        elif method == 'full' or (method == 'grow' and curr_height < min_height):
            idx = randint(len(functions))
            n = deepcopy( functions[idx] )
        else:
            raise ValueError('Unrecognized tree generation method')

        for i in range(n.arity):
            c = GenerateRandomTree(functions, terminals, max_height, curr_height=curr_height + 1, 
                                        method=method, min_height=min_height )
            n.AppendChild( c ) # do not use n.children.append because that won't set the n as parent node of c
    return n