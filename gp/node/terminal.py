from .baseline import Node
import numpy as np


##############################################################
# Properties are normalized to [0,1] before being used in GP #
# Due date of request 
class DDR(Node):
    def __init__(self):
         super(DDR,self).__init__()
    def __repr__(self):
        return "DDR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DDR"
    def getSymbol(self):
        return "DDR"
    def GetOutput(self, X):
        return (X.r.lifetime - X.T)/X.r.lifetime
    
    def GetSurrogateOutput(self, X):
        return X.DDR
    
# Bandwidth of request
class BR(Node):
    def __init__(self, max_bandwidth_network):
         super(BR,self).__init__()
         self.max_bandwidth_network = max_bandwidth_network
    def __repr__(self):
        return "BR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "BR"
    def getSymbol(self):
        return "BR"  

    def GetOutput(self, X):
        return X.r.bw/self.max_bandwidth_network
    
    def GetSurrogateOutput(self, X):
        return X.BR/ self.max_bandwidth_network


# sum of Ram of request
class RRS(Node):
    def __init__(self, sum_ram_network):
        super(RRS,self).__init__()
        self.sum_ram_network = sum_ram_network
    def __repr__(self):
        return "RRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RRS"
    
    def getSymbol(self):
        return "RRS"
    
    def GetOutput(self, X):
        return X.VNFs_request_resource["ram"]/self.sum_ram_network
    
    def GetSurrogateOutput(self, X):
        return X.RRS/ self.sum_ram_network
    
# sum of CPU of request
class CRS(Node):
    def __init__(self, sum_cpu_network):
        super(CRS,self).__init__()
        self.sum_cpu_network = sum_cpu_network
    def __repr__(self):
        return "CRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CRS"

    def getSymbol(self):
        return "CRS"
    def GetOutput(self, X):
        return X.VNFs_request_resource["cpu"]/self.sum_cpu_network
    
    def GetSurrogateOutput(self, X):
        return X.CRS/ self.sum_cpu_network
    
# sum of memory of request
class MRS(Node):
    def __init__(self, sum_mem_network):
        super(MRS, self).__init__()
        self.sum_mem_network = sum_mem_network
    def __repr__(self):
        return "MRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MRS"
    def getSymbol(self):
        return "MRS"
    def GetOutput(self, X):
        return X.VNFs_request_resource["mem"]/self.sum_mem_network
    def GetSurrogateOutput(self, X):
        return X.MRS/ self.sum_mem_network
    
# RAM of first VNF in request
class FirstVNF_RAM(Node):
    def __init__(self, max_ram_VNF):
        super(FirstVNF_RAM, self).__init__()
        self.max_ram_VNF = max_ram_VNF
    def __repr__(self):
        return "FirstVNF_RAM"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FirstVNF_RAM"
    def getSymbol(self):
        return "FirstVNF_RAM"
    def GetOutput(self, X):
        return X.first_VNF_requirement["ram"]/self.max_ram_VNF
    def GetSurrogateOutput(self, X):
        return X.FirstVNF_RAM/self.max_ram_VNF
    
# CPU of first VNF in request
class FirstVNF_CPU(Node):
    def __init__(self, max_cpu_VNF):
        super(FirstVNF_CPU, self).__init__()
        self.max_cpu_VNF = max_cpu_VNF
    def __repr__(self):
        return "FirstVNF_CPU"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FirstVNF_CPU"
    def getSymbol(self):
        return "FirstVNF_CPU"
    def GetOutput(self, X):
        return X.first_VNF_requirement["cpu"]/self.max_cpu_VNF
    def GetSurrogateOutput(self, X):
        return X.FirstVNF_CPU/self.max_cpu_VNF

# Mem of first VNF in request
class FirstVNF_Mem(Node):
    def __init__(self, max_mem_VNF):
        super(FirstVNF_Mem, self).__init__()
        self.max_mem_VNF = max_mem_VNF
    def __repr__(self):
        return "FirstVNF_Mem"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FirstVNF_Mem"
    def getSymbol(self):
        return "FirstVNF_Mem"
    def GetOutput(self, X):
        return X.first_VNF_requirement["mem"]/self.max_mem_VNF
    def GetSurrogateOutput(self, X):
        return X.FirstVNF_Mem/self.max_mem_VNF
    
# Max RAM of server that can be used for first VNF in request
class FirstVNF_RAM_Server(Node):
    def __init__(self, max_ram_server):
        super(FirstVNF_RAM_Server, self).__init__()
        self.max_ram_server = max_ram_server
    def __repr__(self):
        return "FirstVNF_RAM_Server"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FirstVNF_RAM_Server"
    def getSymbol(self):
        return "FirstVNF_RAM_Server"
    def GetOutput(self, X):
        return X.VNFs_resource[X.r.VNFs[0]]["ram"]/self.max_ram_server
    def GetSurrogateOutput(self, X):
        return X.FirstVNF_RAM_Server/ self.max_ram_server
    
