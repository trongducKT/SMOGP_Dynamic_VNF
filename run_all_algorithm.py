from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from run_algorithm.algorithms import *
from deployment.evaluation import calFitness, calFitness_removeGPvalue
from surrogate.gen_pc import *
from utils.crossover import *
from utils.mutation import *

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

    num_pro = 2
    num_train = 10
    pop_size = 80
    max_gen = 50
    min_height = 2
    max_height = 8
    initialization_max_height = 4
    num_of_tour_particips = 2
    tournament_prob = 0.8
    pc = 0.9
    pm = 0.1
    node1 = SubNode()
    node1.AppendChild(PN())
    node1.AppendChild(DDR())

    node2 = AddNode()
    node2.AppendChild(MUC())
    node2.AppendChild(MUR())

    node3 = AddNode()
    node3.AppendChild(node2)
    node3.AppendChild(MUM())

    node4 = SubNode()
    node4.AppendChild(Zero_Node())
    node4.AppendChild(CS())

    node5 = SubNode()
    node5.AppendChild(node4)
    node5.AppendChild(node3)

    rule_ref = Ref_Rule(node1, node5)
    surrogate = Surrogate(20, rule_ref)
    surrogate.gen_situations(10, 50, 10, 20)
    neighborhood_size = 3
    data_set = [r'./data_1_9/conus_centers_easy_s3.json', 
                r'./data_1_9/conus_centers_hard_s3.json', 
                r'./data_1_9/conus_centers_normal_s3.json',
                r'./data_1_9/conus_rural_easy_s3.json', 
                r'./data_1_9/conus_rural_hard_s3.json', 
                r'./data_1_9/conus_rural_normal_s3.json', 
                r'./data_1_9/conus_uniform_easy_s3.json', 
                r'./data_1_9/conus_uniform_hard_s3.json', 
                r'./data_1_9/conus_uniform_normal_s3.json', 
                r'./data_1_9/conus_urban_easy_s3.json', 
                r'./data_1_9/conus_urban_hard_s3.json',
                r'./data_1_9/conus_urban_normal_s3.json']
    for data_path in data_set:
        run_SurrogateNSGAII(data_path, num_pro, num_train,  
        function, terminal_decision, terminal_choosing, 
        pop_size, max_gen,  min_height, max_height, initialization_max_height,  
        num_of_tour_particips, tournament_prob, pc, pm,
        [crossover_branch_individual_swap], [mutation_individual_branch_replace, mutation_individual_node_replace], 3, surrogate, rule_ref,
        calFitness_removeGPvalue)
        run_NSGAII( data_path, num_pro, num_train,  
                    function, terminal_decision, terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob, pc, pm,
                    random_init, crossover_branch_individual_swap, mutation_individual_branch_replace, natural_selection,
                    calFitness_removeGPvalue)
        run_MOEAD(data_path, num_pro, num_train,  
                    function, terminal_decision, terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    pc, pm, random_init, crossover_branch_individual_swap, mutation_individual_branch_replace, natural_selection,
                    neighborhood_size,
                    calFitness_removeGPvalue)
        run_SPEA( data_path, num_pro, num_train,  
                    function, terminal_decision, terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob, pc, pm,
                    random_init, crossover_branch_individual_swap, mutation_individual_branch_replace, natural_selection,
                    calFitness_removeGPvalue)
    