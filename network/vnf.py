import json
class VNF:
    def __init__(self, name, c_f, r_f, h_f, d_f):
        self.name = name # name of VNF
        self.c_f = c_f # used_cpu of VNF
        self.r_f = r_f # used_ram of VNF
        self.h_f = h_f # used_memory of VNF
        self.d_f = d_f # boot time of VNF in server
        # d_f :{
        #     name_server : time_boot
        # }
        
    def MDC_VNF(self):
        return [int(server) for server in self.d_f.keys()]
    


with open(r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\data\input\cogent_urban_hard.json') as file:
    data = json.load(file)
    vnf = VNF(0, data["F"][0]["c_f"], data["F"][0]["r_f"], data["F"][0]["h_f"], data["F"][0]["d_f"])
    
    print(vnf.MDC_VNF())