# Max CPU of server that can be used for first VNF in request
class FirstVNF_CPU_Server(Node):
    def __init__(self, max_cpu_server):
        super(FirstVNF_CPU_Server, self).__init__()
        self.max_cpu_server = max_cpu_server
    def __repr__(self):
        return "FirstVNF_CPU_Server"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FirstVNF_CPU_Server"
    def getSymbol(self):
        return "FirstVNF_CPU_Server"
    def GetOutput(self, X):
        return X.VNFs_resource[X.r.VNFs[0]]["cpu"]/self.max_cpu_server
    def GetSurrogateOutput(self, X):
        return X.FirstVNF_CPU_Server/ self.max_cpu_server

# Max Mem of server that can be used for first VNF in request
class FirstVNF_Mem_Server(Node):
    def __init__(self, max_mem_server):
        super(FirstVNF_Mem_Server, self).__init__()
        self.max_mem_server = max_mem_server
    def __repr__(self):
        return "FirstVNF_Mem_Server"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FirstVNF_Mem_Server"
    def getSymbol(self):
        return "FirstVNF_Mem_Server"
    def GetOutput(self, X):
        return X.VNFs_resource[X.r.VNFs[0]]["mem"]/self.max_mem_server
    def GetSurrogateOutput(self, X):
        return X.FirstVNF_Mem_Server/self.max_mem_server
    
    
# average of max_RAM that can be used in server of request
class ARS(Node):
    def __init__(self, max_ram_server):
        super(ARS, self).__init__()
        self.max_ram_server = max_ram_server
        
    def __repr__(self):
        return "ARS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "ARS"

    def getSymbol(self):
        return "ARS"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNFs_resource[vnf]["ram"]
        return temp/len(X.r.VNFs)/self.max_ram_server
    
    def GetSurrogateOutput(self, X):
        return X.ARS/ self.max_ram_server
    
# average of max_CPU that can be used in server of request
class ACS(Node):
    def __init__(self, max_cpu_server):
        super(ACS, self).__init__()
        self.max_cpu_server = max_cpu_server
        
    def __repr__(self):
        return "ACS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "ACS"

    def getSymbol(self):
        return "ACS"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNFs_resource[vnf]["cpu"]
        return temp/len(X.r.VNFs)/self.max_cpu_server
    
    def GetSurrogateOutput(self, X):
        return X.ACS/ self.max_cpu_server
    
# average of max_Mem that can be used in server of request

class AMS(Node):
    def __init__(self, max_mem_server):
        super(AMS, self).__init__()
        self.max_mem_server = max_mem_server
        
    def __repr__(self):
        return "AMS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "AMS"
    def getSymbol(self):
        return "AMS"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNFs_resource[vnf]["mem"]
        return temp/len(X.r.VNFs)/self.max_mem_server 

    def GetSurrogateOutput(self, X):
        return X.AMS / self.max_mem_server
    

# max_delay in server of request
class MDR(Node):
    def __init__(self):
        super(MDR, self).__init__()
    def __repr__(self):
        return "MDR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MDR"
    def getSymbol(self):
        return "MDR"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNF_max_delay[vnf]
        return temp  / X.r.lifetime 
    
    def GetSurrogateOutput(self, X):
        return X.MDR
    
# push_back number of request
class PN(Node):
    def __init__(self):
        super(PN, self).__init__()
    def __repr__(self):
        return "PN"
    def _GetHumanExpressionSpecificNode(self, args):
        return "PN"
    def getSymbol(self):
        return "PN"
    def GetOutput(self, X):
        return X.r.push_number/X.r.lifetime
    def GetSurrogateOutput(self, X):
        return X.PN

# class ARRS(Node):
#     def __init__(self):
#         super(ARRS, self).__init__()
#     def __repr__(self):
#         return "ARRS"
#     def _GetHumanExpressionSpecificNode(self, args):
#         return "ARRS"
#     def getSymbol(self):
#         return "ARRS"
#     def GetOutput(self, X):
#         return X.VNFs_request_resource["ram"]/len(X.r.VNFs)
#     def GetSurrogateOutput(self, X):
#         return X.ARRS

# class ACRS(Node):
#     def __init__(self):
#         super(ACRS, self).__init__()
#     def __repr__(self):
#         return "ACRS"
#     def _GetHumanExpressionSpecificNode(self, args):
#         return "ACRS"
#     def getSymbol(self):
#         return "ACRS"
#     def GetOutput(self, X):
#         return X.VNFs_request_resource["cpu"]/len(X.r.VNFs)
#     def GetSurrogateOutput(self, X):
#         return X.ACRS

# class AMRS(Node):
#     def __init__(self):
#         super(AMRS, self).__init__()
#     def __repr__(self):
#         return "AMRS"
#     def _GetHumanExpressionSpecificNode(self, args):
#         return "AMRS"
#     def getSymbol(self):
#         return "AMRS"
#     def GetOutput(self, X):
#         return X.VNFs_request_resource["mem"]/len(X.r.VNFs)
#     def GetSurrogateOutput(self, X):
#         return X.AMRS

