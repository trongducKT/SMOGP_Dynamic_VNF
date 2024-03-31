from gp.population.individual import Individual
import random

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
    def __init__(self, DDR, BR, RRS, CRS, MRS, ARS, ACS, AMS, MDR, PN):
        self.DDR = DDR
        self.BR = BR
        self.RRS = RRS
        self.CRS = CRS
        self.MRS = MRS
        self.ARS = ARS
        self.ACS = ACS
        self.AMS = AMS
        self.MDR = MDR
        self.PN = PN
    
    def gen_random(self):
        self.DDR = random.randint(0, 10)
        self.BR = random.uniform(30, 100)
        self.RRS = random.uniform(0, 10)
        self.CRS = random.uniform(0, 10)
        self.MRS = random.uniform(0, 10)
        self.ARS = random.uniform(0, 100)
        self.ACS = random.uniform(0, 100)
        self.AMS = random.uniform(0, 100)
        self.MDR = random.uniform(0, 100)
        self.PN = random.uniform(0, 10)
    
    def __repr__(self) -> str:
        return f"DDR: {self.DDR}, BR: {self.BR}, RRS: {self.RRS}, CRS: {self.CRS}, MRS: {self.MRS}, ARS: {self.ARS}, ACS: {self.ACS}, AMS: {self.AMS}, MDR: {self.MDR}, PN: {self.PN}"

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
        self.RCSe = random.uniform(0, 100)
        self.RRSe = random.uniform(0, 100)
        self.RMSe = random.uniform(0, 100)
        self.MLU = random.uniform(0, 1)
        self.CS = random.uniform(0, 1)
        self.DS = random.uniform(0, 10)
        self.MUC = random.uniform(0, 1)/3
        self.MUR = random.uniform(0, 1)/3
        self.MUM = random.uniform(0, 1)/3
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

    
    def gen_situations_random(self, L_requests_num, U_requests_num, L_servers_num, U_servers_num):
        self.ordered_situations = []
        self.server_situations = []

        for i in range(self.number_situations):
            requests_num = random.randint(L_requests_num, U_requests_num)
            servers_num = random.randint(L_servers_num, U_servers_num)
            request_list = []
            server_list = []
            for ii in range(requests_num):
                request = Request_Surrogate(None, None, None, None, None, None, None, None, None, None)
                request.gen_random()
                request_list.append(request)
            for ii in range(servers_num):
                server = Server_Surrogate(None, None, None, None, None, None, None, None, None)
                server.gen_random()
                server_list.append(server)
            self.ordered_situations.append(request_list)
            self.server_situations.append(server_list)

    def cal_pc(self, individual: Individual):
        ordering_pc = []
        choosing_pc = []
        for i in range(self.number_situations):
            determining_priority = [individual.ordering_tree.GetSurrogateOutput(request) for request in self.ordered_situations[i]]
            choosing_priority = [individual.choosing_tree.GetSurrogateOutput(server) for server in self.server_situations[i]]
            # print(determining_priority, choosing_priority)
            ordering_index = determining_priority.index(max(determining_priority))
            choosing_index = choosing_priority.index(max(choosing_priority))

            ordering_priority_ref = [self.ref_rule.ordering_rule.GetSurrogateOutput(request) for request in self.ordered_situations[i]]
            choosing_priority_ref = [self.ref_rule.choosing_rule.GetSurrogateOutput(server) for server in self.server_situations[i]]


            ordering_rank = ranking_index(ordering_priority_ref)
            choosing_rank = ranking_index(choosing_priority_ref)
            # print(ordering_rank, choosing_rank)
            ordering_pc.append(ordering_rank[ordering_index])
            choosing_pc.append(choosing_rank[choosing_index])
        return ordering_pc + choosing_pc