# from gp.population.gp import *
from gp.population.individual import *
from data_info.read_data import *
from priority_gp.decision_var import Decision, Choosing
from network.network import Network
from utils.utils import *
from .gen_pc import Determining_Surrogate,Server_Surrogate, Request_Surrogate, Ref_Rule, Surrogate
import random
# deploy a request
def deploy(network: Network, request: Request, indi : Individual, vnf_list):
    server_surrogate_list = []
    start_node = request.ingress
    end_node = request.egress
    bw = request.bw
    T = request.arrival
    lifetime = request.lifetime
    network_copy = deepcopy(network)
    request_cost = 0
    
    update_deploy = []
    sum_delay = 0
    
    for VNF in request.VNFs:
        surrogate_VNF = []
        server_chosing = []
        for server in vnf_list[VNF].d_f.keys():
            if vnf_list[VNF].d_f[server] >= request.lifetime - request.arrival:
                continue
            server_node = server_find(network_copy.get_node, server)
            n = 0
            path_delay = np.inf
            while path_delay == None or (path_delay > int(T) + n - T):
                n = n + 1
                path_delay, path = dijkstra(network_copy, start_node, server, bw, int(T), int(T) + n, network_copy.get_node )
                if n >= int(lifetime - T):
                    break
        
            if n >= int(lifetime - T):
                continue
            if path_delay == None or path == None:
                continue
            server_node = server_find(network_copy.get_node, server)
            time_to_server = T + path_delay     # Time to server
            finished_server = vnf_list[VNF].d_f[server] + server_node.delay     #Time to finish on server
            T1, T2 = get_time_slot(time_to_server, finished_server)     #Duration of using server
    
            state_server = server_node.get_state_server(T1, T2)     #State of server in duration (T1, T2)

            if (state_server["cpu"] < vnf_list[VNF].c_f) or (state_server["mem"] < vnf_list[VNF].h_f) or (state_server["ram"]< vnf_list[VNF].r_f) or (time_to_server + finished_server > request.lifetime):
                continue
            else:
                T3 = int(T)
                T4 = int(T) + n
                # T3, T4 = get_time_slot(T, path_delay)     #Duration of using link
                X = Choosing(server_node, T1, T2, path, path_delay, T3, T4, vnf_list[VNF], network_copy.links, request.lifetime)
                value_of_gp = indi.choosing_tree.GetOutput(X)
                se_surrogate = Server_Surrogate(X.server_state["cpu"]/X.cpu_capacity, X.server_state["ram"]/X.ram_capacity, X.server_state["mem"]/X.mem_capacity, 
                                                X.MLU, X.cost, X.delay/X.request_lifetime, 1-X.MRU["cpu"], 1-X.MRU["ram"], 1-X.MRU["mem"])
                surrogate_VNF.append(se_surrogate)
                cost = server_node.get_cost(vnf_list[VNF])
                server_chosing.append((server, value_of_gp, path, time_to_server + finished_server, cost, T1, T2, T3, T4))
        server_chosing_sorted = sorted(server_chosing, key = lambda x: x[1], reverse = True)
        
        if len(surrogate_VNF) > 0:
            server_surrogate_list.append(surrogate_VNF)
        if len(server_chosing_sorted) == 0 or server_chosing_sorted[0][1] == -np.inf:
            #print("Khong tim duoc server")
            return False, False, False
        else:
            request_cost = request_cost + server_chosing_sorted[0][4]
            T = server_chosing_sorted[0][3]
            sum_delay = T
            used = {
                "mem_used": vnf_list[VNF].h_f,
                "cpu_used": vnf_list[VNF].c_f,
                "ram_used": vnf_list[VNF].r_f
            }
            update_deploy.append((server_chosing_sorted[0][0], server_chosing_sorted[0][5], server_chosing_sorted[0][6], used, server_chosing_sorted[0][2], bw, server_chosing_sorted[0][7], server_chosing_sorted[0][8]))
            start_node = server_chosing_sorted[0][0]
            update_link_state(network_copy.links, server_chosing_sorted[0][2], bw , server_chosing_sorted[0][5], server_chosing_sorted[0][6])
            server_node = server_find(network_copy.get_node, server_chosing_sorted[0][0])
            server_node.add_used(server_chosing_sorted[0][5], server_chosing_sorted[0][6], used)
    n = 0
    path_delay = np.inf
    while path_delay == None or (path_delay > int(T)+n - T):
        n = n+1
        if n >= int(lifetime - T):
            break
        path_delay, path = dijkstra(network_copy, start_node, end_node, bw, int(T), int(T) + n, network_copy.get_node)
        if n >= int(lifetime - T):
            break
    if path_delay == None or path_delay == np.inf:
        return False, False, server_surrogate_list
    else:
        T3, T4 = get_time_slot(T, path_delay)
        sum_delay = sum_delay + path_delay
        update_deploy.append((None, None, None, None, path, bw, T3, T4)) 
    if sum_delay >= request.lifetime:
        return False, False, server_surrogate_list
     
    return update_deploy, request_cost, server_surrogate_list

