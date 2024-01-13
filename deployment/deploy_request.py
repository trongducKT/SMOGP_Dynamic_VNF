from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from data_info.read_data import *
from priority_gp.decision_var import Decision, Choosing
from network.network import Network
from utils.utils import *
# deploy a request
def deploy(network: Network, request: Request, indi : Individual, vnf_list):
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
                if n == int(lifetime - T):
                    break
        
            if n == int(lifetime - T):
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
                X = Choosing(server_node, T1, T2, path, path_delay, T3, T4, vnf_list[VNF], network_copy.links)
                value_of_gp = indi.choosing_tree.GetOutput(X)

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
        if n == int(lifetime - T):
            break
        path_delay, path = dijkstra(network_copy, start_node, end_node, bw, int(T), int(T) + n, network_copy.get_node)
        if n == int(lifetime - T):
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

def decision_gp(indi: Individual, request: Request, T, network, vnf_list):
    server_list = network.MDC_nodes
    vnf_resource = VNFs_resource_max(server_list, vnf_list, T)
    max_delay = max_delay_vnf(server_list, vnf_list)
    X = Decision(request, T, vnf_resource, max_delay, vnf_list)
    result  = indi.determining_tree.GetOutput(X)
    return result