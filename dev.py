from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from run_algorithm.algorithms import *
from deployment.evaluation import calFitness_three_policies
from surrogate.gen_pc import *
from utils.crossover import *
from utils.mutation import *
from run_algorithm.train_Surrogate_NSGA_II import SurrogateNSGAPopulation
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()
    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
    terminal_determining = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
    terminal_ordering = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
    terminal_choosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR(), Const()]
    num_pro = 10
    num_train = 10
    pop_size = 50
    max_gen = 15
    min_height = 2
    max_height = 8
    initialization_max_height = 4
    num_of_tour_particips = 2
    tournament_prob = 0.8
    pc = 0.8
    pm = 0.1
    num_neigbor = 5

    #determining_tree
    determining_tree = AddNode()
    determining_tree.AppendChild(DDR())
    determining_tree.AppendChild(BR())

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
    crossover_operator_list = [crossover_branch_individual_swap]
    mutation_operator_list = [mutation_individual_branch_replace]

    rule_ref = Ref_Rule(determining_tree, node1, node5)
    neighborhood_size = 5
    data_set = [r'input_noob\nsf_rural_noob_s3.json']
    for data_path in data_set:
        surrogate = Surrogate(10, rule_ref)
        surrogate.gen_situations_random(20, 50, 5, 10)
        pop = SurrogateNSGAPopulation(pop_size, function, terminal_determining, terminal_ordering, terminal_choosing,
                                      min_height, max_height, initialization_max_height, num_of_tour_particips,
                                      tournament_prob, pc, pm, determining_tree, surrogate, rule_ref, num_neigbor)
        pop.random_init()
        # run_SurrogateNSGAII(data_path, num_pro, pop.indivs, num_train, function, terminal_determing, terminal_ordering,
        #                     terminal_choosing, pop_size, max_gen, min_height, max_height, initialization_max_height,
        #                     num_of_tour_particips, tournament_prob, pc, pm, crossover_operator_list, mutation_operator_list,
        #                     num_neigbor, surrogate, rule_ref, calFitness_three_policies, determinig_tree)

        run_NSGAII( data_path, num_pro, pop.indivs, num_train,  
                function, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                crossover_operator_list, mutation_operator_list, calFitness_three_policies, determining_tree)