# import functools
# from utils import Solution
# import networkx as nx
# from network import Network
# from requests import SFC, Request
# from heapq import heappush, heappop
# from itertools import count
# import numpy as np 
# import time
# from copy import deepcopy
# EPS = 1e-3

# class Graph:
#     def __init__(self, network: Network):
#         self.network = network
#         self.G = nx.DiGraph()
#         self.build()
#     def build(self):
#         for node in self.network.nodes.values():
#             name = node.name
#             self.G.add_node(name)
            
#         for link in self.network.links:

#             u = link.u.name
#             v = link.v.name
#             if u not in self.G.nodes or v not in self.G.nodes:
#                 continue
#             self.G.add_edge(u, v,
#                             weight=(link.cap / (link.cap - link.used+0.0001) + self.G.nodes[v]['weight']))
#             self.G.add_edge(v, u,
#                             weight=(link.cap / (link.cap - link.used+0.0001) + self.G.nodes[u]['weight']))
#     def k_shortest_paths(self, source, target, k=1, weight='weight'):

#         if source == target:
#             return ([[source]]) 
        
#         length, path = nx.single_source_dijkstra(self.G, source, weight=weight)
#         # if target not in length:
#         #     raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))
#         # print(length)
#         lengths = [length[target]]
#         paths = [path[target]]
#         c = count()        
#         B = []                        
#         G_original = self.G.copy()    
        
#         for i in range(1, k):
#             for j in range(len(paths[-1]) - 1):            
#                 spur_node = paths[-1][j]
#                 root_path = paths[-1][:j + 1]
                
#                 edges_removed = []
#                 for c_path in paths:
#                     if len(c_path) > j and root_path == c_path[:j + 1]:
#                         u = c_path[j]
#                         v = c_path[j + 1]
#                         if self.G.has_edge(u, v):
#                             edge_attr = self.G.adj[u][v]
#                             self.G.remove_edge(u, v)
#                             edges_removed.append((u, v, edge_attr))
                
#                 for n in range(len(root_path) - 1):
#                     node = root_path[n]
#                     # out-edges
#                     for u, v, edge_attr in list(self.G.edges(node, data=True)):
#                         self.G.remove_edge(u, v)
#                         edges_removed.append((u, v, edge_attr))
                    
#                     if self.G.is_directed():
#                         # in-edges
#                         for u, v, edge_attr in list(self.G.in_edges(node, data=True)):
#                             self.G.remove_edge(u, v)
#                             edges_removed.append((u, v, edge_attr))
                
#                 spur_path_length, spur_path = nx.single_source_dijkstra(self.G, spur_node, weight=weight)            
#                 if target in spur_path and spur_path[target]:
#                     total_path = root_path[:-1] + spur_path[target]
#                     total_path_length = self.get_path_length(G_original, root_path, weight) + spur_path_length[target]                
#                     heappush(B, (total_path_length, next(c), total_path))
                    
#                 for e in edges_removed:
#                     u, v, edge_attr = e
#                     self.G.add_edge(u, v,weight =  edge_attr['weight'])
                        
#             if B:
#                 (l, _, p) = heappop(B)        
#                 lengths.append(l)
#                 paths.append(p)
#             else:
#                 break
        
#         return paths

#     def get_path_length(self,G, path, weight='weight'):
#         length = 0
#         if len(path) > 1:
#             for i in range(len(path) - 1):
#                 u = path[i]
#                 v = path[i + 1]
                
#                 length += G.adj[u][v].get(weight, 1)
        
#         return length  
#     def path_pair(self, path):
#         paths = []
#         route_links = []
#         paths.append(self.network.nodes[path[0]])
#         for i in range(1, len(path)):
#             name  = path[i]
#             pname = path[i - 1]
#             u = self.network.nodes[pname]
#             next_link = None
#             for link in u.links:
#                 v = link.u if link.v == u else link.v
#                 if v.name == name:
#                     next_link = link
#                     break
#             paths.append(self.network.nodes[name])
#             route_links.append(next_link)
#         return paths,route_links

#     def find_SFCs(self,start,end, k=10):
#         paths = self.k_shortest_paths(str(start),str(end),k)
#         return [self.path_pair(path) if path is not None else None for path in paths]
# class MultiLayerGraph:
#     def __init__(self, network: Network):
#         self.network = network
#         self.G = nx.DiGraph()
#         self.build()
#     def build(self):
#         for node in self.network.nodes.values():
#             name = node.name
#             self.G.add_node(name,
#                             weight=(node.cap / (node.cap - node.used + 0.0001)
#                                     if node.type == 1 else 0.0))
#         for link in self.network.links:

