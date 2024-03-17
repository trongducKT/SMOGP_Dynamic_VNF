from data_info.read_data import *
from network.network import Network
from utils.utils import *
from gp.population.population import *
from gp.population.individual import Individual
import time 
import multiprocessing     
import matplotlib.pyplot as plt
import random
from utils.utils import cal_hv_front
from utils.function_operator import fast_nondominated_sort

class NSGAPopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 initialize_operator, crossover_operator, mutation_operator, selection_operator):
        super().__init__(pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator)

    def reproduction(self):
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
            if np.random.random() < self.crossover_rate:
                children1, children2 = self.crossover_operator(indi1, indi2, self.min_height, self.max_height)
                offspring.extend([children1, children2])
            if np.random.random() < self.mutation_rate:
                mutant1 = self.mutation_operator(indi1, self.functions, self.determining_terminals, 
                                    self.choosing_terminals, self.min_height, self.max_height)
                mutant2 = self.mutation_operator(indi2, self.functions, self.determining_terminals,
                                    self.choosing_terminals, self.min_height, self.max_height)
                offspring.extend([mutant1, mutant2])
        return offspring

def trainNSGAII(processing_number, indi_list,  network, vnf_list, request_list,
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                calFitness):
    
    Pareto_front_generations = []
    hv = []
    pop = NSGAPopulation(pop_size, functions, terminal_determining, terminal_choosing,
                          min_height, max_height, initialization_max_height,
                          num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                          initialize_operator, crossover_operator, mutation_operator, selection_operator)
    # pop.initialize()
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    # len_decision = len(pop.indivs)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost, a = value
    print("Khởi tạo xong ")
    # pop.natural_selection()    

    fast_nondominated_sort(pop)   

    Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0]) 
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
    # Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])       
    for i in range(max_gen):
        offspring = pop.reproduction()
        print("reproduction xong")
        arg = []

        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost, a = value

        pop.indivs.extend(offspring)
        pop.natural_selection()    

        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))  
        print("The he ",i)
        for indi in pop.indivs:
            if(indi.rank == 0):
                print(indi.objectives)
                print("Ket thuc mot ca the")
        if len(hv) > 10:
            if hv[-1] - hv[-10] < 0.01:
                pool.close()
                break
        
    pool.close()
    return Pareto_front_generations


# Pareto front across generations (list of Individuals)