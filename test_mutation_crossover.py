from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from gp.population.ultis import reproduction, natural_selection, random_init
from run_algorithm.gp_algorithm import *
from deployment.evaluation import calFitness, calFitness_removeGPvalue

if __name__ == '__main__':
    multiprocessing.freeze_support()
    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
    terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
    terminal_chosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR(), Const()]

    # a = run_proposed(r'./data_1_9/nsf_rural_easy_s3.json', 8, 10, function, terminal_decision, terminal_chosing, 10, 100,
    #                 2, 8, 4, 2, 0.8, 0.9, 0.1, 
    #                 reproduction, random_init, natural_selection, calFitness)
    
    # a = run_proposed(r'./data_1_9/nsf_urban_normal_s2.json', 8, 10, function, terminal_decision, terminal_chosing, 10, 100,
    #             2, 8, 4, 2, 0.8, 0.9, 0.1, 
    #             reproduction, random_init, natural_selection, calFitness)
    
    # a = run_proposed(r'./data_1_9/nsf_rural_hard_s2.json', 8, 10, function, terminal_decision, terminal_chosing, 10, 100,
    #             2, 8, 4, 2, 0.8, 0.9, 0.1, 
    #             reproduction, random_init, natural_selection, calFitness)

    a = run_MOEAD(r'./data_1_9/nsf_rural_easy_s3.json', 8, 10, function, terminal_decision, terminal_chosing, 10, 100,
                    2, 8, 4, 2, 0.8, 0.9, 0.1, 
                    reproduction, random_init, natural_selection, 3, calFitness)