#             u = link.u.name
#             v = link.v.name
#             if u not in self.G.nodes or v not in self.G.nodes:
#                 continue
#             self.G.add_edge(u, v,
#                             weight=(link.cap / (link.cap - link.used+0.0001) + self.G.nodes[v]['weight']))
#             self.G.add_edge(v, u,
#                             weight=(link.cap / (link.cap - link.used+0.0001) + self.G.nodes[u]['weight']))


#     def k_dijkstra(self,start,end, k=10):
#         if k == 1:
#             try:
#                 return [nx.shortest_path(self.G, start, end, weight='weight')]
#             except:
#                 return []
#         X = nx.shortest_simple_paths(self.G, start, end, weight='weight')
#         paths = []
#         for counter, path in enumerate(X):
#             paths.append(path)
#             if counter == k - 1:
#                 break
#         return paths

#     def path_pair(self, path):
#         paths = []
#         route_links = []
#         paths.append(self.network.nodes[path[0]])
#         for i in range(1, len(path)):
#             name  = path[i]
#             pname = path[i - 1]
#             u = self.network.nodes[pname]
#             next_link = None
#             for link in u.links:
#                 v = link.u if link.v == u else link.v
#                 if v.name == name:
#                     next_link = link
#                     break
#             paths.append(self.network.nodes[name])
#             route_links.append(next_link)
#         return paths,route_links

#     def find_SFCs(self,start,end, k=10):
#         paths = self.k_dijkstra(start,end,k)
#         return [self.path_pair(path) if path is not None else None for path in paths]


# class state: 
#     def __init__(self,network,requests):
#         self.network = network
#         self.requests = requests
#         self.next = None 
#         self.curr = None
#         self.path = None
#         self.route_links = None
#         self.cur_req = None
#         self.H = None
#         self.i = 0 
#         self.path_k = None
#     def update(self,path,route_links):    
#         for node in path:
#             if node.type == 1: 
#                 node.use(self.cur_req.mem)
#         for link in route_links:
#             link.use(self.cur_req.bw)

#     def reset(self,path,route_links,deployed_VNFs):
#         for node in path:
#             if node.type == 1:
#                 if node.used ==0 and self.cur_req.mem !=0:
#                     print("Wrong reset " +str((len(path))))
#                 node.use(-self.cur_req.mem)
#         for node in deployed_VNFs:
#             if node.type ==  1: 
#                 print("Wrong")
#             node.use(-self.cur_req.cpu)
#         for link in route_links:
#             link.use(-self.cur_req.bw)
            
#     def Routing(self,inv: Individual,K: int):
#         paths = []
#         for r in self.requests:
#             self.i +=1
#             src = r.ingress
#             dest = r.egress
#             self.cur_req = r
#             self.curr = self.network.nodes[src]
#             if self.curr.violated(r.mem) or self.network.nodes[dest].violated(r.mem):
#                 paths.append(None)
#                 continue
#             path = [self.curr]
#             route_links = []
#             served = True
#             deployed_VNFs = []
#             VNF_indices = []
#             for i in r.VNFs:
#                 vnf_node = []
#                 for v in self.network.MDC_nodes:
#                     if i in v.VNFs:
#                         vnf_node.append(v)
#                 self.path_k = self.getpaths(self.curr,vnf_node,K)
#                 if self.path_k is None:
#                     print(r)
#                 # n = self.select(inv,vnf_node,K)
#                 n = self.select_2(inv,vnf_node,self.path_k)
#                 if n == None:
#                     served = False
#                     break
#                 deployed_VNFs.append(n)
#                 if n.name == self.curr.name:
#                     VNF_indices.append(len(path)-1)
#                     self.curr = n
#                     n.use(self.cur_req.cpu)
#                     continue
#                 p,links = self.path_k[n.name]
#                 # p,links = self.getpath(self.curr,n,K)
#                 # for node in p:
#                 #     if node.name == '19':
#                 #         print(node.name)
#                 if p == None:
#                     print(self.curr.name)
#                     print(n.name)
#                 self.update(p,links)
#                 p.pop(0)
#                 path.extend(p)
#                 VNF_indices.append(len(path)-1)
#                 route_links.extend(links)
#                 self.curr = n 
#                 n.use(self.cur_req.cpu)
#             p,links = self.getpath(self.curr,self.network.nodes[dest],K)
#             if p == None or not served:
#                 if len(path) != 1:
#                     self.reset(path,route_links,deployed_VNFs)
#                 paths.append(None)
#                 continue
#             self.update(p,links)
#             p.pop(0)
#             path.extend(p)
#             route_links.extend(links)
#             sfc = SFC(r)
#             sfc.route_nodes = path 
#             sfc.route_links = route_links
#             sfc.VNF_indices = VNF_indices
#             paths.append(sfc)
#         return paths
#     def select(self,inv,vnf_node,K):
#         next = None
#         first = True
#         pitority = float('-inf')
#         for v in vnf_node:
#             if v.violated(self.cur_req.cpu):
#                 continue
#             self.path,self.route_links = self.getpath(self.curr,v,K)

