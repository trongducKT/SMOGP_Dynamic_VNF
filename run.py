from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from read_data import *
from decision_var import Decision, Chosing
from network.network import Network
from utils import *
import time

data = Read_data(r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_centers_hard.json') 
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


# pop = Population(10, function, terminal_chosing, 2, 8, 8, 100)
# pop.random_init()
# print(pop.indivs[0].chromosomes.GetHumanExpression())

# r = request_list[0]

# vnf_source = VNFs_resource_max(server_list, vnf_list, 0)
# print(vnf_source)
# X = Decision(r, 1, vnf_source, max_delay, vnf_list)
# fitness = pop.indivs[0].chromosomes.GetOutput(X)
# print(fitness)

# print(server_list[0].get_cost(vnf_list[4]))

def deploy(network: Network, request: Request, chosing_indi : Individual, vnf_list, node_list, link_list):
    #print("deploy")
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
    #start_time = time.time()
    path_delay, path = dijkstra(network, start_node, end_node, bw, int(T), int(T) + n, node_list )
    #print("Time to find path: ", time.time() - start_time)
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
    #print("decision_gp")
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)
    result  = decision_indi.chromosomes.GetOutput(X)
    del X
    return result
        


def calFitness(alpha, decision_indi, chosing_indi, network, request_list, vnf_list, node_list):
    #print("calFitness_decision")
    start_time = time.time()
    network_copy = deepcopy(network)
    request_list_copy = deepcopy(request_list)
    node_list_copy = deepcopy(node_list)
    server_list = network_copy.MDC_nodes
    link_list = network_copy.links
    #print("Time to copy: ", time.time() - start_time)
    sum_max_cost = get_max_cost_request(vnf_list, request_list_copy)
    sum_request = len(request_list_copy)
    T = 1
    reject = 0
    cost_sum = 0
    start_time = time.time()
    while len(request_list_copy) > 0:
        request_processing, reject_request, reject1 = get_request_run(request_list_copy, 0, T)
       # print(len(request_list_copy))
        for request in request_processing:
            request_list_copy.remove(request)
       # print("Sau khi xoa", len(request_list_copy))
        for request in reject_request:
            request_list_copy.remove(request)
       # print(len(request_processing), len(request_list_copy))
        reject = reject+ reject1
        request_decision = []
        #start_time = time.time()
       # print(len(request_processing))
        for request in request_processing:
            #start_time = time.time()
            value_of_gp = decision_gp(decision_indi, request, T, network_copy, vnf_list)
            #print("Time to find decision: ", time.time() - start_time)
            request_decision.append((request, value_of_gp))
        request_decision = sorted(request_decision, key = lambda x: x[1], reverse = True)
        #print("Time to find decision: ", time.time() - start_time)
        ####################################################
        start_time = time.time()
        #print(len(request_decision))
        for re_de in request_decision:
            start_time = time.time()
            update_state, cost = deploy(network_copy, re_de[0], chosing_indi, vnf_list, node_list_copy, link_list)
            #print("deploy:", time.time()-start_time)
            # print(cost)
            start_time = time.time()
            if update_state == False:
                re_de[0].arrival = re_de[0].arrival + 1
                request_list_copy.append(re_de[0])
            else:
                cost_sum = cost_sum + cost
                #print(update_state)
                for update_item in update_state:
                    if update_item[0] == None:
                        update_link_state(link_list, update_item[4], update_item[5], update_item[6], update_item[7])
                    else:
                        server_node = server_find(server_list, update_item[0])
                        #print("Update", update_item[0],update_item[1], update_item[2], update_item[3])
                        #print(server_node.used)
                        server_node.add_used(update_item[1], update_item[2], update_item[3])
                        #print(server_node.used)
                        update_link_state(link_list, update_item[4], update_item[5], update_item[6], update_item[7])
           # print("Time to update: ", time.time() - start_time)
            del update_state
        #print("for:", time.time()-start_time)
        #####################################################print("for:", time.time()-start_time)
        del request_processing        
        T = T + 1
    # for T in range (50):
    #     print(T)
    #     print(network_copy.get_conflict_link(T))
    #     print(network_copy.get_conflict_server(T))
    # for link in network_copy.links:
    #     print(link.u.name, link.v.name)
    #     for T in range(50):
    #         print(link.get_state_link(T))
    #print("Time to deploy: ", time.time() - start_time)
    # del network_copy
    # del request_list_copy
    # del node_list_copy 
    # del server_list
    # del vnf_list
    # del link_list
    return alpha*reject/sum_request + (1-alpha)*cost_sum/sum_max_cost, reject, cost_sum

