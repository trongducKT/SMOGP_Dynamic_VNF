from gp.node.function import *
from gp.node.terminal import *
# from gp.population.gp import *
from gp.population.individual import *
from data_info.read_data import *
from utils.utils import *
from .deploy_request import *

def calFitness(indi, network, request_list, vnf_list):
    # storing processing history
    processing_history ={}
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    sum_max_cost = get_max_cost_request(vnf_list, request_list_copy) # max cost of all request
    sum_request = len(request_list_copy)

    # Execution time slot
    T = request_list_copy[0].arrival
    reject = 0 # number of reject request
    cost_sum = 0 # sum of cost of all request that excuted 
    while len(request_list_copy) > 0:
        request_processing, reject_request, reject1 = get_request_run(request_list_copy, 0, T)
        for request in request_processing:
            request_list_copy.remove(request)
        for request in reject_request:
            request_list_copy.remove(request)
        reject = reject + reject1

        request_decision = []
        # Calculate value of GP for each request
        for request in request_processing:
            value_of_gp = decision_gp(indi, request, T, network_copy, vnf_list)
            # print("Gia tri GP ở biến decision: ", value_of_gp)
            request_decision.append((request, value_of_gp))
        request_decision = sorted(request_decision, key = lambda x: x[1], reverse = True)

        for re_de in request_decision:
            update_state, cost, hanhtrinh = deploy(network_copy, re_de[0], indi, vnf_list)
            if update_state == False:
                re_de[0].arrival = re_de[0].arrival + 1
                re_de[0].push_number = re_de[0].push_number + 1
                request_list_copy.insert(0,re_de[0])
            else:
                processing_history[re_de[0].name] ={ 
                    "Time slot": T,
                    "Path": hanhtrinh
                                                    }
                cost_sum = cost_sum + cost
                for update_item in update_state:
                    if update_item[0] == None:
                        update_link_state(network_copy.links, update_item[4], update_item[5], update_item[6], update_item[7])
                    else:
                        server_node = server_find(network_copy.get_node, update_item[0])
                        server_node.add_used(update_item[1], update_item[2], update_item[3])
                        update_link_state(network_copy.links, update_item[4], update_item[5], update_item[6], update_item[7])
       
        T = T + 1
    return reject/sum_request, cost_sum/sum_max_cost, reject, cost_sum, processing_history

def calFitness_removeGPvalue(indi: Individual, network, request_list, vnf_list):
    # storing processing history
    processing_history ={}
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    sum_max_cost = get_max_cost_request(vnf_list, request_list_copy) # max cost of all request
    sum_request = len(request_list_copy)

    # Execution time slot
    T = request_list_copy[0].arrival
    reject = 0 # number of reject request
    cost_sum = 0 # sum of cost of all request that excuted 
    while len(request_list_copy) > 0:
        request_processing, reject_request, reject1 = get_request_run(request_list_copy, 0, T)
        for request in request_processing:
            request_list_copy.remove(request)
        for request in reject_request:
            request_list_copy.remove(request)
        reject = reject + reject1

        request_decision = []
        # Calculate value of GP for each request
        for request in request_processing:
            value_of_gp = decision_gp(indi, request, T, network_copy, vnf_list)
            if value_of_gp < 0:
                reject = reject + 1
                continue
            request_decision.append((request, value_of_gp))
        request_decision = sorted(request_decision, key = lambda x: x[1], reverse = True)

        for re_de in request_decision:
            update_state, cost, hanhtrinh = deploy(network_copy, re_de[0], indi, vnf_list)
            if update_state == False:
                re_de[0].arrival = re_de[0].arrival + 1
                re_de[0].push_number = re_de[0].push_number + 1
                request_list_copy.insert(0,re_de[0])
            else:
                processing_history[re_de[0].name] ={ 
                    "Time slot": T,
                    "Path": hanhtrinh
                                                    }
                cost_sum = cost_sum + cost
                for update_item in update_state:
                    if update_item[0] == None:
                        update_link_state(network_copy.links, update_item[4], update_item[5], update_item[6], update_item[7])
                    else:
                        server_node = server_find(network_copy.get_node, update_item[0])
                        server_node.add_used(update_item[1], update_item[2], update_item[3])
                        update_link_state(network_copy.links, update_item[4], update_item[5], update_item[6], update_item[7])
       
        T = T + 1
    return reject/sum_request, cost_sum/sum_max_cost, reject, cost_sum, processing_history