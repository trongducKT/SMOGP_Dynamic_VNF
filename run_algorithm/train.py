from data_info.read_data import *
from network.network import Network
from utils.utils import *
from gp.population.population import *
import time 
import multiprocessing     
import matplotlib.pyplot as plt

def trainGP(processing_number, network, vnf_list, request_list,
            functions, terminal_decision, terminal_choosing, 
            pop_size, max_gen,  min_height, max_height, initialization_max_height,  
            num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
            reproduce_opertation, initialize_operator, selection_operator,
            calFitness):
    
    fitness_history = {}
    fitness_history["decision"] = []
    fitness_history["chosing"] = []
    time_start = time.time()
    
    pop = Population(pop_size, functions, terminal_decision, terminal_choosing, 
                    min_height, max_height, initialization_max_height, num_of_tour_particips, tournament_prob,
                    crossover_rate, mutation_rate, reproduce_opertation, initialize_operator, selection_operator )
    pop.initialize()

    print("Danh sach ca the khoi tao")
    for indi in pop.indivs:
        print(indi.determining_tree.GetHumanExpression())
        print(indi.choosing_tree.GetHumanExpression())
    print("Khoi tao xong")

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
    sum_gen = 0   
    for i in range(max_gen):
        offspring = pop.reproduction()
    
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost, a = value

        pop.indivs.extend(offspring)
        pop.natural_selection()    
            
        sum_gen = i+1 
        print("The he ",i)
        for indi in pop.indivs:
            if(indi.rank == 0):
                print(indi.objectives)
                print(indi.determining_tree.GetHumanExpression())
                print(indi.choosing_tree.GetHumanExpression())
                print("Ket thuc mot ca the")
        if checkChange(pop.history) == True and checkChange(pop.history) == True:
            break

        if True:
            x = [indi.objectives[0] for indi in pop.indivs if indi.rank == 0]
            y = [indi.objectives[1] for indi in pop.indivs if indi.rank == 0]
            print(len(x))
            plt.scatter(x, y)
            plt.show()
    pool.close()              
    return sum_gen, time.time()-time_start, fitness_history  