def determining_gp(indi: Individual, request: Request, T, network, vnf_list):
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)


    ARS_value = 0
    for vnf in X.r.VNFs:
        ARS_value += X.VNFs_resource[vnf]["ram"]
    ARS_value = ARS_value/len(X.r.VNFs)


    ACS_value = 0
    for vnf in X.r.VNFs:
        ACS_value += X.VNFs_resource[vnf]["cpu"]
    ACS_value = ACS_value/len(X.r.VNFs)

    AMS_value = 0
    for vnf in X.r.VNFs:
        AMS_value += X.VNFs_resource[vnf]["mem"]
    AMS_value = AMS_value/len(X.r.VNFs)

    MDR_value = 0
    for vnf in X.r.VNFs:
        MDR_value += X.VNF_max_delay[vnf]
    MDR_value = MDR_value/X.r.lifetime
    request_surrogate = Determining_Surrogate((X.r.lifetime - X.T)/X.r.lifetime, X.r.bw, X.VNFs_request_resource["ram"], X.VNFs_request_resource["cpu"],
                                              X.VNFs_request_resource["mem"], X.first_VNF_requirement["ram"], X.first_VNF_requirement["cpu"], X.first_VNF_requirement["mem"],
                                              X.VNFs_resource[X.r.VNFs[0]]["ram"], X.VNFs_resource[X.r.VNFs[0]]["cpu"], X.VNFs_resource[X.r.VNFs[0]]["mem"],
                                              ARS_value, ACS_value, AMS_value, MDR_value, X.r.push_number/X.r.lifetime)
    result  = indi.determining_tree.GetOutput(X)
    return result, request_surrogate

def ordering_gp(indi: Individual, request: Request, T, network, vnf_list):
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)


    ARS_value = 0
    for vnf in X.r.VNFs:
        ARS_value += X.VNFs_resource[vnf]["ram"]
    ARS_value = ARS_value/len(X.r.VNFs)


    ACS_value = 0
    for vnf in X.r.VNFs:
        ACS_value += X.VNFs_resource[vnf]["cpu"]
    ACS_value = ACS_value/len(X.r.VNFs)

    AMS_value = 0
    for vnf in X.r.VNFs:
        AMS_value += X.VNFs_resource[vnf]["mem"]
    AMS_value = AMS_value/len(X.r.VNFs)

    MDR_value = 0
    for vnf in X.r.VNFs:
        MDR_value += X.VNF_max_delay[vnf]
    MDR_value = MDR_value/X.r.lifetime
    request_surrogate = Determining_Surrogate((X.r.lifetime - X.T)/X.r.lifetime, X.r.bw, X.VNFs_request_resource["ram"], X.VNFs_request_resource["cpu"],
                                              X.VNFs_request_resource["mem"], X.first_VNF_requirement["ram"], X.first_VNF_requirement["cpu"], X.first_VNF_requirement["mem"],
                                              X.VNFs_resource[X.r.VNFs[0]]["ram"], X.VNFs_resource[X.r.VNFs[0]]["cpu"], X.VNFs_resource[X.r.VNFs[0]]["mem"],
                                              ARS_value, ACS_value, AMS_value, MDR_value, X.r.push_number/X.r.lifetime)
    result  = indi.determining_tree.GetOutput(X)
    return result, request_surrogate

def store_event(indi: Individual, network, request_list, vnf_list):
    # storing processing history
    request_surrogate = []
    server_surrogate = []
    determining_surrogate = []

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
        request_surrogate_item = []
        for request in request_processing:
            value_of_determining_gp, det_sur_item = determining_gp(indi, request, T, network_copy, vnf_list)
            determining_surrogate.append(det_sur_item)
            if value_of_determining_gp < 0:
                reject = reject + 1
                continue
            value_of_ordering_gp, re_sur_item = ordering_gp(indi, request, T, network_copy, vnf_list)
            request_surrogate_item.append(re_sur_item)
            request_decision.append((request, value_of_ordering_gp))
        request_decision = sorted(request_decision, key = lambda x: x[1], reverse = True)

        for re_de in request_decision:
            update_state, cost, ser_sur_item = deploy(network_copy, re_de[0], indi, vnf_list)
            if ser_sur_item != False:
                server_surrogate.extend(ser_sur_item)
            if update_state == False:
                re_de[0].arrival = re_de[0].arrival + 1
                re_de[0].push_number = re_de[0].push_number + 1
                request_list_copy.insert(0,re_de[0])
            else:
                cost_sum = cost_sum + cost
                for update_item in update_state:
                    if update_item[0] == None:
                        update_link_state(network_copy.links, update_item[4], update_item[5], update_item[6], update_item[7])
                    else:
                        server_node = server_find(network_copy.get_node, update_item[0])
                        server_node.add_used(update_item[1], update_item[2], update_item[3])
                        update_link_state(network_copy.links, update_item[4], update_item[5], update_item[6], update_item[7])
       
        T = T + 1
        if len(request_surrogate_item) > 0:
            request_surrogate.append(request_surrogate_item)
    return determining_surrogate, request_surrogate, server_surrogate

def gen_surrogate(data_path, num_train, num_surrogate, ref_rule: Ref_Rule):
    indi = Individual(ref_rule.determinig_rule, ref_rule.ordering_rule, ref_rule.choosing_rule)
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
    
    determing_surrogate, request_surrogate, server_surrogate = store_event(indi, network, request_train, vnf_list)
    surrogate = Surrogate(num_surrogate, ref_rule)

    surrogate.determining_situations = []
    surrogate.ordered_situations = []
    surrogate.server_situations = []
    index_list = np.random.choice(len(request_surrogate), num_surrogate, replace = False)
    for index in index_list:
        surrogate.ordered_situations.append(request_surrogate[index])
    index_list = np.random.choice(len(server_surrogate), num_surrogate, replace = False)
    for index in index_list:
        surrogate.server_situations.append(server_surrogate[index])
    # request_surrogate.sort(key = lambda x: len(x), reverse= True)
    # server_surrogate.sort(key = lambda x: len(x), reverse= True)
    surrogate.determining_situations = random.sample(determing_surrogate, num_surrogate)
    # surrogate.ordered_situations = request_surrogate[:num_surrogate]
    # surrogate.server_situations = server_surrogate[:num_surrogate]
    return surrogate