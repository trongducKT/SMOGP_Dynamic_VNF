import numpy as np
from utils.utils import link_search
class Decision:
    def __init__(self, r, T , vnf_resource, max_delay, vnf_list):
        #rint("Khoi tao bien decision")
        self.r = r
        self.T = T # time slot that is happening
        self.VNFs_resource = vnf_resource # max VNFs_resource in server
        self.VNF_max_delay = max_delay # delay of vnf in server
        cpu = 0
        ram = 0
        mem = 0
        for vnf_name in self.r.VNFs:
            for vnf in vnf_list:
                if vnf.name == vnf_name:
                    cpu += vnf.c_f
                    cpu += vnf.r_f
                    mem += vnf.h_f
        self.VNFs_request_resource = {
            "cpu": cpu,
            "ram": ram,
            "mem": mem
        }
        self.first_VNF_requirement = {}
        for vnf in vnf_list:
            if vnf.name == self.r.VNFs[0]:
                self.first_VNF_requirement = {
                    "cpu": vnf.c_f,
                    "ram": vnf.r_f,
                    "mem": vnf.h_f
                }

class Choosing:
    #T1, T2 in server
    #T3, T4 in link
     def __init__(self, server, T1, T2, path, path_delay, T3, T4, VNF, link_list, request_lifetime ):
        #print("Khoi tao bien chosing")
        self.server_state = server.get_state_server(T1,T2)
        self.cpu_capacity = server.cap["cpu_cap"]
        self.mem_capacity = server.cap["memory_cap"]
        self.ram_capacity = server.cap["ram_cap"]
        temp = np.inf
        for i in range (len(path)-1):
            link = link_search(link_list, path[i], path[i+1])
            link_utilization = link.get_MLU(T3, T4)
            temp = min(temp, link_utilization)
        if len(path) == 1:
            self.MLU = 1
        else:
            self.MLU = 1- temp/(len(path)-1)
        if self.MLU == 0:
            self.MLU = 0
        self.cost = server.get_cost(VNF)/VNF.max_cost
        self.delay = path_delay + VNF.d_f[server.name] + server.delay
        self.MRU = server.get_MRU(T1,T2)
        self.request_lifetime = request_lifetime