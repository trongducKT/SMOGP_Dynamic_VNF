from .baseline import Node
import numpy as np


# Decision policy
# Due date of request 
class DDR(Node):
    def __init__(self):
         super(DDR,self).__init__()
    def __repr__(self):
        return "DDR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DDR"
    def GetOutput(self, X):
        return X.r.lifetime - X.T
    
# Bandwidth of request
class BR(Node):
    def __init__(self):
         super(BR,self).__init__()
    def __repr__(self):
        return "BR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "BR"
    def GetOutput(self, X):
        return X.r.bw

# sum of Ram of request
class RRS(Node):
    def __init__(self):
        super(RRS,self).__init__()
    def __repr__(self):
        return "RRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RRS"
    def GetOutput(self, X):
        return X.VNFs_request_resource["ram"]
    
# sum of CPU of request
class CRS(Node):
    def __init__(self):
        super(CRS,self).__init__()
    def __repr__(self):
        return "CRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CRS"
    def GetOutput(self, X):
        return X.VNFs_request_resource["cpu"]
    
# sum of memory of request
class MRS(Node):
    def __init__(self):
        super(MRS, self).__init__()
    def __repr__(self):
        return "MRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MRS"
    def GetOutput(self, X):
        return X.VNFs_request_resource["mem"]
    
# average of max_RAM that can be used in server of request
class ARS(Node):
    def __init__(self):
        super(ARS, self).__init__()
        
    def __repr__(self):
        return "ARS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "ARS"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNFs_resource[vnf]["ram"]
        return temp/len(X.r.VNFs)
    
# average of max_CPU that can be used in server of request
class CRS(Node):
    def __init__(self):
        super(CRS, self).__init__()
        
    def __repr__(self):
        return "CRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CRS"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNFs_resource[vnf]["cpu"]
        return temp/len(X.r.VNFs)
    
# average of max_Mem that can be used in server of request

class MRS(Node):
    def __init__(self):
        super(MRS, self).__init__()
        
    def __repr__(self):
        return "MRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MRS"
    
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNFs_resource[vnf]["mem"]
        return temp/len(X.r.VNFs)   
    

# max_delay in server of request
class MDR(Node):
    def __init__(self):
        super(MDR, self).__init__()
    def __repr__(self):
        return "MDR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MDR"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += X.VNF_max_delay[vnf]
        return temp    
    
    
class Rand(Node):
    def __init__(self):
        super(Rand, self).__init__()
    def __repr__(self):
        return "Rand"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Rand"
    def GetOutput(self, X):
        return np.random.rand()
    
class Const(Node):
    def __init__(self):
        super(Const, self).__init__()
    def __repr__(self):
        return "Const"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Const"
    def GetOutput(self, X):
        return 1
    
# push_back number of request
class PN(Node):
    def __init__(self):
        super(PN, self).__init__()
    def __repr__(self):
        return "PN"
    def _GetHumanExpressionSpecificNode(self, args):
        return "PN"
    def GetOutput(self, X):
        return X.r.push_number

class FIFO_DD(Node):
    def __init__(self):
        super(FIFO_DD, self).__init__()
    def __repr__(self):
        return "FIFO_DD"
    def _GetHumanExpressionSpecificNode(self, args):
        return "FIFO_DD"
    def GetOutput(self, X):
        temp = X.r.lifetime - X.T
        rand = temp * np.random.uniform(0,1)
        return (temp + rand)
    
class MinDD(Node):
    def __init__(self):
        super(MinDD, self).__init__()
    def __repr__(self):
        return "MinDD"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MinDD"
    def GetOutput(self, X):
        return -(X.r.lifetime-X.T)               

# Chosing server policy

# The remain of CPU in server
class RCSe(Node):
    def __init__(self):
        super(RCSe, self).__init__()
    def __repr__(self):
        return "RCSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RCSe"
    def GetOutput(self, X):
        return X.server_state["cpu"]
    
# The remain of RAM in server
class RRSe(Node):
    def __init__(self):
        super(RRSe, self).__init__()
    def __repr__(self):
        return "RRSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RRSe"
    def GetOutput(self, X):
        return X.server_state["ram"]
    
# The remain of Mem in server
class  RMSe(Node):
    def __init__(self):
        super(RMSe, self).__init__()
    def __repr__(self):
        return "RMSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RMSe"
    def GetOutput(self, X):
        return X.server_state["mem"]
    
# Maximun link utilization of path to server
class MLU(Node):
    def __init__(self):
        super(MLU, self).__init__()
    def __repr__(self):
        return "MLU"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MLU"
    def GetOutput(self, X):
        return X.MLU
    
# The cost of server
class CS(Node):
    def __init(self):
        super(CS, self).__init__()
    def __repr__(self):
        return "CS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CS"
    def GetOutput(self, X):
        return X.cost


# The max delay to server
class DS(Node):
    def __init__(self):
        super(DS, self).__init__()
    def __repr__(self):
        return "DS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DS"
    def GetOutput(self, X):
        return X.delay
# The max utilization of CPU in server
class MUC(Node):
    def __init__(self):
        super(MUC, self).__init__()
    
    def __repr__(self):
        return "MUC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUC"
    def GetOutput(self, X):
        return 1-X.MRU["cpu"]

# The max utilization of RAM in server
class MUR(Node):
    def __init__(self):
        super(MUR, self).__init__()
    
    def __repr__(self):
        return "MUR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUR"
    def GetOutput(self, X):
        return 1-X.MRU["ram"]
        
# The max utilization of Mem in server
class MUM(Node):
    def __init__(self):
        super(MUM, self).__init__()
    
    def __repr__(self):
        return "MUM"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUM"
    def GetOutput(self, X):
        return 1-X.MRU["mem"]
    
    
class MinCost(Node):
    def __init__(self):
        super(MinCost, self).__init__()
    def __repr__(self):
        return "MinCost"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MinCost"
    def GetOutput(self, X):
        return -X.cost
    
class Relax(Node):
    def __init__(self):
        super(Relax, self).__init__()
    def __repr__(self):
        return "Relax"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Relax"
    def GetOutput(self, X):
        temp = 1-X.MRU["mem"] + 1-X.MRU["ram"] + 1-X.MRU["cpu"]
        temp = temp/3
        return temp

class  CS_Relax(Node):
    def __init__(self):
        super(CS_Relax, self).__init__()
    def __repr__(self):
        return "CS_Relax"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CS_Relax"
    def GetOutput(self, X):
        temp = 1-X.MRU["mem"] + 1-X.MRU["ram"] + 1-X.MRU["cpu"]
        temp = temp/3
        return -X.cost/1000 + temp 

class Scale(Node):
    def __init__(self):
        super(Scale, self).__init__()
    def __repr__(self):
        return "Scale"
    def _GetHumanExpressionSpecificNode(self, args):
        return "Scale"
    def GetOutput(self, X):
        return 1 
    
