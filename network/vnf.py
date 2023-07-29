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
        self.max_cost = 0
        
    def MDC_VNF(self):
        return [int(server) for server in self.d_f.keys()]

    def get_requested_resource(self):
        return {
            "cpu": self.c_f,
            "memory": self.h_f,
            "ram": self.r_f
        }
        
    def get_requested_CPU(self):
        return self.c_f
    
    def get_requested_RAM(self):
        return self.r_f
    
    def get_requested_memory(self):
        return self.h_f    