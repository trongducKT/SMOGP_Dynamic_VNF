from gp.population.individual import Individual
import random
import time 

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

class Request_Surrogate:
    def __init__(self, DDR,BR, RRS, CRS, MRS, FirstVNF_RAM, FirstVNF_CPU,
                 FirstVNF_Mem, FirstVNF_RAM_Server, FirstVNF_CPU_Server, FirstVNF_Mem_Server,
                 ARS, ACS, AMS, MDR, PN):
        self.DDR = DDR
        self.BR = BR
        self.RRS = RRS
        self.CRS = CRS
        self.MRS = MRS
        self.FirstVNF_RAM = FirstVNF_RAM
        self.FirstVNF_CPU = FirstVNF_CPU
        self.FirstVNF_Mem = FirstVNF_Mem
        self.FirstVNF_RAM_Server = FirstVNF_RAM_Server
        self.FirstVNF_CPU_Server = FirstVNF_CPU_Server
        self.FirstVNF_Mem_Server = FirstVNF_Mem_Server
        self.ARS = ARS
        self.ACS = ACS
        self.AMS = AMS
        self.MDR = MDR
        self.PN = PN
    
    def gen_random(self):
        self.DDR = random.uniform(0,1)
        self.BR = random.uniform(0,1)
        self.RRS = random.uniform(0,1)
        self.CRS = random.uniform(0,1)
        self.MRS = random.uniform(0,1)
        self.FirstVNF_RAM = random.uniform(0,1)
        self.FirstVNF_CPU = random.uniform(0,1)
        self.FirstVNF_Mem = random.uniform(0,1)
        self.FirstVNF_RAM_Server = random.uniform(0,1)
        self.FirstVNF_CPU_Server = random.uniform(0,1)
        self.FirstVNF_Mem_Server = random.uniform(0,1)
        self.ARS = random.uniform(0,1)
        self.ACS = random.uniform(0,1)
        self.AMS = random.uniform(0,1)
        self.MDR = random.uniform(0,1)
        self.PN = random.uniform(0,1)
class Determining_Surrogate:
    def __init__(self, DDR,BR, RRS, CRS, MRS, FirstVNF_RAM, FirstVNF_CPU,
                 FirstVNF_Mem, FirstVNF_RAM_Server, FirstVNF_CPU_Server, FirstVNF_Mem_Server,
                 ARS, ACS, AMS, MDR, PN):
        self.DDR = DDR
        self.BR = BR
        self.RRS = RRS
        self.CRS = CRS
        self.MRS = MRS
        self.FirstVNF_RAM = FirstVNF_RAM
        self.FirstVNF_CPU = FirstVNF_CPU
        self.FirstVNF_Mem = FirstVNF_Mem
        self.FirstVNF_RAM_Server = FirstVNF_RAM_Server
        self.FirstVNF_CPU_Server = FirstVNF_CPU_Server
        self.FirstVNF_Mem_Server = FirstVNF_Mem_Server
        self.ARS = ARS
        self.ACS = ACS
        self.AMS = AMS
        self.MDR = MDR
        self.PN = PN
    
    def gen_random(self):
        self.DDR = random.uniform(0,1)
        self.BR = random.uniform(0,1)
        self.RRS = random.uniform(0,1)
        self.CRS = random.uniform(0,1)
        self.MRS = random.uniform(0,1)
        self.FirstVNF_RAM = random.uniform(0,1)
        self.FirstVNF_CPU = random.uniform(0,1)
        self.FirstVNF_Mem = random.uniform(0,1)
        self.FirstVNF_RAM_Server = random.uniform(0,1)
        self.FirstVNF_CPU_Server = random.uniform(0,1)
        self.FirstVNF_Mem_Server = random.uniform(0,1)
        self.ARS = random.uniform(0,1)
        self.ACS = random.uniform(0,1)
        self.AMS = random.uniform(0,1)
        self.MDR = random.uniform(0,1)
        self.PN = random.uniform(0,1)

