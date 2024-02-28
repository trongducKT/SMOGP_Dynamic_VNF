def ranking_index(value_list):
    sorted_list = sorted(value_list, reverse=True)
    index_list = []
    seen = set()
    for x in value_list:
        for i, y in enumerate(sorted_list):
            if x == y:
                if i not in seen:
                    index_list.append(i+1)
                    seen.add(i)
                    break
                else:
                    index_list.append(i+1)
                    break
    return index_list


from .gp.population.individual import Individual
import random

class Request_Surrogate:
    def __init__(self):
        self.DDR = random.uniform(0,20)
        self.BR = random.uniform(20, 100)
        self.RRS = random.uniform(0,100)
        self.CRS = random.uniform(0,100)
        self.MRS = random.uniform(0,100)
        self.ARS = random.uniform(0,100)
        self.ACS = random.uniform(0,100)
        self.AMS = random.uniform(0,100)
        self.MDR = random.uniform(0,100)
        self.PN = random.randint(0,10)
        self.Con = random.random()

class Server_Surrogate:
    def __init__(self):
        self.RCSe = random.uniform(0,100)
        self.RRSe = random.uniform(0,100)
        self.RMSe = random.uniform(0,100)
        self.MLU = random.random()
        self.CS = random.uniform(0,500)
        self.DS = random.uniform(0,100)
        self.MUC = random.random()
        self.MUR = random.random()
        self.MUM = random.random()
        self.Con = random.random()

class Ref_Rule:
    def __init__(self, determining_rule, choosing_rule):
        self.determining_rule = determining_rule
        self.choosing_rule = choosing_rule


class Surrogate:
    def __init__(self, number_situations, ref_rule: Ref_Rule):
        self.number_situations = number_situations
        self.ref_individual = ref_rule
        self.ordered_situations = None
        self.server_situations = None
        self.determining_ref = None
        self.choosing_ref = None

    
    def gen_situations(self, L_requests_num, U_requests_num, L_servers_num, U_servers_num):
        self.ordered_situations = []
        self.server_situations = []

        for i in range(self.number_situations):
            requests_num = random.randint(L_requests_num, U_requests_num)
            servers_num = random.randint(L_servers_num, U_servers_num)
            request_list = [Request_Surrogate() for i in range(requests_num)]
            server_list = [Server_Surrogate() for i in range(servers_num)]
            self.ordered_situations.append(request_list)
            self.server_situations.append(server_list)
    
    def cal_ref_rule(self):
        self.determining_ref = []
        self.choosing_ref = []
        for i in range(self.number_situations):
            determining_priority = [self.ref_rule.determining_rule.GetSurrogateOutput(request) for request in self.ordered_situations[i]]
            choosing_priority = [self.ref_rule.choosing_rule.GetSurrogateOutput(server) for server in self.server_situations[i]]
            determining_index = determining_priority.index(max(determining_priority))
            choosing_index = choosing_priority.index(max(choosing_priority))
            self.determining_ref.append(determining_index)
            self.choosing_ref.append(choosing_index)

    def cal_pc(self, individual: Individual):
        determining_pc = []
        choosing_pc = []
        for i in range(self.number_situations):
            determining_priority = [individual.determining_tree.GetSurrogateOutput(request) for request in self.ordered_situations[i]]
            choosing_priority = [individual.choosing_tree.GetSurrogateOutput(server) for server in self.server_situations[i]]
            determining_rank = ranking_index(determining_priority)
            choosing_rank = ranking_index(choosing_priority)
            determining_pc.append(determining_rank[self.determining_ref[i]])
            choosing_pc.append(choosing_rank[self.choosing_ref[i]])
        pc = determining_pc.extends(choosing_pc)
        return pc