import json
from network.network import Node, Link
from network.requests import Request
from network.vnf import VNF
from utils.utils import get_info_link, get_info_server, get_info_vnf

class Read_data:
    def __init__(self, PATH):
        with open(PATH) as f:
            self.data = json.load(f)
        
    def get_V(self):
        node_list = []
        for key, value in self.data["V"].items():
            name = int(key)
            if value["server"] == True:
                cap ={
                    "memory_cap": value["h_v"],
                    "cpu_cap": value["c_v"],
                    "ram_cap": value["r_v"]
                }
                delay = value["d_v"]
                cost ={
                    "cost_c" : value["cost_c"],
                    "cost_h":  value["cost_h"],
                    "cost_r":   value["cost_r"]
                }
                node = Node(name, 2, delay, cap, cost)  
                node_list.append(node)
            else:
                node = Node(name, 1)
                node_list.append(node)
        return node_list
    
    def get_E(self):
        link_list = []
        for link in self.data["E"]:
            u = int(link["u"])
            v = int(link["v"])
            cap = link["b_l"]
            delay = link["d_l"]
            link1 = Link(u, v, cap, delay)
            link_list.append(link1)
        return link_list
    
    def get_F(self):
        vnf_list = []
        for i in range(len(self.data["F"])):
            c_f = self.data["F"][i]["c_f"]
            r_f = self.data["F"][i]["r_f"]
            h_f = self.data["F"][i]["h_f"]
            d_f = {}
            for key, value in self.data["F"][i]["d_f"].items():
                d_f[int(key)] = value
            vnf = VNF(i, c_f, r_f, h_f, d_f)
            vnf_list.append(vnf)
        return vnf_list
    
    def get_R(self):
        r_list = []
        name = 0
        for r in self.data["R"]:
            T = r["T"] + 1
            st_r = r["st_r"]
            d_r = r["d_r"]
            F_r = r["F_r"]
            b_r = r["b_r"]
            d_max = int(r["d_max"])+T
            request = Request(r["d_max"], name, T, d_max, st_r, d_r, F_r, b_r)
            r_list.append(request)
            name = name + 1
        return r_list
    
    def get_info_network(self):
        server_list = self.get_V()
        link_list = self.get_E()
        vnf_list = self.get_F()
        print(len(server_list), len(link_list), len(vnf_list))
        ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server = get_info_server(server_list)
        ram_max_vnf, cpu_max_vnf, mem_max_vnf = get_info_vnf(vnf_list)
        max_bandwidth = get_info_link(link_list)
        return ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server, ram_max_vnf, cpu_max_vnf, mem_max_vnf, max_bandwidth