#             if self.path == None:
#                 continue
#             if(first):
#                 next = v 
#                 self.next = v
#                 pitority = inv.chromosomes.GetOutput(self)
#                 first = False
#                 continue
#             self.next = v
#             tmp = inv.chromosomes.GetOutput(self)
#             if(tmp > pitority):
#                 next = v
#                 pitority = tmp
#         return next
#     def select_2(self,inv,vnf_node,paths):
#         next = None
#         first = True
#         pitority = float('-inf')
#         for v in vnf_node:
#             if v.violated(self.cur_req.cpu):
#                 continue
#             self.path,self.route_links = paths[v.name]
#             if self.path == None:
#                 continue
#             if(first):
#                 next = v 
#                 self.next = v
#                 pitority = inv.chromosomes.GetOutput(self)
#                 first = False
#                 continue
#             self.next = v
#             tmp = inv.chromosomes.GetOutput(self)
#             if(tmp > pitority):
#                 next = v
#                 pitority = tmp
#         return next
#     def isValid(self,path,links):
#         for node in path:
#             if node.type == 1 and node.violated(self.cur_req.mem):
#                 return False
#         for link in links:
#             if link.violated(self.cur_req.bw):
#                 return False
#         return True

#     def getpath(self,u,v,k):
#         mlgraph = MultiLayerGraph(self.network)
#         # print(mlgraph.G.nodes)
#         paths = mlgraph.find_SFCs(u.name,v.name,k)
#         for path in paths: 
#             if self.isValid(path[0],path[1]):
#                 return path
#         return None,None
#     def getpaths(self,u,vnf_node,k):
#         mlgraph = MultiLayerGraph(self.network)
#         # mlgraph = Graph(self.network)
#         # print(mlgraph.G.nodes)
#         rs = {}
#         for v in vnf_node:
#             paths = mlgraph.find_SFCs(u.name,v.name,k)
#             for path in paths: 
#                 if self.isValid(path[0],path[1]):
#                     rs[v.name] = path
#                     break
#             if v.name not in rs.keys():
#                 rs[v.name] = None,None
#         return rs
    
    
# class simple_gp:
#     def __init__(self,network,requests):
#         self.network = network
#         self.requests = requests
    
#     def undeploy(self, paths):
#         for path in paths:
#             if path != None:
#                 path.undeploy()
#     def evaluate(self, ind: Individual,K:int, alpha=0.01):
#         s = state(self.network,self.requests)
#         paths = s.Routing(ind,K) 
#         MLU = max(self.network.max_used_bandwidth(),
#                 self.network.max_used_cpu(),
#                 self.network.max_used_memory())
#         self.undeploy(paths)
#         cnt = 0 
#         for path in paths:
#             if path != None:
#                 cnt +=1
#         return (1-alpha) * cnt/len(paths) - alpha * MLU
    
#     def run_GP(self,K,pop_size=100, max_gen=50, crossover_rate=0.8, mutation_rate=0.05, alpha=0.01):
#         functions = [AddNode(),SubNode(),MulNode(),DivNode(),MaxNode(),MinNode()]
#         terminals = [NHNode(),BRNode(),TBRNode(),ERCNode(),CPUNode()]
#         min_height = 2
#         max_height = 8
#         initialization_max_tree_height = 4
#         pop = Population(pop_size, functions,terminals,min_height,max_height,initialization_max_tree_height,functools.partial(self.evaluate, K= K,alpha=alpha))
#         ind =  pop.run(max_gen, crossover_rate, mutation_rate)
#         return ind,pop.history
    