class Server_Surrogate:
    def __init__(self, RCSe, RRSe, RMSe, MLU, CS, DS, MUC, MUR, MUM):
        self.RCSe = RCSe
        self.RRSe = RRSe
        self.RMSe = RMSe
        self.MLU = MLU
        self.CS = CS
        self.DS = DS
        self.MUC = MUC
        self.MUR = MUR
        self.MUM = MUM
    
    def gen_random(self):
        self.RCSe = random.uniform(0,1)
        self.RRSe = random.uniform(0,1)
        self.RMSe = random.uniform(0,1)
        self.MLU = random.uniform(0,1)
        self.CS = random.uniform(0,1)
        self.DS = random.uniform(0,1)
        self.MUC = random.uniform(0,1)
        self.MUR = random.uniform(0,1)
        self.MUM = random.uniform(0,1)
        
class Ref_Rule:
    def __init__(self, determining_rule, ordering_rule, choosing_rule):
        self.determinig_rule = determining_rule
        self.ordering_rule = ordering_rule
        self.choosing_rule = choosing_rule


class Surrogate:
    def __init__(self, number_situations, ref_rule: Ref_Rule):
        self.number_situations = number_situations
        self.ref_rule = ref_rule
        self.ordered_situations = None
        self.server_situations = None
        self.determining_situations = None
        self.ordering_ordered_ref = None
        self.choosing_ordered_ref = None

    
    def gen_situations_random(self, L_requests_num, U_requests_num, L_servers_num, U_servers_num):
        self.ordered_situations = []
        self.server_situations = []
        self.determining_situations = []

        for i in range(self.number_situations):
            requests_num = random.randint(L_requests_num, U_requests_num)
            servers_num = random.randint(L_servers_num, U_servers_num)
            determining_list = []
            request_list = []
            server_list = []
            for ii in range(requests_num):
                determining_request = Determining_Surrogate(None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None)
                determining_request.gen_random()
                determining_list.append(determining_request)
                request = Request_Surrogate(None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None)
                request.gen_random()
                request_list.append(request)
            for ii in range(servers_num):
                server = Server_Surrogate(None, None, None, None, None, None, None, None, None)
                server.gen_random()
                server_list.append(server)
            determining_request = Determining_Surrogate(None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None)
            determining_request.gen_random()
            self.determining_situations.append(determining_request)
            self.ordered_situations.append(request_list)
            self.server_situations.append(server_list)
    
    
    def cal_ordered_ref(self):
        self.ordering_ordered_ref = []
        self.choosing_ordered_ref = []
        for i in range(self.number_situations):
            ordering_priority_ref = [self.ref_rule.ordering_rule.GetSurrogateOutput(request) for request in self.ordered_situations[i]]
            choosing_priority_ref = [self.ref_rule.choosing_rule.GetSurrogateOutput(server) for server in self.server_situations[i]]

            ordering_rank = ranking_index(ordering_priority_ref)
            choosing_rank = ranking_index(choosing_priority_ref)
            self.ordering_ordered_ref.append(ordering_rank)
            self.choosing_ordered_ref.append(choosing_rank)
            

    def cal_pc(self, individual: Individual):
        # for situation in self.determining_situations:
        #     print(individual.determining_tree.GetSurrogateOutput(situation))
#         determining_pc = [ 0 if individual.determining_tree.GetSurrogateOutput(situation) <= 0 else 1 for situation in self.determining_situations]
        ordering_pc = []
        choosing_pc = []
        for i in range(self.number_situations):
            determining_priority = [individual.ordering_tree.GetSurrogateOutput(request) for request in self.ordered_situations[i]]
            choosing_priority = [individual.choosing_tree.GetSurrogateOutput(server) for server in self.server_situations[i]]
            # print(determining_priority, choosing_priority)
            ordering_index = determining_priority.index(max(determining_priority))
            choosing_index = choosing_priority.index(max(choosing_priority))

            # print(ordering_rank, choosing_rank)
            ordering_pc.append(self.ordering_ordered_ref[i][ordering_index])
            choosing_pc.append(self.choosing_ordered_ref[i][choosing_index])
#         return determining_pc + ordering_pc + choosing_pc
        return ordering_pc + choosing_pc