class Accepted_Node(Node):
    def __init__(self, accepted_value):
        super(Accepted_Node, self).__init__()
        self.accepted_value = accepted_value
    def __repr__(self):
        return "Accepted_Node"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Accepted_Node"
    def getSymbol(self):
        return "Accepted_Node"
    def GetOutput(self, X):
        return self.accepted_value
    def GetSurrogateOutput(self, X):
        return X.Accepted_Node
    
 ##############################################################   
class Rand(Node):
    def __init__(self):
        super(Rand, self).__init__()
    def __repr__(self):
        return "Rand"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Rand"
    def getSymbol(self):
        return "Rand"
    def GetOutput(self, X):
        return np.random.rand()
      
class Const(Node):
    def __init__(self):
        super(Const, self).__init__()
        self.value = np.random.uniform(0, 1)
    def __repr__(self):
        return "Const"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Const"
    def getSymbol(self):
        return "Const"
    def GetOutput(self, X):
        return self.value
    def GetSurrogateOutput(self, X):
        return self.value 

    def mutate_value(self):
        self.value = self.value + np.random.normal(0, 0.1)           

####################################################################
# Chosing server policy

# The remain of CPU in server
class RCSe(Node):
    def __init__(self):
        super(RCSe, self).__init__()
    def __repr__(self):
        return "RCSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RCSe"
    def getSymbol(self):    
        return "RCSe"
    def GetOutput(self, X):
        return X.server_state["cpu"]/X.cpu_capacity
    def GetSurrogateOutput(self, X):
        return X.RCSe
    
# The remain of RAM in server
class RRSe(Node):
    def __init__(self):
        super(RRSe, self).__init__()
    def __repr__(self):
        return "RRSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RRSe"
    def getSymbol(self):
        return "RRSe"
    def GetOutput(self, X):
        return X.server_state["ram"]/X.ram_capacity
    def GetSurrogateOutput(self, X):
        return X.RRSe
    
# The remain of Mem in server
class  RMSe(Node):
    def __init__(self):
        super(RMSe, self).__init__()
    def __repr__(self):
        return "RMSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RMSe"
    def getSymbol(self):
        return "RMSe"
    def GetOutput(self, X):
        return X.server_state["mem"]/X.mem_capacity
    def GetSurrogateOutput(self, X):
        return X.RMSe
    
# Maximun link utilization of path to server
class MLU(Node):
    def __init__(self):
        super(MLU, self).__init__()
    def __repr__(self):
        return "MLU"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MLU"
    def getSymbol(self):
        return "MLU"
    def GetOutput(self, X):
        return X.MLU
    def GetSurrogateOutput(self, X):
        return X.MLU
    
# The cost of server
class CS(Node):
    def __init__(self):
        super(CS, self).__init__()
    def __repr__(self):
        return "CS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CS"
    def getSymbol(self):
        return "CS"
    def GetOutput(self, X):
        return X.cost
    def GetSurrogateOutput(self, X):
        return X.CS

# The max delay to server
class DS(Node):
    def __init__(self):
        super(DS, self).__init__()
    def __repr__(self):
        return "DS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DS"
    def getSymbol(self):
        return "DS"
    def GetOutput(self, X):
        return X.delay/X.request_lifetime
    def GetSurrogateOutput(self, X):
        return X.DS
# The max utilization of CPU in server
class MUC(Node):
    def __init__(self):
        super(MUC, self).__init__()
    
    def __repr__(self):
        return "MUC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUC"

    def getSymbol(self):
        return "MUC"
    def GetOutput(self, X):
        return 1-X.MRU["cpu"]
    def GetSurrogateOutput(self, X):
        return X.MUC

# The max utilization of RAM in server
class MUR(Node):
    def __init__(self):
        super(MUR, self).__init__()
    
    def __repr__(self):
        return "MUR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUR"
    def getSymbol(self):
        return "MUR"

    def GetOutput(self, X):
        return 1-X.MRU["ram"]
    def GetSurrogateOutput(self, X):
        return X.MUR
        
# The max utilization of Mem in server
class MUM(Node):
    def __init__(self):
        super(MUM, self).__init__()
    
    def __repr__(self):
        return "MUM"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUM"
    def getSymbol(self):
        return "MUM"
    def GetOutput(self, X):
        return 1-X.MRU["mem"]
    def GetSurrogateOutput(self, X):
        return X.MUM
    
class Zero_Node(Node):
    def __init__(self):
        super(Zero_Node, self).__init__()
    def __repr__(self):
        return "Zero_Node"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Zero_Node"
    def getSymbol(self):
        return "Zero_Node"
    def GetOutput(self, X):
        return 0
    def GetSurrogateOutput(self, X):
        return 0