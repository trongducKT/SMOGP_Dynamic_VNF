import json
from copy import deepcopy
import numpy as np
import heapq
from copy import deepcopy

# the remain of resource in server at time slot T
def remain_server_state(server_list, T):
    #print("remain server state")
    remain_resource = {
        
    }
    for server in server_list:
        remain_resource[server.name] = server.check_resource_T(T)
    return remain_resource

# max resource that can provide for VNFs at time slot T:
def VNFs_resource_max(server_list , vnf_list, T):
    #print("VNFs resource max")
    VNFs_resource = {}
    remain_resource = remain_server_state(server_list, T)
    for vnf in vnf_list:
        cpu_max = -np.inf
        mem_max = -np.inf
        ram_max = -np.inf
        for server in vnf.d_f.keys():
            cpu_max = max(cpu_max, remain_resource[server]["remain_cpu"])
            mem_max = max(mem_max, remain_resource[server]["remain_mem"]) 
            ram_max = max(ram_max, remain_resource[server]["remain_ram"])
            VNFs_resource[vnf.name] = {
                "cpu": cpu_max,
                "mem": mem_max,
                "ram": ram_max
                
            }
    return VNFs_resource

def server_find(list_server, server_name):
    #print("server find")
    for server in list_server:
        if server.name == server_name:
            return server
    return None

            
def max_delay_vnf(list_server, list_vnf):
    #print("max delay vnf")
    max_delay ={}
    for vnf in list_vnf:
        max_vnf_delay = -np.inf
        for server in vnf.d_f.keys():
            server_node = server_find(list_server, server)
            max_vnf_delay = max(max_vnf_delay, vnf.d_f[server] + server_node.delay) 
        max_delay[vnf.name] = max_vnf_delay
        
    return max_delay

def dijkstra(network , start, end, bandwidth_requirement, T1,T2, node_list):
    #print("dijkstra")
    graph = network.to_graph()
    
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]
    parents = {vertex: None for vertex in graph}

    while heap:
        current_distance, current_vertex = heapq.heappop(heap)
        if current_distance > distances[current_vertex]:
            continue
        server_node = server_find(node_list, current_vertex)
        for link in server_node.links:
            neighbor = link.next(server_node).name
            delay = link.link_delay
            bandwidth = link.get_bandwidth_to(T1, T2)

            if bandwidth < bandwidth_requirement:
                continue
            
            distance = current_distance + delay

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_vertex
                heapq.heappush(heap, (distance, neighbor))
    path = [end]
    current_vertex = end
    while current_vertex != start:
        if current_vertex is None:
            return None, None
        current_vertex = parents[current_vertex]
        path.append(current_vertex)
    path.reverse()
    del graph
    del heap
    return distances[end], path

def link_search(link_list, u, v):
    #print("link search")
    for link in link_list:
        if link.u.name == u and link.v.name == v:
            return link
        elif link.u.name == v and link.v.name == u:
            return link
    return None
        
def update_link_state(link_list, path, bandwidth_used, T1, T2):
    #print("update link state")
    for i in range(len(path) - 1):
        link = link_search(link_list, path[i], path[i+1])
        if link !=None:
            link.add_used(T1,T2, bandwidth_used)
            
def get_time_slot(arrival_time, finised_time):
    #print("get time slot")
    T1 = int(arrival_time)
    T2 = int(arrival_time + finised_time) 
    if T2 != arrival_time + finised_time:
        T2 += 1
    return T1, T2

def get_request_run(request_list, reject, T):
    #print("get request run")
    request_processing = []
    request_reject = []
    for request in request_list:
        if request.arrival == T :
            if request.lifetime > T:
                request_processing.append(request)
            else:
                reject += 1
                request_reject.append(request)
    
    # for request in request_processing:
    #     request_list.remove(request)
    # for request in request_reject:
    #     request_list.remove(request)
            
    return request_processing, request_reject, reject


def get_max_cost_vnf(server_list, vnf_list):
    #print("get max cost vnf")
    for vnf in vnf_list:
        max_cost = -np.inf
        for server in vnf.d_f.keys():
            server_node = server_find(server_list, server)
            max_cost = max(max_cost, server_node.get_cost(vnf))
        vnf.max_cost = max_cost
            

def get_max_cost_request(vnf_list, request_list):
    #print("get max cost request")
    sum_max_cost = 0
    for request in request_list:
        for vnf in request.VNFs:
            sum_max_cost += vnf_list[vnf].max_cost
    
    return sum_max_cost
            
