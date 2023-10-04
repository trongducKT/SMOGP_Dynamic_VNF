from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from read_data import *
from decision_var import Decision, Chosing
from network.network import Network
from utils import *
import time 
import multiprocessing     
import csv
import numba as nb
import random


# deploy a request
def deploy(network: Network, request: Request, chosing_indi : Individual, vnf_list):
    hanhtrinh = []
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
                if n == 10:
                    break
        
            if n == 10:
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
                X = Chosing(server_node, T1, T2, path, path_delay, T3, T4, vnf_list[VNF], network_copy.links)
                value_of_gp = chosing_indi.chromosomes.GetOutput(X)

                cost = server_node.get_cost(vnf_list[VNF])
                server_chosing.append((server, value_of_gp, path, time_to_server + finished_server, cost, T1, T2, T3, T4))
        server_chosing_sorted = sorted(server_chosing, key = lambda x: x[1], reverse = True)
        
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
            hanhtrinh.extend(server_chosing_sorted[0][2])
    n = 0
    path_delay = np.inf
    while path_delay == None or (path_delay > int(T)+n - T):
        n = n+1
        if n == 10:
            break
        path_delay, path = dijkstra(network_copy, start_node, end_node, bw, int(T), int(T) + n, network_copy.get_node)
        if n == 10:
            break
    if path_delay == None or path_delay == np.inf:
        return False, False, False
    else:
        T3, T4 = get_time_slot(T, path_delay)
        sum_delay = sum_delay + path_delay
        update_deploy.append((None, None, None, None, path, bw, T3, T4)) 
        hanhtrinh.extend(path)
    if sum_delay >= request.lifetime:
        return False, False, False
     
    return update_deploy, request_cost, hanhtrinh

def decision_gp(decision_indi: Individual, request: Request, T, network, vnf_list):
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)
    result  = decision_indi.chromosomes.GetOutput(X)
    return result
        

def calFitness(alpha, decision_indi, chosing_indi, network, request_list, vnf_list):
    processing_history ={}
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    sum_max_cost = get_max_cost_request(vnf_list, request_list_copy)
    sum_request = len(request_list_copy)
#     print("sum_max_cost",sum_max_cost)
#     print("sum_request", sum_request)
    T = request_list_copy[0].arrival
    reject = 0
    cost_sum = 0
    while len(request_list_copy) > 0:
        request_processing, reject_request, reject1 = get_request_run(request_list_copy, 0, T)
        for request in request_processing:
            request_list_copy.remove(request)
        for request in reject_request:
            request_list_copy.remove(request)
        reject = reject+ reject1

        request_decision = []
        for request in request_processing:
            value_of_gp = decision_gp(decision_indi, request, T, network_copy, vnf_list)

            request_decision.append((request, value_of_gp))
        request_decision = sorted(request_decision, key = lambda x: x[1], reverse = True)

        for re_de in request_decision:
            update_state, cost, hanhtrinh = deploy(network_copy, re_de[0], chosing_indi, vnf_list)
            if update_state == False:
                re_de[0].arrival = re_de[0].arrival + 1
                request_list_copy.insert(0,re_de[0])
                re_de[0].push_number = re_de[0].push_number + 1
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
    # for T in range (12):
    #     print(network_copy.get_conflict_server(T))
    #     print(network_copy.get_conflict_link(T))
    return alpha*reject/sum_request + (1-alpha)*cost_sum/sum_max_cost, reject, cost_sum, processing_history

