def checkChange(history):
    if len(history) < 10:
        return False
    last = history[-1]
    for value in history[-10:]:
        if value != last:
            return False
    return True

from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from read_data import *
from decision_var import Decision, Chosing
from network.network import Network
from utils import *
import time
import csv

data = Read_data(r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_centers_easy.json') 
request_list = data.get_R()
vnf_list = data.get_F()
node_list = data.get_V()
link_list = data.get_E()

network = Network()
network.add_node_to_network(node_list)
network.add_link_to_network(link_list)
server_list = network.MDC_nodes
node_list = network.get_node
link_list = network.links

max_delay = max_delay_vnf(server_list, vnf_list)
get_max_cost_vnf(server_list, vnf_list)

function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR()]
terminal_chosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR()]        

def deploy(network: Network, request: Request, chosing_indi : Individual, vnf_list, node_list, link_list):
    start_node = request.ingress
    end_node = request.egress
    bw = request.bw
    T = request.arrival
    request_cost = 0
    delay = 0
    update_deploy = []
    for VNF in request.VNFs:
        server_chosing = []
        for server in vnf_list[VNF].d_f.keys():
            server_node = server_find(node_list, server)
            n = 0
            path_delay = np.inf
            while path_delay == None or (path_delay > int(T)+ n - T):
                n = n+1
                if n == 10:
                    break
                path_delay, path = dijkstra(network, start_node, server, bw, int(T), int(T) + n, node_list )
            if n == 10:
                continue
            time_to_server = T + path_delay
            finished_server = vnf_list[VNF].d_f[server] + server_node.delay
            T1, T2 = get_time_slot(time_to_server, finished_server)
            state_server = server_node.get_state_server(T1, T2)
            if (state_server["cpu"] < vnf_list[VNF].c_f) or (state_server["mem"] < vnf_list[VNF].h_f) or (state_server["ram"]< vnf_list[VNF].r_f) or (time_to_server + finished_server > request.lifetime):
                 server_chosing.append((server, -np.inf , path,time_to_server+finished_server, np.inf))
            else:
                T3 = int(T)
                T4 = int(T) + n
                X = Chosing(server_node, T1, T2, path, path_delay, T3, T4, vnf_list[VNF], link_list)
                value_of_gp = chosing_indi.chromosomes.GetOutput(X)
                cost = server_node.get_cost(vnf_list[VNF])
                server_chosing.append((server, value_of_gp, path, time_to_server + finished_server, cost, T1, T2, T3, T4))
        server_chosing_sorted = sorted(server_chosing, key = lambda x: x[1], reverse = True)
        if len(server_chosing_sorted) == 0 or server_chosing_sorted[0][1] == -np.inf:
            return False, False
        else:
            request_cost = request_cost + server_chosing_sorted[0][4]
            T = server_chosing_sorted[0][3]
            used = {
                "mem_used": vnf_list[VNF].h_f,
                "cpu_used": vnf_list[VNF].c_f,
                "ram_used": vnf_list[VNF].r_f
            }
            update_deploy.append((server_chosing_sorted[0][0], server_chosing_sorted[0][5], server_chosing_sorted[0][6], used, server_chosing_sorted[0][2], bw, server_chosing_sorted[0][7], server_chosing_sorted[0][8]))
            start_node = server_chosing_sorted[0][0]
    path_delay, path = dijkstra(network, start_node, end_node, bw, int(T), int(T) + n, node_list )
    n = 0
    path_delay = np.inf
    while path_delay == None or (path_delay > int(T)+n - T):
        n = n+1
        if n == 10:
            break
        path_delay, path = dijkstra(network, start_node, end_node, bw, int(T), int(T) + n, node_list )
    if path_delay == None:
        return False, False
    else:
        update_deploy.append((None, None, None, None, path, bw, int(T), int(T) + n))
         
    return update_deploy, request_cost
            

def decision_gp(decision_indi: Individual, request: Request, T, network, vnf_list):
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)
    result  = decision_indi.chromosomes.GetOutput(X)
    del X
    return result
        


def calFitness(alpha, decision_indi, chosing_indi, network, request_list, vnf_list, node_list):
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    node_list_copy = deepcopy(node_list)
    server_list = network_copy.MDC_nodes
    link_list = network_copy.links
    sum_max_cost = get_max_cost_request(vnf_list, request_list_copy)
    sum_request = len(request_list_copy)
    T = 1
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
            update_state, cost = deploy(network_copy, re_de[0], chosing_indi, vnf_list, node_list_copy, link_list)
            if update_state == False:
                re_de[0].arrival = re_de[0].arrival + 1
                request_list_copy.append(re_de[0])
            else:
                cost_sum = cost_sum + cost
                for update_item in update_state:
                    if update_item[0] == None:
                        update_link_state(link_list, update_item[4], update_item[5], update_item[6], update_item[7])
                    else:
                        server_node = server_find(server_list, update_item[0])
                        server_node.add_used(update_item[1], update_item[2], update_item[3])
                        update_link_state(link_list, update_item[4], update_item[5], update_item[6], update_item[7])
            del update_state
        del request_processing        
        T = T + 1
    return alpha*reject/sum_request + (1-alpha)*cost_sum/sum_max_cost, reject, cost_sum

