from .baseline import Node
import numpy as np

# class NHNode(Node):
#     def __init__(self):
#         super(NHNode,self).__init__()

#     def __repr__(self):
#         return 'NH'

#     def _GetHumanExpressionSpecificNode( self, args ):
#         return  'NH'
    
#     def GetOutput( self, X):
#         tmp = 0
#         for path in X.path_k:
#             tmp = max(tmp,len(path))
#         return len(X.path)/tmp
# class BRNode(Node):
#     def __init__(self):
#         super(BRNode,self).__init__()

#     def __repr__(self):
#         return 'BR'

#     def _GetHumanExpressionSpecificNode( self, args ):
#         return  'BR'
    
#     def GetOutput( self, X):
#         tmp =  float('inf')
#         for link in X.route_links:
#             tmp = min(tmp,(link.cap-link.used)/link.cap)
#         return tmp

# class DNode(Node):
#     def __init__(self):
#         super(DNode,self).__init__()

#     def __repr__(self):
#         return 'Degree'

#     def _GetHumanExpressionSpecificNode( self, args ):
#         return  'Degree'
#     def GetOutput(self,X):
#         return None
# class TBRNode(Node):
#     def __init__(self):
#         super(TBRNode,self).__init__()
#     def __repr__(self):
#         return 'TBR'

#     def _GetHumanExpressionSpecificNode( self, args ):
#         return  'TBR'
#     def GetOutput(self,X):
#         tmp = 0 
#         for link in X.route_links:
#             tmp += (link.cap-link.used)/link.cap
#         return tmp
# class CPUNode(Node):
#     def __init__(self):
#         super(CPUNode,self).__init__()
#     def __repr__(self):
#         return 'CPU'

#     def _GetHumanExpressionSpecificNode( self, args ):
#         return  'CPU'
#     def GetOutput(self,X):
#         return X.next.used/ X.next.cap
# class ERCNode(Node):
#     def __init__(self):
#         super(ERCNode,self).__init__()
#         self.value = np.random.rand()
#     def __repr__(self):
#         return str(self.value) 

#     def _GetHumanExpressionSpecificNode( self, args ):
#         return  str(self.value)
#     def GetOutput(self,X):
#         return self.value
   
###################################################333333333333 
# decision policy
# class X:
#     self.r : request
#     self.T : time slot that is happening
#     slelf.VNFs_resourcei in server:
#         self.VNFs_resource = {
#             vnf_name:{
#                 "cpu": 0,
#                 "ram": 0,
#                 "mem": 0
#}   
# }
#     self.max_delay = {
#          vnf_name: 0
#    
#}

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
        temp = 0
        for vnf in X.r.VNFs:
            temp += vnf.r_f
        return temp
    
# sum of CPU of request
class CRS(Node):
    def __init__(self):
        super(CRS,self).__init__()
    def __repr__(self):
        return "CRS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CRS"
    def GetOutput(self, X):
        temp = 0
        for vnf in X.r.VNFs:
            temp += vnf.c_f
        return temp
    
# sum of memory of request
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
            temp += vnf.h_f
        return temp
    
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
                 

# Chosing server policy

# The remain of CPU in server
class RCSe(Node):
    def __init__(self):
        super(RCSe, self).__init__()
    def __repr__(self):
        return "RCSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RCSe"
    def GetOutput(self, X, start_T, end_T):
        return min(X.used[start_T: end_T]["cpu_used"])
    
# The remain of RAM in server
class RRSe(Node):
    def __init__(self):
        super(RRSe, self).__init__()
    def __repr__(self):
        return "RRSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RRSe"
    def GetOutput(self, X, start_T, end_T):
        return min(X.used[start_T: end_T]["ram_used"])
    
# The remain of Mem in server
class  RMSe(Node):
    def __init__(self):
        super(RMSe, self).__init__()
    def __repr__(self):
        return "RMSe"
    def _GetHumanExpressionSpecificNode(self, args):
        return "RMSe"
    def GetOutput(self, X, start_T, end_T):
        return min(X.used[start_T: end_T]["mem_used"])
    
# Maximun link utilization of path to server
class MLU(Node):
    def __init__(self):
        super(MLU, self).__init__()
    def __repr__(self):
        return "MLU"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MLU"
    def GetOutput(self, X, path, start_T, end_T):
        temp = -np.inf
        for link in path:
            link_utilization = max(link.used[start_T: end_T]/link.cap)
            temp = max(temp, link_utilization)
        return temp
    
# The cost of server
class CS(Node):
    def __init(self):
        super(CS, self).__init__()
    def __repr__(self):
        return "CS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "CS"
    def GetOutput(self, X, VNF):
        return VNF.c_f*X.cost["cost_c"] + VNF.r_f*X.cost["cost_r"] + VNF.h_f*X.cost["cost_h"]


# The max delay to server
class DS(Node):
    def __init__(self):
        super(DS, self).__init__()
    def __repr__(self):
        return "DS"
    def _GetHumanExpressionSpecificNode(self, args):
        return "DS"
    def GetOutput(self, X, VNF, path):
        delay = 0
        for link in path:
            delay += link.link_delay
        
        delay += VNF.d_f[X.name]
        delay += X.delay
        return delay
    
# The max utilization of CPU in server
class MUC(Node):
    def __init__(self):
        super(MUC, self).__init__()
    
    def __repr__(self):
        return "MUC"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUC"
    def GetOutput(self, start_T, end_T):
        return max(self.used[start_T: end_T]["cpu_used"]/self.cap["cpu_cap"])

# The max utilization of RAM in server
class MUR(Node):
    def __init__(self):
        super(MUR, self).__init__()
    
    def __repr__(self):
        return "MUR"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUR"
    def GetOutput(self, start_T, end_T):
        return max(self.used[start_T: end_T]["ram_used"]/self.cap["ram_cap"])
        
# The max utilization of Mem in server
class MUM(Node):
    def __init__(self):
        super(MUM, self).__init__()
    
    def __repr__(self):
        return "MUM"
    def _GetHumanExpressionSpecificNode(self, args):
        return "MUM"
    def GetOutput(self, start_T, end_T):
        return max(self.used[start_T: end_T]["mem_used"]/self.cap["mem_cap"])       
        