from copy import deepcopy
class Population:
    def __init__(self, pop_size, 
                 functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree):
        self.history = []
        self.ParetoFront = []
        self.pop_size = pop_size
        self.functions  = functions 
        self.determining_terminals = determining_terminals
        self.ordering_terminals = ordering_terminals
        self.choosing_terminals = choosing_terminals
        self.min_height = min_height
        self.max_height = max_height
        self.initialization_max_tree_height = initialization_max_tree_height
        self.indivs = []
        self.num_of_tour_ptiarcips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

        self.determining_tree = determining_tree
    
    def pre_indi_gen(self, indi_list):
        if len(indi_list) != self.pop_size:
            raise ValueError("The length of the list of individuals is not equal to the population size")
        self.indivs = deepcopy(indi_list)
    

    
    
