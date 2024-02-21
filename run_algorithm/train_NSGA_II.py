from data_info.read_data import *
from network.network import Network
from utils.utils import *
from gp.population.population import *
import time 
import multiprocessing     
import matplotlib.pyplot as plt

class NSGAPopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 initialize_operator, crossover_operator, mutation_operator, selection_operator, 
                 reproduce_opertation):
        super().__init__(pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator)

        self.reproduce_opertation = reproduce_opertation

    def reproduction(self):
        return self.reproduce_opertation(self)

def trainNSGAII(processing_number, network, vnf_list, request_list,
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                reproduce_operator, calFitness):
    
    # fitness_history = {}
    # fitness_history["decision"] = []
    # fitness_history["chosing"] = []

    # Return
    Pareto_front_generations = []
    
    pop = NSGAPopulation(pop_size, functions, terminal_determining, terminal_choosing,
                          min_height, max_height, initialization_max_height,
                          num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                          initialize_operator, crossover_operator, mutation_operator, selection_operator, 
                          reproduce_operator)
    pop.initialize()

    # print("Danh sach ca the khoi tao")
    # for indi in pop.indivs:
    #     print(indi.determining_tree.GetHumanExpression())
    #     print(indi.choosing_tree.GetHumanExpression())
    # print("Khoi tao xong")

    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    print("Bat dau tinh fitness")
    result = pool.starmap(calFitness, arg)
    # len_decision = len(pop.indivs)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost, a = value
    print("Tinh fitness xong")
          
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
        print("The he ",i)
        for indi in pop.indivs:
            if(indi.rank == 0):
                print(indi.objectives)
                print(indi.determining_tree.GetHumanExpression())
                print(indi.choosing_tree.GetHumanExpression())
                print("Ket thuc mot ca the")
        

        # if checkChange(pop.history) == True and checkChange(pop.history) == True:
        #     break
        
    pool.close()
    return Pareto_front_generations


# Pareto front across generations (list of Individuals)