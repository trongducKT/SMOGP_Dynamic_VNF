class Population:
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 reproduce_opertation, initialize_operator, selection_operator):
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

        self.reproduce_opertation = reproduce_opertation
        self.initialize_operator = initialize_operator
        self.selection_operator = selection_operator
    
    def initialize(self):
        self.initialize_operator(self)
    
    def reproduction(self):
        return self.reproduce_opertation(self)

    def natural_selection(self):
        self.selection_operator(self)    
    

    
    
