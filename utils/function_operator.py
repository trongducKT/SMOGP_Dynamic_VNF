import numpy as np
import random
from numpy.random import randint
from copy import deepcopy
from .initialization import GenerateRandomTree
import time

# Tree  branch replace mutation
def mutation_tree_branch_replace(tree, functions, terminals, min_height, max_height ):
    
    nodes = tree.GetSubtree()
    nodes, chosen_depth = __GetCandidateNodesAtUniformRandomDepth(nodes, max_height )
    to_replace = nodes[randint(len(nodes))]
    
    if not to_replace.parent:
        mutation_branch = GenerateRandomTree(functions, terminals, max_height, min_height = min_height )
        del tree
        return mutation_branch

    if chosen_depth == max_height:
        mutation_branch = np.random.choice(terminals)
    else:
        mutation_branch = GenerateRandomTree(functions, terminals, max_height - chosen_depth, min_height = 1)
    
    
    p = to_replace.parent
    idx = p.DetachChild(to_replace)
        
    p.InsertChildAtPosition(idx, mutation_branch)
    return tree

# Tree node replace mutation
def mutation_tree_node_replace(tree, functions, terminals, min_height, max_height):
    node_identifier = set()
    for node in functions:
        node_identifier.add(node.getSymbol())
    nodes = tree.GetSubtree()
    random_node = nodes[randint(len(nodes))]
    p = random_node.parent
#     print(random_node, p)
#     time.sleep(2)
    if random_node.getSymbol() in node_identifier:
        temp = functions[randint(len(functions))]
        while temp.getSymbol() == random_node.getSymbol():
            temp = functions[randint(len(functions))]
        replace_node = deepcopy(temp)
        
        child1 = deepcopy(random_node._children[0])
        child2 = deepcopy(random_node._children[1])
        replace_node.AppendChild(child1)
        replace_node.AppendChild(child2)
        if p != None:
            idx = p.DetachChild(random_node)
            p.InsertChildAtPosition(idx, replace_node)
        else:
            del tree
            return replace_node

    else:
        temp = terminals[randint(len(terminals))]
        while temp.getSymbol() == random_node.getSymbol():
            temp = terminals[randint(len(terminals))]
        replace_node = deepcopy(temp)
    
        idx = p.DetachChild(random_node)
        p.InsertChildAtPosition(idx, replace_node)
    return tree


# Tree branch swap mutation
def mutation_tree_branch_swap(tree, functions, terminals, min_height, max_height):
    nodes = tree.GetSubtree()
    random_node = nodes[randint(len(nodes))]
    if random_node._children == []:
        return tree
    child1 = random_node._children[0]
    child2 = random_node._children[1]
    random_node._children[0] = child2
    random_node._children[1] = child1
    return tree


# Tree crossover
def crossover_tree_branch_swap(tree, donor, max_height):
    tree = deepcopy(tree)
    nodes1_subtree = tree.GetSubtree()
    nodes2_subtree = donor.GetSubtree()	# no need to deep copy all nodes of parent2
    nodes1, depth_node1 = __GetCandidateNodesAtUniformRandomDepth( nodes1_subtree, max_height )
    nodes2, depth_node2 = __GetCandidateNodesAtUniformRandomDepth_crossover( nodes2_subtree, max_height - 
                                                                                    depth_node1 )

    while nodes2 == False:
        nodes1, depth_node1 = __GetCandidateNodesAtUniformRandomDepth( nodes1_subtree, max_height )
        nodes2, depth_node2 = __GetCandidateNodesAtUniformRandomDepth_crossover( nodes2_subtree, max_height - 
                                                                                        depth_node1 )
    to_swap1 = nodes1[ randint(len(nodes1)) ]
    to_swap2 = deepcopy( nodes2[ randint(len(nodes2)) ] )
    to_swap2.parent = None

    p1 = to_swap1.parent

    if not p1:
        return to_swap2

    idx = p1.DetachChild(to_swap1)
    p1.InsertChildAtPosition(idx, to_swap2)

    return tree


def __GetCandidateNodesAtUniformRandomDepth(nodes, max_height_thereshold):

    depths_total = np.unique( [x.GetDepth() for x in nodes] )
    depths = []
    for depth in depths_total:
        if depth > 0 and depth <= max_height_thereshold:
            depths.append(depth)
    chosen_depth = depths[randint(len(depths))]
    candidates = [x for x in nodes if x.GetDepth() == chosen_depth]

    return candidates, chosen_depth

def __GetCandidateNodesAtUniformRandomDepth_crossover(nodes, max_height_thereshold):

    heights_total = np.unique( [x.GetHeight() for x in nodes] )
    heights = []
    for height in heights_total:
        if height <= max_height_thereshold:
            heights.append(height)
    if len(heights) == 0:
        return False, False
    chosen_height = heights[randint(len(heights))]
    candidates = [x for x in nodes if x.GetHeight() == chosen_height]

    return candidates, chosen_height

def tournament_selection(pop, remove_position):
    index_list = list(np.arange(len(pop.indivs)))
    if remove_position in index_list:
        index_list.remove(remove_position)
    print("index_list", index_list)
    participants = random.sample(index_list, pop.num_of_tour_particips)
    best = None
    for participant in participants:
        if best is None or (pop.crowding_operator(pop.indivs[participant], pop.indivs[best]) == 1 and 
                            np.random.random() < pop.tournament_prob):
            best = participant
    return best