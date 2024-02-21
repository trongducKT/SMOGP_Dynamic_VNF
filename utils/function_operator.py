import numpy as np
import random
from numpy.random import randint
from copy import deepcopy
from gp.population.individual import Individual

# Fast Non-dominated Sort
def fast_nondominated_sort(pop):
    pop.ParetoFront = [[]]
    for individual in pop.indivs:
        individual.domination_count = 0
        individual.dominated_solutions = []
        for other_individual in pop.indivs:
            if individual.dominates(other_individual):
                individual.dominated_solutions.append(other_individual)
            elif other_individual.dominates(individual):
                individual.domination_count += 1
        if individual.domination_count == 0:
            individual.rank = 0
            pop.ParetoFront[0].append(individual)
    i = 0
    while len(pop.ParetoFront[i]) > 0:
        temp = []
        for individual in pop.ParetoFront[i]:
            for other_individual in individual.dominated_solutions:
                other_individual.domination_count -= 1
                if other_individual.domination_count == 0:
                    other_individual.rank = i + 1
                    temp.append(other_individual)
        i = i + 1
        pop.ParetoFront.append(temp)


def calculate_crowding_distance(front):
    if len(front) > 0:
        solutions_num = len(front)
        for individual in front:
            individual.crowding_distance = 0

        for m in range(len(front[0].objectives)):
            front.sort(key=lambda individual: individual.objectives[m])
            front[0].crowding_distance = 10 ** 9
            front[solutions_num - 1].crowding_distance = 10 ** 9
            m_values = [individual.objectives[m] for individual in front]
            scale = max(m_values) - min(m_values)
            if scale == 0: scale = 1
            for i in range(1, solutions_num - 1):
                front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale

# Crowding Operator
def crowding_operator( individual, other_individual):
    if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (
                    individual.crowding_distance > other_individual.crowding_distance)):
        return 1
    else:
        return -1
    
# Random Initialization  
def random_init(pop):
    curr_max_depth = pop.min_height
    init_depth_interval = pop.pop_size / (pop.initialization_max_tree_height - pop.min_height + 1)
    next_depth_interval = init_depth_interval
    for i in range( pop.pop_size ):
        if i >= next_depth_interval:
            next_depth_interval += init_depth_interval
            curr_max_depth += 1
        determining_tree = GenerateRandomTree( pop.functions, pop.determining_terminals, curr_max_depth, 
                                                    curr_height=0, 
            method='grow' if np.random.random() < .5 else 'full', min_height=pop.min_height )
        choosing_tree = GenerateRandomTree( pop.functions, pop.choosing_terminals, curr_max_depth, 
                                                curr_height=0, 
            method='grow' if np.random.random() < .5 else 'full', min_height=pop.min_height )
        inv = Individual(determining_tree, choosing_tree)
        pop.indivs.append(inv)


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

def mutation(individual,functions, terminals, min_height, max_height ):
    
    nodes = individual.GetSubtree()
    nodes, chosen_depth = __GetCandidateNodesAtUniformRandomDepth(nodes, max_height )
    to_replace = nodes[randint(len(nodes))]
    
    if not to_replace.parent:
        mutation_branch = GenerateRandomTree(functions, terminals, max_height, min_height = min_height )
        del individual
        return mutation_branch

    if chosen_depth == max_height:
        mutation_branch = np.random.choice(terminals)
    else:
        mutation_branch = GenerateRandomTree(functions, terminals, max_height - chosen_depth, min_height = 1)
    
    
    p = to_replace.parent
    idx = p.DetachChild(to_replace)
        
    p.InsertChildAtPosition(idx, mutation_branch)
    return individual


def crossover(individual, donor, max_height):
    individual = deepcopy(individual)
    nodes1_subtree = individual.GetSubtree()
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

    return individual


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

def reproduction(pop):
    print(pop.min_height, pop.max_height)
    O = []
    for _ in range( pop.pop_size ):
        # individual1_index = self.tournament_selection(-1)
        # individual2_index = self.tournament_selection(individual1_index)

        # individual1 = deepcopy(self.indivs[individual1_index])
        # individual2 = deepcopy(self.indivs[individual2_index])
        individual1, individual2 = random.sample(pop.indivs, 2)
        
        SD = np.linalg.norm(individual1.objectives - individual2.objectives)
        print("SD", SD)
        # crossover
        # if ( np.random.rand() < self.crossover_rate ):
        if ( SD > 0.1 ):
            part_crossover = np.random.rand()
            # determining tree crossover
            if part_crossover < 1/3:
                o1 = crossover(individual1.determining_tree, individual2.determining_tree, pop.max_height)
                height1 = o1.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    O.append(Individual(o1, individual1.choosing_tree))
            # choosing tree crossover
            elif part_crossover > 2/3:
                o1 = crossover(individual1.choosing_tree, individual2.choosing_tree, pop.max_height)
                height2 = o1.GetHeight()
                if height2 >= pop.min_height and height2 <= pop.max_height:
                    O.append(Individual(individual1.determining_tree, o1))
            # both trees crossover
            else:
                o1 = crossover(individual1.determining_tree, individual2.determining_tree, pop.max_height)
                height1 = o1.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    o2 = crossover(individual1.choosing_tree, individual2.choosing_tree, pop.max_height)
                    height2 = o2.GetHeight()
                    if height2 >= pop.min_height and height2 <= pop.max_height:
                        O.append(Individual(o1, o2))

        # mutation
        # if ( np.random.rand() < self.mutation_rate ):
        if ( SD < 0.1 ):
            part_mutation = np.random.rand()
            # determining tree mutation
            if part_mutation < 1/3:
                o = mutation(individual1.determining_tree, pop.functions, pop.determining_terminals, pop.min_height, pop.max_height)
                height1 = o.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    O.append(Individual(o, individual1.choosing_tree))
            # choosing tree mutation
            elif part_mutation > 2/3:
                o = mutation(individual1.choosing_tree, pop.functions, pop.choosing_terminals, pop.min_height, pop.max_height)
                height2 = o.GetHeight()
                if height2 >= pop.min_height and height2 <= pop.max_height:
                    O.append(Individual(individual1.determining_tree, o))
            # both trees mutation
            else:
                o1 = mutation(individual1.determining_tree, pop.functions, pop.determining_terminals, pop.min_height, pop.max_height)
                height1 = o1.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    o2 = mutation(individual1.choosing_tree, pop.functions, pop.choosing_terminals, pop.min_height, pop.max_height)
                    height2 = o2.GetHeight()
                    if height2 >= pop.min_height and height2 <= pop.max_height:
                        O.append(Individual(o1, o2))    
        # reproduction
        if(np.random.rand() < 0.15):
            tree1 = GenerateRandomTree(pop.functions, pop.determining_terminals, pop.max_height, min_height = pop.min_height )
            tree2 = GenerateRandomTree(pop.functions, pop.choosing_terminals, pop.max_height, min_height = pop.min_height )
            O.append(Individual(tree1, tree2))
    return O


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

