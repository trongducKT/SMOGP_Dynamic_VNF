from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from data_info.read_data import *
from network.network import Network
from utils.utils import *
from .train import *
from deployment.evaluation import *
# Heuristic 1: Random for determining policy and Random for choosing policy
def heuristic1(data_path, alpha, num_train):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)

    get_max_cost_vnf(network.MDC_nodes, vnf_list)
    
    determining_indi = Individual(Rand())
    choosing_indi = Individual(Rand())
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    fitness, reject, cost, proc = calFitness(alpha, determining_indi, choosing_indi, network, request_test, vnf_list)

    return fitness, reject, cost, proc  




# Heuristic 2: Random for determining policy and min_cost for choosing policy
def heuristic2(data_path, alpha, num_train):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)

    get_max_cost_vnf(network.MDC_nodes, vnf_list)
    
    determining_indi = Individual(Rand())
    choosing_indi = Individual(MinCost())
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    fitness, reject, cost, proc = calFitness(alpha, determining_indi, choosing_indi, network, request_test, vnf_list)

    return fitness, reject, cost, proc    
    
# Heuristic 3: Due date for determining policy and min_cost for choosing policy
def heuristic3(data_path, alpha, num_train):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
    
    determining_indi = Individual(MinDD())
    choosing_indi = Individual(MinCost())
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    fitness, reject, cost, proc = calFitness(alpha, determining_indi, choosing_indi, network, request_test, vnf_list)

    return fitness, reject, cost, proc


#Heuristic 4: FIFO/Relax
def heuristic4(data_path, alpha, num_train):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
    
    determining_indi = Individual(Rand())
    choosing_indi = Individual(Relax())
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    fitness, reject, cost, proc = calFitness(alpha, determining_indi, choosing_indi, network, request_test, vnf_list)

    return fitness, reject, cost, proc   

def heuristic5(data_path, alpha, num_train):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
    
    determining_indi = Individual(FIFO_DD())
    choosing_indi = Individual(MinCost())
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    fitness, reject, cost, proc = calFitness(alpha, determining_indi, choosing_indi, network, request_test, vnf_list)

    return fitness, reject, cost, proc  


def heuristic6(data_path, alpha, num_train):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
    
    determining_indi = Individual(MinDD())
    choosing_indi = Individual(CS_Relax())
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    fitness, reject, cost, proc = calFitness(alpha, determining_indi, choosing_indi, network, request_test, vnf_list)

    return fitness, reject, cost, proc