def trainGP(alpha, network, function, terminal_decision, terminal_chosing, node_list, link_list, vnf_list, request_list, pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    decision_pop = Population(pop_size, function, terminal_decision, min_height, max_height, initialization_max_height, evaluation)
    chosing_pop = Population(pop_size, function, terminal_chosing, min_height, max_height, initialization_max_height, evaluation)
    decision_pop.random_init()
    chosing_pop.random_init()
    decision_best = decision_pop.indivs[0]
    chosing_best = chosing_pop.indivs[0]
    for indi in decision_pop.indivs:
        indi.fitness, indi.reject, indi.cost = calFitness(alpha, indi, chosing_best, network, request_list, vnf_list, node_list)     
    for indi in chosing_pop.indivs:
        indi.fitness, indi.reject, indi.cost = calFitness(alpha, decision_best, indi, network, request_list, vnf_list, node_list)
    for i in range(max_gen):
        decision_offspring = decision_pop.reproduction(crossover_rate, mutation_rate)
        for indi in decision_offspring:
            indi.fitness, indi.reject, indi.cost = calFitness(alpha, indi, chosing_best, network, request_list, vnf_list, node_list)
        chosing_offspring = chosing_pop.reproduction(crossover_rate, mutation_rate)
        for indi in chosing_offspring:
            indi.fitness, indi.reject, indi.cost = calFitness(alpha, decision_best, indi, network, request_list, vnf_list, node_list)
        decision_pop.indivs.extend(decision_offspring)
        chosing_pop.indivs.extend(chosing_offspring)
        
        decision_pop.natural_selection()
        chosing_pop.natural_selection()
        
        if decision_pop.indivs[0].fitness < decision_best.fitness:
            decision_best = decision_pop.indivs[0]
        if chosing_pop.indivs[0].fitness < chosing_best.fitness:
            chosing_best = chosing_pop.indivs[0]
            
        decision_pop.history.append(decision_pop.indivs[0].fitness)
        chosing_pop.history.append(chosing_pop.indivs[0].fitness)
        if checkChange(decision_pop.history) == True and checkChange(chosing_pop.history) == True:
            break   
    return decision_best, chosing_best
        

# request_train = []
# request_test = []
# for request in request_list:
#     if request.arrival <= 20:
#         request_train.append(request)
#     else: 
#         request_test.append(request)


# start_time = time.time()
# decision_best, chosing_best = trainGP(0.5, network, function, terminal_decision, terminal_chosing, node_list, link_list, vnf_list, request_train, 5, 2, 8, 4, 10, 10, 0.8, 0.1)
# print("Thoi gian train", time.time() - start_time)
# print(decision_best.fitness, chosing_best.fitness)
# print(decision_best.chromosomes.GetHumanExpression())
# print(chosing_best.chromosomes.GetHumanExpression())

# start_time = time.time()
# fitness, reject, cost = calFitness(0.5, decision_best, chosing_best, network, request_test, vnf_list, node_list)
# print("Thoi gian test", time.time() - start_time)
# print("Result: ")
# print(fitness, reject, cost)

data_path = [r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_centers_easy.json',r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_centers_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_rural_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_rural_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_uniform_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_uniform_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_urban_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\nsf_urban_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_centers_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_centers_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_rural_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_rural_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_uniform_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_uniform_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_urban_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\conus_urban_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_centers_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_centers_hard.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_rural_easy.json', r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_rural_hard.json']

for path in data_path:
    data = Read_data(path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_list = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_list)
    server_list = network.MDC_nodes
    node_list = network.get_node
    link_list = network.links

    max_delay = max_delay_vnf(server_list, vnf_list)
    get_max_cost_vnf(server_list, vnf_list)

    function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
    terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR()]
    terminal_chosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR()]
    
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= 10:
            request_train.append(request)
        else: 
            request_test.append(request)

    result ={}
    result['dataset'] = path[80:-5]
    start_time = time.time()
    decision_best, chosing_best = trainGP(0.5, network, function, terminal_decision, terminal_chosing, node_list, link_list, vnf_list, request_train, 50, 2, 8, 4, 10, 50, 0.8, 0.1)
    # print("Thoi gian train", time.time() - start_time)
    # print(decision_best.fitness, chosing_best.fitness)
    # print(decision_best.chromosomes.GetHumanExpression())
    # print(chosing_best.chromosomes.GetHumanExpression())
    result["Train time"] = time.time() - start_time

    start_time = time.time()
    fitness, reject, cost = calFitness(0.5, decision_best, chosing_best, network, request_test, vnf_list, node_list)
    # print("Thoi gian test", time.time() - start_time)
    # print("Result: ")
    # print(fitness, reject, cost)
    result["Test time"] = time.time() - start_time
    result["fitness"] = fitness
    result["reject"] = reject
    result["cost"] = cost
    with open ("result1.csv", "a") as f:
        fieldnames = ['dataset', 'Train time', 'Test time', 'fitness', 'reject', 'cost']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(result)