def trainGP(processing_number, alpha, network, function, terminal_decision, terminal_chosing, vnf_list, request_list, pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    fitness_history = {}
    fitness_history["decision"] = []
    fitness_history["chosing"] = []
    time_start = time.time()
    
    decision_pop = Population(pop_size -1, function, terminal_decision, min_height, max_height, initialization_max_height, evaluation)
    chosing_pop = Population(pop_size -1, function, terminal_chosing, min_height, max_height, initialization_max_height, evaluation)
    
    decision_pop.random_init()
    chosing_pop.random_init()
    
    
    node1 = MinDD()
    node2 = Scale()
    node3 = MinCost()
    node4 = Scale()
    func1 = AddNode()
    func2 = AddNode()
    
    func1.AppendChild(node1)
    func1.AppendChild(node2)
    func2.AppendChild(node3)
    func2.AppendChild(node4) 
    indi1 = Individual(func1)
    indi2 = Individual(func2)  
    decision_pop.indivs.append(indi1)
    chosing_pop.indivs.append(indi2)
    
    decision_best = decision_pop.indivs[0]
    chosing_best = chosing_pop.indivs[0]
    
    
    print("Khoi tao xong")
#     for indi in decision_pop.indivs:
#         print(indi.chromosomes.GetHumanExpression())
#     time.sleep(10)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in decision_pop.indivs:
#         chosing_best_random = random.choice(chosing_pop.indivs)
        arg.append((alpha, indi, chosing_best, network, request_list, vnf_list))
    for indi in chosing_pop.indivs:
#         decision_best_random = random.choice(decision_pop.indivs)
        arg.append((alpha, decision_best, indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    len_decision = len(decision_pop.indivs)
    for indi, value in zip(decision_pop.indivs, result[0: len_decision]):
        indi.fitness, indi.reject, indi.cost, a = value

    for indi, value in zip(chosing_pop.indivs, result[len_decision:]):
        indi.fitness, indi.reject, indi.cost, a = value
    print("Tinh fitness khoi tạo xong")   

    sum_gen = 0   
    for i in range(max_gen):
        decision_offspring = decision_pop.reproduction(crossover_rate, mutation_rate)
        chosing_offspring = chosing_pop.reproduction(crossover_rate, mutation_rate)
        
    
        arg = []
        for indi in decision_offspring:
#             chosing_best_random = random.choice(chosing_pop.indivs)
            arg.append((alpha, indi, chosing_best, network, request_list, vnf_list))
        for indi in chosing_offspring:
#             decision_best_random = random.choice(decision_pop.indivs)
            arg.append((alpha, decision_best, indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        len_decision_off = len(decision_offspring)
        for indi, value in zip(decision_offspring, result[: len_decision_off]):
            indi.fitness, indi.reject, indi.cost, a = value
        for indi, value in zip(chosing_offspring, result[len_decision_off:]):
            indi.fitness, indi.reject, indi.cost, a = value

        decision_pop.indivs.extend(decision_offspring)
        chosing_pop.indivs.extend(chosing_offspring)
#         print(len(decision_pop.indivs))
#         time.sleep(10)
        
        decision_pop.natural_selection()
#         print(len(decision_pop.indivs))
        chosing_pop.natural_selection()
        print("The he", i)
#         for indi in decision_pop.indivs:
#             print("Decision",indi.fitness, indi.chromosomes.GetHumanExpression())
#         for indi in chosing_pop.indivs:
#             print("Chosing",indi.fitness, indi.chromosomes.GetHumanExpression())        
        if decision_pop.indivs[0].fitness < decision_best.fitness:
            decision_best = decision_pop.indivs[0]
        if chosing_pop.indivs[0].fitness < chosing_best.fitness:
            chosing_best = chosing_pop.indivs[0]
            
        decision_pop.history.append(decision_pop.indivs[0].fitness)
        chosing_pop.history.append(chosing_pop.indivs[0].fitness)
        sum_gen = i+1
        print("The he ",i)
        print("Decision",decision_best.fitness)
        print("Chosing",chosing_best.fitness)
        fitness_history["decision"].append(decision_best.fitness)
        fitness_history["chosing"].append(chosing_best.fitness)
        if checkChange(decision_pop.history) == True and checkChange(chosing_pop.history) == True:
            break    
    pool.close()              
    return decision_best, chosing_best, sum_gen, decision_best.fitness, time.time()-time_start, fitness_history  


# Proposed algorithm

def run_proposed(data_path, processing_num, alpha, num_train,  pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)

    get_max_cost_vnf(network.MDC_nodes, vnf_list)

    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode(), SinNode(), CosNode(), PowNode()]
    terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
    terminal_chosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR(), Const()]
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)

    decision_best, chosing_best, sum_gen, fitness_train, time_train, fitness_history = trainGP(processing_num, alpha, network, function, terminal_decision, terminal_chosing, vnf_list, request_train, pop_size, min_height, max_height, initialization_max_height, evaluation, max_gen, crossover_rate, mutation_rate)

    fitness, reject, cost, proc = calFitness(alpha, decision_best, chosing_best, network, request_test, vnf_list)

    return fitness, reject, cost, proc, sum_gen, fitness_train, time_train, fitness_history



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
    