from data_info.read_data import *
from network.network import Network
from utils.utils import *
from gp.population.population import *
import multiprocessing     
import random
from utils.initialization import individual_init
from utils.selection import natural_selection

class SingleObjectivePopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree):
        super().__init__(pop_size, 
                 functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree)

   
    def gen_offspring(self, crossover_operator_list, mutation_operator_list):
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
            if np.random.random() < self.crossover_rate:
                for crossover_operator in crossover_operator_list:
                    children1, children2 = crossover_operator(indi1, indi2, self.min_height, self.max_height, self.determining_tree)
                    offspring.extend([children1, children2])
            if np.random.random() < self.mutation_rate:
                for mutation_operator in mutation_operator_list:
                    mutant1 = mutation_operator(indi1, self.functions, 
                                                self.determining_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, self.determining_tree)
                    mutant2 = mutation_operator(indi2, self.functions, 
                                                self.determining_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, self.determining_tree)
                    offspring.extend([mutant1, mutant2])
            if np.random.random() < 1 - self.crossover_rate - self.mutation_rate:
                indi = individual_init(self.min_height, self.max_height, self.determining_tree, self.functions,
                                       self.determining_terminals, self.ordering_terminals, self.choosing_terminals)
                offspring.append(indi)
        return offspring
    
    def natural_selection(self, alpha):
        self.indivs.sort(key=lambda x: x.objectives[0]*alpha + x.objectives[1]*(1-alpha))
        self.indivs = self.indivs[:self.pop_size]
    
    def take_best(self, alpha):
        self.indivs.sort(key=lambda x: x.objectives[0]*alpha + x.objectives[1]*(1-alpha))
        return self.indivs[0]


def trainSingleObjective(processing_number, indi_list,  network, vnf_list, request_list,
                functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, alpha):
    print("Số request:",len(request_list))
    pop = SingleObjectivePopulation(pop_size, functions, terminal_determining, terminal_ordering, terminal_choosing, 
                        min_height, max_height, initialization_max_height, 
                        num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                        determining_tree)
    # pop.initialize()
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost = value
    print("Khởi tạo xong ")  
    
    best = pop.take_best(alpha)
    print("The he 0:")
    print(best.objectives)    
    for i in range(max_gen):
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost = value
  
        pop.indivs.extend(offspring)
        pop.natural_selection(alpha)
        best = pop.take_best(alpha)   
        print("The he ", i+1)
        print(best.objectives, best.reject, best.cost)      
    pool.close()
    return best

def run_SingleObjective( data_path, processing_num, indi_list, num_train,  
                functions, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, alpha):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
    best = trainSingleObjective(processing_num, indi_list,  network, vnf_list, request_train,
                    functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, alpha)
    # Store the Pareto front and objective Pareto
    normal_reject, normal_cost, reject, cost = calFitness(best, network, request_test, vnf_list)
    print(normal_reject, normal_cost, reject, cost)
    
    pool = multiprocessing.Pool(processes=processing_num)
    return  True