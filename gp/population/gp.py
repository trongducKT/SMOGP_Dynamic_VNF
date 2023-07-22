from copy import deepcopy
import numpy as np
from numpy.random import randint


class Individual:
    def __init__(self, chromosomes, default_fitness=-float('inf')):
        self.fitness = default_fitness
        self.chromosomes = chromosomes

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
        mutation_branch = self.GenerateRandomTree( self.functions, self.terminals, max_height, min_height=min_height )
        
        nodes = individual.GetSubtree()

        nodes = self.__GetCandidateNodesAtUniformRandomDepth( nodes )

        to_replace = nodes[randint(len(nodes))]

        if not to_replace.parent:
            del individual
            return mutation_branch


        p = to_replace.parent
        idx = p.DetachChild(to_replace)
        p.InsertChildAtPosition(idx, mutation_branch)

        return individual


    def crossover(self, individual, donor ):
	
	# this version of crossover returns 1 child
        nodes1 = individual.GetSubtree()
        nodes2 = donor.GetSubtree()	# no need to deep copy all nodes of parent2

        nodes1 = self.__GetCandidateNodesAtUniformRandomDepth( nodes1 )
        nodes2 = self.__GetCandidateNodesAtUniformRandomDepth( nodes2 )

        to_swap1 = nodes1[ randint(len(nodes1)) ]
        to_swap2 = deepcopy( nodes2[ randint(len(nodes2)) ] )	# we deep copy now, only the sutbree from parent2
        to_swap2.parent = None

        p1 = to_swap1.parent

        if not p1:
            return to_swap2

        idx = p1.DetachChild(to_swap1)
        p1.InsertChildAtPosition(idx, to_swap2)

        return individual


    def __GetCandidateNodesAtUniformRandomDepth(self,nodes ):

        depths = np.unique( [x.GetDepth() for x in nodes] )
        chosen_depth = depths[randint(len(depths))]
        candidates = [x for x in nodes if x.GetDepth() == chosen_depth]

        return candidates

    def reproduction(self, crossover_rate, mutation_rate):
        O = []
        for i in range( self.pop_size ):
            o = deepcopy(self.indivs[i]).chromosomes
            if ( np.random.rand() < crossover_rate ):
                o = self.crossover(o,self.indivs[ randint( self.pop_size )].chromosomes)
            if ( np.random.rand() < crossover_rate + mutation_rate ):
                o = self.mutation(o)
            # check offspring meets constraints	
            invalid_offspring = False
            if len(o.GetSubtree()) > self.max_height:
                invalid_offspring = True
            elif (o.GetHeight() < self.min_height):
                invalid_offspring = True	
            if invalid_offspring:
                del o
                o = deepcopy(self.indivs[i]).chromosomes
                ind = Individual(o,self.indivs[i].fitness)
            else:
                ind = Individual(o)
                ind.fitness = self.evaluation(ind)
            O.append(ind)
        return O

    def natural_selection(self):
        self.indivs.sort(key=lambda x: x.fitness, reverse=True)
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