def natural_selection(pop):
    fast_nondominated_sort(pop)
    new_indivs = []
    new_fronts = []
    front_num = 0
    while len(new_indivs) + len(pop.ParetoFront[front_num]) <= pop.pop_size:
        new_indivs.extend(pop.ParetoFront[front_num])
        new_fronts.append(pop.ParetoFront[front_num])
        front_num += 1
    calculate_crowding_distance(pop.ParetoFront[front_num])
    pop.ParetoFront[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
    new_indivs.extend(pop.ParetoFront[front_num][0:pop.pop_size - len(new_indivs)])
    new_fronts.append(pop.ParetoFront[front_num][0:pop.pop_size - len(new_indivs)])
    pop.ParetoFront = new_fronts
    pop.indivs = new_indivs


def reproduction1(pop):
    O = []
    for _ in range( pop.pop_size ):
        individual1, individual2 = random.sample(pop.indivs, 2)
        
        crossover_random = np.random.rand()
        # crossover
        # if ( np.random.rand() < self.crossover_rate ):
        if ( crossover_random < pop.crossover_rate ):
            part_crossover = np.random.rand()
            # determining tree crossover
            if part_crossover < 1/3:
                o1 = pop.crossover_operator(individual1.determining_tree, individual2.determining_tree, pop.max_height)
                height1 = o1.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    O.append(Individual(o1, individual1.choosing_tree))
            # choosing tree crossover
            elif part_crossover > 2/3:
                o1 = pop.crossover_operator(individual1.choosing_tree, individual2.choosing_tree, pop.max_height)
                height2 = o1.GetHeight()
                if height2 >= pop.min_height and height2 <= pop.max_height:
                    O.append(Individual(individual1.determining_tree, o1))
            # both trees crossover
            else:
                o1 = pop.crossover_operator(individual1.determining_tree, individual2.determining_tree, pop.max_height)
                height1 = o1.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    o2 = pop.crossover_operator(individual1.choosing_tree, individual2.choosing_tree, pop.max_height)
                    height2 = o2.GetHeight()
                    if height2 >= pop.min_height and height2 <= pop.max_height:
                        O.append(Individual(o1, o2))

        # mutation
        # if ( np.random.rand() < self.mutation_rate ):
        elif ( crossover_random < pop.mutation_rate + pop.crossover_rate ):
            part_mutation = np.random.rand()
            # determining tree mutation
            if part_mutation < 1/3:
                o = pop.mutation_operator(individual1.determining_tree, pop.functions, pop.determining_terminals, pop.min_height, pop.max_height)
                height1 = o.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    O.append(Individual(o, individual1.choosing_tree))
            # choosing tree mutation
            elif part_mutation > 2/3:
                o = pop.mutation_operator(individual1.choosing_tree, pop.functions, pop.choosing_terminals, pop.min_height, pop.max_height)
                height2 = o.GetHeight()
                if height2 >= pop.min_height and height2 <= pop.max_height:
                    O.append(Individual(individual1.determining_tree, o))
            # both trees mutation
            else:
                o1 = pop.mutation_operator(individual1.determining_tree, pop.functions, pop.determining_terminals, pop.min_height, pop.max_height)
                height1 = o1.GetHeight()
                if height1 >= pop.min_height and height1 <= pop.max_height:
                    o2 = pop.mutation_operator(individual1.choosing_tree, pop.functions, pop.choosing_terminals, pop.min_height, pop.max_height)
                    height2 = o2.GetHeight()
                    if height2 >= pop.min_height and height2 <= pop.max_height:
                        O.append(Individual(o1, o2))    
        # reproduction
        if(np.random.rand() < 0.15):
            tree1 = GenerateRandomTree(pop.functions, pop.determining_terminals, pop.max_height, min_height = pop.min_height )
            tree2 = GenerateRandomTree(pop.functions, pop.choosing_terminals, pop.max_height, min_height = pop.min_height )
            O.append(Individual(tree1, tree2))
    return O