# def gp_x(network: Network, requests: list,K: int, alpha=0.01):
#     # First phase: find K potential paths for each request
#     network_tmp = deepcopy(network)
#     algorithm = simple_gp(network_tmp,requests)
#     start = time.process_time()
#     ind,hist = algorithm.run_GP(K)
#     end = time.process_time()
#     s = state(network_tmp,requests)
#     paths = s.Routing(ind,K)     
#     f1 = 0 
#     f2 = (network_tmp.max_used_bandwidth() + network_tmp.max_used_memory()+ network_tmp.max_used_cpu()) /3 
#     for path in paths:
#         if path is not None:
#             f1+=1
#             path.undeploy()
#     return Solution(network, paths),hist,end-start,(1-f1/len(requests),f2)

# class complex_gp:
#     def __init__(self,train):
#         self.train = train
    
#     def undeploy(self, paths):
#         for path in paths:
#             if path != None:
#                 path.undeploy()
#     def evaluate(self, ind: Individual,K:int, alpha=0.01):
#         fitness = 0 
#         for instance in self.train:
#             name,network,requests = instance
#             s = state(network,requests)
#             paths = s.Routing(ind,K) 
#             MLU = max(network.max_used_bandwidth(),
#                     network.max_used_cpu(),
#                     network.max_used_memory())
#             self.undeploy(paths)
#             cnt = 0 
#             for path in paths:
#                 if path != None:
#                     cnt +=1
#             fitness += (1-alpha) * cnt /len(requests) - alpha * MLU
#         return fitness/len(self.train)
#     def run_GP(self,K,pop_size=100, max_gen=50, crossover_rate=0.8, mutation_rate=0.05, alpha=0.01):
#         functions = [AddNode(),SubNode(),MulNode(),DivNode(),MaxNode(),MinNode()]
#         terminals = [NHNode(),BRNode(),TBRNode(),ERCNode(),CPUNode()]
#         min_height = 2
#         max_height = 8
#         initialization_max_tree_height = 4
#         pop = Population(pop_size, functions,terminals,min_height,max_height,initialization_max_tree_height,functools.partial(self.evaluate, K= K,alpha=alpha))
#         ind =  pop.run(max_gen, crossover_rate, mutation_rate)
#         return ind,pop.history
# def gp_ml(train,test ,K: int, alpha=0.01):
#     algorithm = complex_gp(train)
#     start = time.process_time()
#     ind,hist = algorithm.run_GP(K)
#     end = time.process_time()
#     results = []
#     instance_list = []
#     for instance in train: 
#         name,network,requests = instance
#         s = state(network,requests)
#         paths = s.Routing(ind,K)     
#         for path in paths:
#             if path is not None:
#                 path.undeploy()
#         results.append(Solution(network, paths))
#         instance_list.append(name)
#     for instance in test:
#         name,network,requests = instance
#         s = state(network,requests)
#         paths = s.Routing(ind,K)     
#         for path in paths:
#             if path is not None:
#                 path.undeploy()
#         results.append(Solution(network, paths))
#         instance_list.append(name)
#     return instance_list,results,hist,end-start

    
# if __name__ == '__main__':
#     network = file_to_network('./data/network.txt')
#     requests = file_to_requests('./data/requests.txt')[:20]
#     sol = gp_x(network, requests)

from gp.node.function import *
from gp.node.terminal import *
from gp.population.gp import *
from read_data import *
from decision_var import Decision

terminal = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR()]
terminal2 = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR()]
function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]        
pop = Population(10, function, terminal, 3, 8, 8, 100)
pop.random_init()
print(pop.indivs[0].chromosomes.GetHumanExpression())
data = Read_data(r'C:\Users\Admin\Documents\LAB\Virtural network\GP_Code\GP_Dynamic_VNF\data\input\cogent_centers_easy.json') 
request_list = data.get_R()
r = request_list[0]
print(r.VNFs)
vnf_source = {
    5:{
        "cpu": 1,
        "ram": 3,
        "mem": 2
    }
}
max_delay = {
    5: 10
}
X = Decision(r, 1, vnf_source, max_delay)
fitness = pop.indivs[0].chromosomes.GetOutput(X)
print(fitness)