def trainGP(alpha, network, function, terminal_decision, terminal_chosing, node_list, link_list, vnf_list, request_list, pop_size, min_height, max_height, initialization_max_height,  evaluation, max_gen, crossover_rate, mutation_rate):
    decision_pop = Population(pop_size, function, terminal_decision, min_height, max_height, initialization_max_height, evaluation)
    chosing_pop = Population(pop_size, function, terminal_chosing, min_height, max_height, initialization_max_height, evaluation)
    decision_pop.random_init()
    chosing_pop.random_init()
    decision_best = decision_pop.indivs[0]
    chosing_best = chosing_pop.indivs[0]
    
    # decision_best.fitness, decision_best.reject, decision_best.cost = calFitness_decision(alpha, decision_best, chosing_best, network, request_list, vnf_list, node_list)
    # chosing_best.fitness, chosing_best.reject, chosing_best.cost = calFitness_decision(alpha, decision_best, chosing_best, network, request_list, vnf_list, node_list)
    #print("Xong khoi tao")
    for indi in decision_pop.indivs:
        indi.fitness, indi.reject, indi.cost = calFitness(alpha, indi, chosing_best, network, request_list, vnf_list, node_list) 
        #print("Xong ca the indi_decision")
    #print("Xong decision")        

    
    for indi in chosing_pop.indivs:
        indi.fitness, indi.reject, indi.cost = calFitness(alpha, decision_best, indi, network, request_list, vnf_list, node_list)
        #print("Xong ca the indi")
    #print("Xong chosing")
    for i in range(max_gen):
        #print("The he: ", i)
        start_time = time.time()
        decision_offspring = decision_pop.reproduction(crossover_rate, mutation_rate)
        #print("Time to reproduction: ", time.time() - start_time)
        for indi in decision_offspring:
            start_time = time.time()
            indi.fitness, indi.reject, indi.cost = calFitness(alpha, indi, chosing_best, network, request_list, vnf_list, node_list)
            #print(indi.chromosomes.GetHumanExpression())
            #print("Time to cal fitness: ", time.time() - start_time)
        chosing_offspring = chosing_pop.reproduction(crossover_rate, mutation_rate)
        for indi in chosing_offspring:
            indi.fitness, indi.reject, indi.cost = calFitness(alpha, decision_best, indi, network, request_list, vnf_list, node_list)
            print(indi.chromosomes.GetHumanExpression())
            print(indi.fitness, indi.reject, indi.cost)
        decision_pop.indivs.extend(decision_offspring)
        chosing_pop.indivs.extend(chosing_offspring)
        
        decision_pop.natural_selection()
        chosing_pop.natural_selection()
        print(decision_pop.indivs[-1].fitness, chosing_pop.indivs[-1].fitness)
        if decision_pop.indivs[0].fitness > decision_best.fitness:
            decision_best = decision_pop.indivs[0]
        if chosing_pop.indivs[0].fitness > chosing_best.fitness:
            chosing_best = chosing_pop.indivs[0]
        print("The he: ", i)
        print(decision_best.fitness, chosing_best.fitness)    
    return decision_best, chosing_best
        
        
    

   
# pop = Population(10, function, terminal_chosing, 2, 8, 4, 100)
# pop.random_init()

# pop1 = Population(10, function, terminal_decision, 2, 8, 4, 100)
# pop1.random_init()

# decision_indi = pop1.indivs[0]
# chosing_indi = pop.indivs[0]

# update_state, cost = deploy(network, request_list[3], pop.indivs[1], vnf_list, node_list, link_list)
# print(update_state)
# print(cost)

# shortest_delay, path = dijkstra(network, 67, 17, 0.5, 1,3, node_list)
# print(f"Shortest delay from 40 to 1 with bandwidth requirement 0: {shortest_delay}")
# print(path)
request_train = []
request_test = []
for request in request_list:
    if request.arrival <= 20:
        request_train.append(request)
    else: 
        request_test.append(request)
# print("Result:")
# print(len(request_train)) 
# fitness, reject, cost_sum = calFitness_decision(0.5, decision_indi, chosing_indi, network, request_train, vnf_list, node_list)
# print(fitness)
# print(reject)
# print(cost_sum)

start_time = time.time()
decision_best, chosing_best = trainGP(0.5, network, function, terminal_decision, terminal_chosing, node_list, link_list, vnf_list, request_train, 10, 2, 8, 4, 50, 10, 0.8, 0.1)
print("Thoi gian train", time.time() - start_time)
print(decision_best.fitness, chosing_best.fitness)
print(decision_best.chromosomes.GetHumanExpression())
print(chosing_best.chromosomes.GetHumanExpression())

start_time = time.time()
fitness, reject, cost = calFitness(0.5, decision_best, chosing_best, network, request_test, vnf_list, node_list)
print("Thoi gian test", time.time() - start_time)
print("Result: ")
print(fitness, reject, cost)

# update_deploy, cost = deploy(network, request_list[0], chosing_indi, vnf_list, node_list, link_list)
# print(update_deploy)
# print(cost)