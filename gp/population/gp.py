from copy import deepcopy
import numpy as np
from numpy.random import randint
import time
import random
from queue import Queue


class Individual:
    def __init__(self, determining_tree, choosing_tree):
        self.determining_tree = determining_tree
        self.choosing_tree = choosing_tree
        self.objectives = np.zeros(2)
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None # be dominated
        self.dominated_solutions = None # dominate

    # Dominate operator
    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)
    
    # Individual equation
    def __eq__(self, other):
        # Tree 1
        expr1 = self.determining_tree.GetHumanExpression()
        expr2 = other.determining_tree.GetHumanExpression()
        if expr1 != expr2:
            return False
        # Tree 2
        expr1 = self.choosing_tree.GetHumanExpression()
        expr2 = other.choosing_tree.GetHumanExpression()
        if expr1 != expr2:
            return False
        return True
                 

class Population:
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, min_height, max_height, 
                 initialization_max_tree_height, num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate):
        self.history = []
        self.ParetoFront = []
        self.pop_size = pop_size
        self.functions  = functions 
        self.determining_terminals = determining_terminals
        self.choosing_terminals = choosing_terminals
        self.min_height = min_height
        self.max_height = max_height
        self.initialization_max_tree_height = initialization_max_tree_height
        self.indivs = []
        self.num_of_tour_ptiarcips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        
    def fast_nondominated_sort(self):
        self.ParetoFront = [[]]
        for individual in self.indivs:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in self.indivs:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                self.ParetoFront[0].append(individual)
        i = 0
        while len(self.ParetoFront[i]) > 0:
            temp = []
            for individual in self.ParetoFront[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            self.ParetoFront.append(temp)


    def calculate_crowding_distance(self, front):
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

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (
                        individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1
        
        
    def random_init(self):
        curr_max_depth = self.min_height
        init_depth_interval = self.pop_size / (self.initialization_max_tree_height - self.min_height + 1)
        next_depth_interval = init_depth_interval
        for i in range( self.pop_size ):
            if i >= next_depth_interval:
                next_depth_interval += init_depth_interval
                curr_max_depth += 1
            determining_tree = self.GenerateRandomTree( self.functions, self.determining_terminals, curr_max_depth, 
                                                       curr_height=0, 
                method='grow' if np.random.random() < .5 else 'full', min_height=self.min_height )
            choosing_tree = self.GenerateRandomTree( self.functions, self.choosing_terminals, curr_max_depth, 
                                                    curr_height=0, 
                method='grow' if np.random.random() < .5 else 'full', min_height=self.min_height )
            inv = Individual(determining_tree, choosing_tree)
            self.indivs.append(inv)
    

    def GenerateRandomTree(self,functions, terminals, max_height, curr_height=0, method='grow', min_height=2):
        if curr_height == max_height:
            idx = randint(len(terminals))
            n = deepcopy( terminals[idx] )
        else:
            if method == 'grow' and curr_height	>= min_height:
                term_n_funs = terminals + functions
                idx = randint( len(term_n_funs) )
                n = deepcopy( term_n_funs[idx] )
            elif method == 'full' or (method == 'grow' and curr_height < min_height):
                idx = randint( len(functions) )
                n = deepcopy( functions[idx] )
            else:
                raise ValueError('Unrecognized tree generation method')

            for i in range(n.arity):
                c = self.GenerateRandomTree( functions, terminals, max_height, curr_height=curr_height + 1, 
                                            method=method, min_height=min_height )
                n.AppendChild( c ) # do not use n.children.append because that won't set the n as parent node of c
        return n

    def mutation(self,individual,functions, terminals ):
        
        nodes = individual.GetSubtree()
        nodes, chosen_depth = self.__GetCandidateNodesAtUniformRandomDepth(nodes, self.max_height )
        to_replace = nodes[randint(len(nodes))]
        
        if not to_replace.parent:
            mutation_branch = self.GenerateRandomTree(functions, terminals, self.max_height, min_height = self.min_height )
            del individual
            return mutation_branch

        if chosen_depth == self.max_height:
            mutation_branch = np.random.choice(terminals)
        else:
            mutation_branch = self.GenerateRandomTree(functions, terminals, self.max_height - chosen_depth, min_height = 1)
        
        
        p = to_replace.parent
        idx = p.DetachChild(to_replace)
            
        p.InsertChildAtPosition(idx, mutation_branch)
        return individual


    def crossover(self, individual, donor):
        individual = deepcopy(individual)
        nodes1_subtree = individual.GetSubtree()
        nodes2_subtree = donor.GetSubtree()	# no need to deep copy all nodes of parent2
        nodes1, depth_node1 = self.__GetCandidateNodesAtUniformRandomDepth( nodes1_subtree, self.max_height )
        nodes2, depth_node2 = self.__GetCandidateNodesAtUniformRandomDepth_crossover( nodes2_subtree, self.max_height - 
                                                                                     depth_node1 )

        while nodes2 == False:
            nodes1, depth_node1 = self.__GetCandidateNodesAtUniformRandomDepth( nodes1_subtree, self.max_height )
            nodes2, depth_node2 = self.__GetCandidateNodesAtUniformRandomDepth_crossover( nodes2_subtree, self.max_height - 
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


    def __GetCandidateNodesAtUniformRandomDepth(self,nodes, max_height_thereshold):

        depths_total = np.unique( [x.GetDepth() for x in nodes] )
        depths = []
        for depth in depths_total:
            if depth > 0 and depth <= max_height_thereshold:
                depths.append(depth)
        chosen_depth = depths[randint(len(depths))]
        candidates = [x for x in nodes if x.GetDepth() == chosen_depth]

        return candidates, chosen_depth
    
    def __GetCandidateNodesAtUniformRandomDepth_crossover(self,nodes, max_height_thereshold):

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

    def reproduction(self):
        O = []
        for _ in range( self.pop_size ):
            # individual1_index = self.tournament_selection(-1)
            # individual2_index = self.tournament_selection(individual1_index)

            # individual1 = deepcopy(self.indivs[individual1_index])
            # individual2 = deepcopy(self.indivs[individual2_index])
            individual1, individual2 = random.sample(self.indivs, 2)
            
            SD = np.linalg.norm(individual1.objectives - individual2.objectives)
            print("SD", SD)
            # crossover
            # if ( np.random.rand() < self.crossover_rate ):
            if ( SD > 0.1 ):
                part_crossover = np.random.rand()
                # determining tree crossover
                if part_crossover < 1/3:
                    o1 = self.crossover(individual1.determining_tree, individual2.determining_tree)
                    height1 = o1.GetHeight()
                    if height1 >= self.min_height and height1 <= self.max_height:
                        O.append(Individual(o1, individual1.choosing_tree))
                # choosing tree crossover
                elif part_crossover > 2/3:
                    o1 = self.crossover(individual1.choosing_tree, individual2.choosing_tree)
                    height2 = o1.GetHeight()
                    if height2 >= self.min_height and height2 <= self.max_height:
                        O.append(Individual(individual1.determining_tree, o1))
                # both trees crossover
                else:
                    o1 = self.crossover(individual1.determining_tree, individual2.determining_tree)
                    height1 = o1.GetHeight()
                    if height1 >= self.min_height and height1 <= self.max_height:
                        o2 = self.crossover(individual1.choosing_tree, individual2.choosing_tree)
                        height2 = o2.GetHeight()
                        if height2 >= self.min_height and height2 <= self.max_height:
                            O.append(Individual(o1, o2))

            # mutation
            # if ( np.random.rand() < self.mutation_rate ):
            if ( SD < 0.1 ):
                part_mutation = np.random.rand()
                # determining tree mutation
                if part_mutation < 1/3:
                    o = self.mutation(individual1.determining_tree, self.functions, self.determining_terminals)
                    height1 = o.GetHeight()
                    if height1 >= self.min_height and height1 <= self.max_height:
                        O.append(Individual(o, individual1.choosing_tree))
                # choosing tree mutation
                elif part_mutation > 2/3:
                    o = self.mutation(individual1.choosing_tree, self.functions, self.choosing_terminals)
                    height2 = o.GetHeight()
                    if height2 >= self.min_height and height2 <= self.max_height:
                        O.append(Individual(individual1.determining_tree, o))
                # both trees mutation
                else:
                    o1 = self.mutation(individual1.determining_tree, self.functions, self.determining_terminals)
                    height1 = o1.GetHeight()
                    if height1 >= self.min_height and height1 <= self.max_height:
                        o2 = self.mutation(individual1.choosing_tree, self.functions, self.choosing_terminals)
                        height2 = o2.GetHeight()
                        if height2 >= self.min_height and height2 <= self.max_height:
                            O.append(Individual(o1, o2))    
            # reproduction
            if(np.random.rand() < 0.15):
                tree1 = self.GenerateRandomTree(self.functions, self.determining_terminals, self.max_height, min_height = self.min_height )
                tree2 = self.GenerateRandomTree(self.functions, self.choosing_terminals, self.max_height, min_height = self.min_height )
                O.append(Individual(tree1, tree2))

        return O

    def tournament_selection(self, remove_position):
        index_list = list(np.arange(len(self.indivs)))
        if remove_position in index_list:
            index_list.remove(remove_position)
        print("index_list", index_list)
        participants = random.sample(index_list, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(self.indivs[participant], self.indivs[best]) == 1 and 
                                np.random.random() < self.tournament_prob):
                best = participant
        return best

    def natural_selection(self):
        self.fast_nondominated_sort()
        new_indivs = []
        new_fronts = []
        front_num = 0
        while len(new_indivs) + len(self.ParetoFront[front_num]) <= self.pop_size:
            new_indivs.extend(self.ParetoFront[front_num])
            new_fronts.append(self.ParetoFront[front_num])
            front_num += 1
        self.calculate_crowding_distance(self.ParetoFront[front_num])
        self.ParetoFront[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
        new_indivs.extend(self.ParetoFront[front_num][0:self.pop_size - len(new_indivs)])
        new_fronts.append(self.ParetoFront[front_num][0:self.pop_size - len(new_indivs)])
        self.ParetoFront = new_fronts
        self.indivs = new_indivs