from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from data_info.read_data import *
from network.network import Network
from utils.utils import *
from .train import *


def run_proposed(data_path, processing_num, num_train,  
                functions, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                reproduce_opertation, initialize_operator, selection_operator,
                calFitness):
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

    sum_gen,time_train, fitness_history = trainGP(processing_num, network, vnf_list, request_train,
                                                  functions, terminal_decision, terminal_choosing,
                                                  pop_size, max_gen, min_height, max_height, initialization_max_height,
                                                  num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                                                  reproduce_opertation, initialize_operator, selection_operator,
                                                  calFitness)

    # fitness, reject, cost, proc = calFitness_removeGPvalue(alpha, decision_best, chosing_best, network, request_test, vnf_list)

    # return fitness, reject, cost, proc, sum_gen, fitness_train, time_train, fitness_history
    return True