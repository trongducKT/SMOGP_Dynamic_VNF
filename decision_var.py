class Decision:
    def __init__(self, r, T , vnf_resource, max_delay):
        self.r = r
        self.T = T # time slot that is happening
        self.VNFs_resource = vnf_resource # VNFs_resourcei in server
        self.VNF_max_delay = max_delay # delay of vnf in server
    

