from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from run_algorithm.algorithms import *
from deployment.evaluation import calFitness, calFitness_removeGPvalue

if __name__ == '__main__':
    multiprocessing.freeze_support()
    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
    terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
    terminal_choosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR(), Const()]

    # a = run_proposed(r'./data_1_9/nsf_rural_easy_s3.json', 8, 10, function, terminal_decision, terminal_chosing, 100, 10,
    #                 2, 8, 4, 2, 0.8, 0.9, 0.1, 
    #                 reproduction, random_init, natural_selection, calFitness)
    
    # a = run_proposed(r'./data_1_9/nsf_urban_normal_s2.json', 8, 10, function, terminal_decision, terminal_chosing, 10, 100,
    #             2, 8, 4, 2, 0.8, 0.9, 0.1, 
    #             reproduction, random_init, natural_selection, calFitness)
    
    # a = run_proposed(r'./data_1_9/nsf_rural_hard_s2.json', 8, 10, function, terminal_decision, terminal_chosing, 10, 100,
    #             2, 8, 4, 2, 0.8, 0.9, 0.1, 
    #             reproduction, random_init, natural_selection, calFitness)

    num_pro = 90
    num_train = 10
    pop_size = 80
    max_gen = 100
    min_height = 2
    max_height = 8
    initialization_max_height = 4
    num_of_tour_particips = 2
    tournament_prob = 0.8
    pc = 0.8
    pm = 0.1
    neighborhood_size = 3

    data_path = r'./data_1_9/nsf_rural_easy_s3.json'

    a = run_NSGAII( data_path, num_pro, num_train,  
                function, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                random_init, crossover, mutation, natural_selection,
                reproduction1, calFitness)
    a = run_MOEAD(data_path, num_pro, num_train,  
                function, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                pc, pm, random_init, crossover, mutation, natural_selection,
                neighborhood_size,
                calFitness)
    
    data_path = r'./data_1_9/nsf_urban_normal_s2.json'

    a = run_NSGAII( data_path, num_pro, num_train,  
                function, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                random_init, crossover, mutation, natural_selection,
                reproduction1, calFitness)
    a = run_MOEAD(data_path, num_pro, num_train,  
                function, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                pc, pm, random_init, crossover, mutation, natural_selection,
                neighborhood_size,
                calFitness)
    
    data_path = r'./data_1_9/nsf_rural_hard_s2.json'

    a = run_NSGAII( data_path, num_pro, num_train,  
                function, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                random_init, crossover, mutation, natural_selection,
                reproduction1, calFitness)
    a = run_MOEAD(data_path, num_pro, num_train,  
                function, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                pc, pm, random_init, crossover, mutation, natural_selection,
                neighborhood_size,
                calFitness)