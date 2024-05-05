from data_info.read_data import *
from network.network import Network
from utils.utils import *
from gp.population.population import *
import multiprocessing     
import random
from utils.initialization import individual_init
from utils.selection import natural_selection
import time

class NSGAPopulation(Population):
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
    
    def natural_selection(self):
        natural_selection(self)


def trainNSGAII(processing_number, indi_list,  network, vnf_list, request_list,
                functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, max_time):
    

    time_objective = {}
    Pareto_front_generations = []
    hv = []
    time_start = time.time()
    pop = NSGAPopulation(pop_size, functions, terminal_determining, terminal_ordering, terminal_choosing, 
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
    
    pop.natural_selection()
    Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0]) 
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
    print("The he 0: ", hv[-1])
    time_objective[0] = {"time": time.time() - time_start, "HV": hv[-1]}     
    for i in range(max_gen):
        if time.time() - time_start >= max_time:
            pool.close()
            break
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        print(len(offspring))
        arg = []

        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost = value
        pop.indivs.extend(offspring)
        pop.natural_selection()    
        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))  
        print("The he ", i+1, ": ", hv[-1])
        time_objective[i + 1] = {"time": time.time() - time_start, "HV": hv[-1]}
        if len(hv) > 10:
            if hv[-1] - hv[-10] < 0.001:
                pool.close()
                break        
    pool.close()
    return Pareto_front_generations, time_objective


# Pareto front across generations (list of Individuals)