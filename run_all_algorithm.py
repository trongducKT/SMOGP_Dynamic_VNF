from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from run_algorithm.algorithms import *
from deployment.evaluation import calFitness, calFitness_removeGPvalue
from surrogate.gen_pc import *
from utils.crossover import *
from utils.mutation import *
from run_algorithm.train_Surrogate_NSGA_II import SurrogateNSGAPopulation
from surrogate.gen_surrogate_data import gen_surrogate

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

    num_pro = 10
    num_train = 10
    pop_size = 50
    max_gen = 15
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
    neighborhood_size = 5
    data_set = [r'input_noob\nsf_rural_noob_s3.json']
    for data_path in data_set:
        surrogate = gen_surrogate(data_path, num_train, 10, rule_ref)
        for request in surrogate.ordered_situations:
            print(request)
        for server in surrogate.server_situations:
            print(server)
        pop = SurrogateNSGAPopulation(pop_size, function, terminal_decision, terminal_choosing, min_height,
                                  max_height, initialization_max_height, num_of_tour_particips, tournament_prob,
                                  pc, pm, None, None, None, None, None, 
                                  surrogate, rule_ref, neighborhood_size)
        pop.random_init()


        run_SurrogateNSGAII(data_path, num_pro, pop.indivs, num_train,  
        function, terminal_decision, terminal_choosing, 
        pop_size, max_gen,  min_height, max_height, initialization_max_height,  
        num_of_tour_particips, tournament_prob, pc, pm,
        [crossover_branch_individual_swap], [mutation_individual_node_replace], 5, surrogate, rule_ref,
        calFitness)
        print("Hoan thanh")
        # time.sleep(10)
        # run_SurrogateNSGAII(data_path, num_pro, pop.indivs, num_train,  
        # function, terminal_decision, terminal_choosing, 
        # pop_size, max_gen,  min_height, max_height, initialization_max_height,  
        # num_of_tour_particips, tournament_prob, pc, pm,
        # [crossover_branch_individual_swap], [mutation_individual_node_replace], 5, surrogate, rule_ref,
        # calFitness)
        
        
        run_NSGAII( data_path, num_pro, pop.indivs,  num_train,  
                    function, terminal_decision, terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob, pc, pm,
                    random_init, crossover_branch_individual_swap, mutation_individual_branch_replace, natural_selection,
                    calFitness)
        
        
        # run_MOEAD(data_path, num_pro, pop.indivs, num_train,  
        #             function, terminal_decision, terminal_choosing, 
        #             pop_size, max_gen,  min_height, max_height, initialization_max_height,  
        #             pc, pm, random_init, crossover_branch_individual_swap, mutation_individual_branch_replace, natural_selection,
        #             neighborhood_size,
        #             calFitness_removeGPvalue)
        
        
        # run_SPEA( data_path, num_pro, pop.indivs,  num_train,  
        #             function, terminal_decision, terminal_choosing, 
        #             pop_size, max_gen,  min_height, max_height, initialization_max_height,  
        #             num_of_tour_particips, tournament_prob, pc, pm,
        #             random_init, crossover_branch_individual_swap, mutation_individual_branch_replace, natural_selection,
        #             calFitness_removeGPvalue)
    