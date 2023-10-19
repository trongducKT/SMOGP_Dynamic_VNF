from copy import deepcopy
import numpy as np
from numpy.random import randint
import time


class Individual:
    def __init__(self, chromosomes, default_fitness=-float('inf')):
        self.fitness = default_fitness
        self.chromosomes = chromosomes
        self.reject = 0
        self.cost = np.inf

class Population:
    def __init__(self, pop_size,functions,terminals,min_height,max_height,initialization_max_tree_height, evaluation):
        self.history = []
        self.pop_size = pop_size
        self.functions  = functions 
        self.terminals = terminals
        self.min_height = min_height
        self.max_height = max_height
        self.initialization_max_tree_height = initialization_max_tree_height
        self.indivs = []
        self.evaluation = evaluation
    def random_init(self):
        #print("random init")
        curr_max_depth = self.min_height
        init_depth_interval = self.pop_size / (self.initialization_max_tree_height - self.min_height + 1)
        next_depth_interval = init_depth_interval
        for i in range( self.pop_size ):
            if i >= next_depth_interval:
                next_depth_interval += init_depth_interval
                curr_max_depth += 1
            t = self.GenerateRandomTree( self.functions, self.terminals, curr_max_depth, curr_height=0, 
                method='grow' if np.random.random() < .5 else 'full', min_height=self.min_height )
            inv = Individual(t)
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
                c = self.GenerateRandomTree( functions, terminals, max_height, curr_height=curr_height + 1, method=method, min_height=min_height )
                n.AppendChild( c ) # do not use n.children.append because that won't set the n as parent node of c

        return n

    def mutation(self,individual, max_height=4, min_height=2 ):
        # mutation_branch = self.GenerateRandomTree( self.functions, self.terminals, max_height, min_height=min_height )
        
        nodes = individual.GetSubtree()
        # print("nodes66", nodes)
        nodes, chosen_depth = self.__GetCandidateNodesAtUniformRandomDepth(nodes, self.max_height )
        # print("node68", nodes)
        to_replace = nodes[randint(len(nodes))]
        # print("to_replace", to_replace)
        
        # mutation_branch = self.GenerateRandomTree( self.functions, self.terminals, max_height, min_height=min_height )
        if not to_replace.parent:
            mutation_branch = self.GenerateRandomTree( self.functions, self.terminals, max_height, min_height=min_height )
            del individual
            return mutation_branch

        if chosen_depth == self.max_height:
            mutation_branch = np.random.choice(self.terminals)
        else:
            mutation_branch = self.GenerateRandomTree(self.functions, self.terminals, self.max_height - chosen_depth, min_height = 1)
        
        
        p = to_replace.parent
        idx = p.DetachChild(to_replace)
            
        # mutation_branch = self.GenerateRandomTree( self.functions, self.terminals, max_height -depth_index -1, min_height=min_height )
        p.InsertChildAtPosition(idx, mutation_branch)
        return individual


    def crossover(self, individual, donor, max_height=4, min_height=2 ):
        #print("crossover")
	# this version of crossover returns 1 child
        individual = deepcopy(individual)
        nodes1 = individual.GetSubtree()
        # print("Hello 96", nodes1)
        nodes2 = donor.GetSubtree()	# no need to deep copy all nodes of parent2
        # print("Hello 98", nodes2)
        nodes1, depth_node1 = self.__GetCandidateNodesAtUniformRandomDepth( nodes1, self.max_height )
        nodes2, depth_node2 = self.__GetCandidateNodesAtUniformRandomDepth_crossover( nodes2, self.max_height - depth_node1 )

        while nodes2 == False:
            nodes1, depth_node1 = self.__GetCandidateNodesAtUniformRandomDepth( nodes1, self.max_height )
            nodes2, depth_node2 = self.__GetCandidateNodesAtUniformRandomDepth_crossover( nodes2, self.max_height - depth_node1 )
        # print(depth_node1, depth_node2)
        # print(nodes1, nodes2)
        to_swap1 = nodes1[ randint(len(nodes1)) ]
        to_swap2 = deepcopy( nodes2[ randint(len(nodes2)) ] )
        # print("to_swap1", to_swap1)
        # print("to_swap2", to_swap2)
        to_swap2.parent = None

        p1 = to_swap1.parent

        if not p1:
            # print("Tai goc")
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

    def reproduction(self, crossover_rate, mutation_rate):
        #print("reproduction")
        O = []
        for i in range( self.pop_size ):
            o = deepcopy(self.indivs[i]).chromosomes
            if ( np.random.rand() < crossover_rate ):
                o1 = self.crossover(o,self.indivs[ randint( self.pop_size )].chromosomes, self.max_height, self.min_height)
                height1 = o1.GetHeight()
                if height1 >= self.min_height and height1 <= self.max_height:
                    O.append(Individual(o1))

            if ( np.random.rand() < mutation_rate ):
                o2 = self.mutation(o, self.max_height, self.min_height)

                height2 = o2.GetHeight()
                if height2 >= self.min_height and height2 <= self.max_height:
                    O.append(Individual(o2))
            # check offspring meets constraints	
        return O

    def natural_selection(self):
        #print("natural selection")
        self.indivs.sort(key=lambda x: x.fitness, reverse=False)
        self.indivs = self.indivs[:self.pop_size]

    def run(self, max_gen=1000, crossover_rate=0.8, mutation_rate=0.05):
        self.random_init()

        for i in range(max_gen):
            offspring = self.reproduction(crossover_rate, mutation_rate)
            self.indivs.extend(offspring)
            self.natural_selection()
            best_indiv = self.indivs[0]
            self.history.append(best_indiv.fitness)
            print('Iteration', i, ', best fitness =', best_indiv.fitness)

        return self.indivs[0]
