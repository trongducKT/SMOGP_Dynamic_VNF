from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from run_algorithm_selection.algorithms import *
from deployment.evaluation import calFitness_three_policies
from surrogate.gen_pc import *
from utils.crossover import *
from utils.mutation import *
from run_algorithm.train_Surrogate_NSGA_II import SurrogateNSGAPopulation
import multiprocessing
from surrogate.gen_surrogate_data import gen_surrogate
from data_info.read_data import *
import csv

if __name__ == '__main__':
    multiprocessing.freeze_support()
    data_nsf = [r'data_1_9/nsf_centers_easy_s3.json', r'data_1_9/nsf_rural_easy_s3.json',r'data_1_9/nsf_urban_easy_s3.json', r'data_1_9/nsf_uniform_easy_s3.json', r'data_1_9/nsf_rural_normal_s3.json', r'data_1_9/nsf_rural_hard_s3.json',
                 r'data_1_9/nsf_uniform_normal_s3.json', r'data_1_9/nsf_uniform_hard_s3.json', r'data_1_9/nsf_urban_normal_s3.json', r'data_1_9/nsf_urban_hard_s3.json',
                r'data_1_9/nsf_centers_normal_s3.json', r'data_1_9/nsf_centers_hard_s3.json']
    data_conus = [r'data_1_9/conus_centers_easy_s3.json', r'data_1_9/conus_rural_easy_s3.json',r'data_1_9/conus_urban_easy_s3.json', r'data_1_9/conus_uniform_easy_s3.json', r'data_1_9/conus_rural_normal_s3.json', r'data_1_9/conus_rural_hard_s3.json',
                 r'data_1_9/conus_uniform_normal_s3.json', r'data_1_9/conus_uniform_hard_s3.json', r'data_1_9/conus_urban_normal_s3.json', r'data_1_9/conus_urban_hard_s3.json',
                r'data_1_9/conus_centers_normal_s3.json', r'data_1_9/conus_centers_hard_s3.json']
    num_pro = 60
    num_train = 10
    pop_size = 50
    min_height = 2
    max_height = 8
    initialization_max_height = 4
    num_of_tour_particips = 2
    tournament_prob = 0.9
    pc = 0.9
    pm = 0.1
    num_neighbor = 5
    neighborhood_size = 3
    max_time = 10000
    crossover_operator_list = [crossover_branch_individual_swap, crossover_sub_tree_swap]
    mutation_operator_list = [mutation_individual_branch_replace, mutation_individual_node_replace, mutation_individual_branch_swap, mutation_value_determining]
    crossover_operator_list_1 = [crossover_branch_individual_swap]
    mutation_operator_list_1 = [mutation_individual_branch_replace]

 
    for data_path in data_conus:
        print(data_path)
        data = Read_data(data_path)
        ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server, ram_max_vnf, cpu_max_vnf, mem_max_vnf, max_bandwidth = data.get_info_network()
        function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
        terminal_determining = [DDR(), BR(max_bandwidth), RRS(sum_ram_server), 
                                CRS(sum_cpu_server), MRS(sum_mem_server), FirstVNF_RAM(ram_max_vnf),
                                FirstVNF_CPU(cpu_max_vnf), FirstVNF_Mem(mem_max_vnf), FirstVNF_RAM_Server(ram_max_server),
                                FirstVNF_CPU_Server(cpu_max_server), FirstVNF_Mem_Server(mem_max_server), ARS(ram_max_server),
                                ACS(cpu_max_server), AMS(mem_max_server), MDR(), PN(), Const()]
        
        terminal_ordering = [DDR(), BR(max_bandwidth), RRS(sum_ram_server), 
                                CRS(sum_cpu_server), MRS(sum_mem_server), FirstVNF_RAM(ram_max_vnf),
                                FirstVNF_CPU(cpu_max_vnf), FirstVNF_Mem(mem_max_vnf), FirstVNF_RAM_Server(ram_max_server),
                                FirstVNF_CPU_Server(cpu_max_server), FirstVNF_Mem_Server(mem_max_server), ARS(ram_max_server),
                                ACS(cpu_max_server), AMS(mem_max_server), MDR(), PN(), Const()]
        terminal_choosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUR(), MUM()]
        
        determining_tree = Const()


        node1 = SubNode()
        node1.AppendChild(PN())
        node1.AppendChild(DDR())

        node2 = AddNode()
        node2.AppendChild(MUC())
        node2.AppendChild(MUR())

        node3 = AddNode()
        node3.AppendChild(node2)
        node3.AppendChild(MUM())

        node4 = SubNode()
        node4.AppendChild(Zero_Node())
        node4.AppendChild(CS())

        node5 = SubNode()
        node5.AppendChild(node4)
        node5.AppendChild(node3)
        rule_ref = Ref_Rule(determining_tree, node1, node5)
        surrogate = Surrogate(20, rule_ref)
        surrogate.gen_situations_random(20, 50, 3, 10)
#         surrogate = gen_surrogate(data_path, num_train, 10, rule_ref)
        surrogate.cal_ordered_ref()
        pop = SurrogateNSGAPopulation(pop_size, function, terminal_determining, terminal_ordering, terminal_choosing,
                                      min_height, max_height, initialization_max_height, num_of_tour_particips,
                                      tournament_prob, pc, pm, None, surrogate, rule_ref, num_neighbor)
        pop.random_init()
        print("Surrogate")
        determining_tree_algorithm = None
        max_gen = 40
        objective_json, tree_json, test_objectives_json, time_objective, surrogate_objective, test_hv_surrogate, time_train = run_SurrogateNSGAII(data_path, num_pro, pop.indivs, num_train, function, terminal_determining, terminal_ordering,
                            terminal_choosing, pop_size, max_gen, min_height, max_height, initialization_max_height,
                            num_of_tour_particips, tournament_prob, pc, pm, crossover_operator_list, mutation_operator_list,
                            num_neighbor, surrogate, rule_ref, calFitness_three_policies, determining_tree_algorithm, max_time)
        
#         objective_json, tree_json, test_objectives_json, time_objective, test_hv_surrogate, time_train = run_NSGAII( data_path, num_pro, pop.indivs, num_train,  
#                 function, terminal_determining, terminal_ordering, terminal_choosing, 
#                 pop_size, max_gen,  min_height, max_height, initialization_max_height,  
#                 num_of_tour_particips, tournament_prob, pc, pm,
#                 crossover_operator_list_1, mutation_operator_list_1, calFitness_three_policies, determining_tree_algorithm, max_time)
        name_store = "Result_selection/Pareto_tree_history/Surrogate/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(tree_json, f)
        name_store = "Result_selection/Pareto_objective_history/Surrogate/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(objective_json, f)
        name_store = "Result_selection/Test_result/Surrogate/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(test_objectives_json, f)
        name_store = "Result_selection/time_objective/Surrogate/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(time_objective, f)
        
        max_gen = 1000
        print("NSGA-II")
        objective_json, tree_json, test_objectives_json, NFE_generation, test_hv_NSGAII, abc = run_NSGAII( data_path, num_pro, pop.indivs, num_train,  
                function, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                crossover_operator_list, mutation_operator_list, calFitness_three_policies, determining_tree_algorithm, time_train)
        name_store = "Result_selection/Pareto_tree_history/NSGAII/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(tree_json, f)
        name_store = "Result_selection/Pareto_objective_history/NSGAII/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(objective_json, f)
        name_store = "Result_selection/Test_result/NSGAII/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(test_objectives_json, f)
        name_store = "Result_selection/time_objective/NSGAII/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(NFE_generation, f)
        
        print("MOEAD")
        objective_json, tree_json, test_objectives_json, NFE_generation, test_hv_MOEAD = run_MOEAD( data_path, num_pro, pop.indivs, num_train,  
                function, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob, pc, pm,
                crossover_operator_list, mutation_operator_list, calFitness_three_policies, determining_tree_algorithm, 3, time_train)
        
        name_store = "Result_selection/Pareto_tree_history/MOEAD/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(tree_json, f)
        name_store = "Result_selection/Pareto_objective_history/MOEAD/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(objective_json, f)
        name_store = "Result_selection/Test_result/MOEAD/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(test_objectives_json, f)
        name_store = "Result_selection/time_objective/MOEAD/" + data_path[9:-5] + ".json"
        with open(name_store, 'w') as f:
            json.dump(NFE_generation, f)
            
        # Đường dẫn tới tệp CSV
        file_path = "Result_selection/result_test.csv"

        # Dữ liệu để ghi vào tệp CSV
        data_to_append = [
            {'name_path': data_path[9:-5], 'surrogate': test_hv_surrogate, 'nsga2': test_hv_NSGAII, 'moead': test_hv_MOEAD},
        ]

        # Mở tệp CSV trong chế độ ghi thêm ('a') và ghi dữ liệu
        with open(file_path, 'a', newline='') as csv_file:
            fieldnames = ['name_path', 'surrogate', 'nsga2', 'moead']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Ghi dữ liệu mới vào tệp CSV
            for row in data_to_append:
                writer.writerow(row)

#         objective_json, tree_json, test_objectives_json, NFE_generation = run_SPEA( data_path, num_pro, pop.indivs, num_train,  
#                 function, terminal_determining, terminal_ordering, terminal_choosing, 
#                 pop_size, max_gen,  min_height, max_height, initialization_max_height,  
#                 num_of_tour_particips, tournament_prob, pc, pm,
#                 crossover_operator_list, mutation_operator_list, calFitness_three_policies, None, max_time)
        
#         name_store = "Result_selection/Pareto_tree_history/SPEA/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(tree_json, f)
#         name_store = "Result_selection/Pareto_objective_history/SPEA/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(objective_json, f)
#         name_store = "Result_selection/Test_result/SPEA/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(test_objectives_json, f)
#         name_store = "Result_selection/time_objective/SPEA/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(NFE_generation, f)
#     data_set = [ r'data_1_9/nsf_centers_easy_s3.json', r'data_1_9/nsf_centers_normal_s3.json', r'data_1_9/nsf_centers_hard_s3.json',
#                 r'data_1_9/nsf_rural_easy_s3.json', r'data_1_9/nsf_rural_normal_s3.json', r'data_1_9/nsf_rural_hard_s3.json',
#                 r'data_1_9/nsf_uniform_easy_s3.json', r'data_1_9/nsf_uniform_normal_s3.json', r'data_1_9/nsf_uniform_hard_s3.json',
#                r'data_1_9/nsf_urban_easy_s3.json', r'data_1_9/nsf_urban_normal_s3.json', r'data_1_9/nsf_urban_hard_s3.json',]
#     max_time = 7200
#     data_set = [ 
#             r'data_1_9/conus_rural_easy_s3.json', r'data_1_9/conus_rural_normal_s3.json', r'data_1_9/conus_rural_hard_s3.json',
#             r'data_1_9/conus_uniform_easy_s3.json', r'data_1_9/conus_uniform_normal_s3.json', r'data_1_9/conus_uniform_hard_s3.json',
#             r'data_1_9/conus_urban_easy_s3.json', r'data_1_9/conus_urban_normal_s3.json', r'data_1_9/conus_urban_hard_s3.json',
#     r'data_1_9/conus_centers_easy_s3.json', r'data_1_9/conus_centers_normal_s3.json', r'data_1_9/conus_centers_hard_s3.json']
# #     data_set = [ r'data_1_9/nsf_rural_hard_s3.json', r'data_1_9/nsf_rural_easy_s3.json', r'data_1_9/nsf_rural_normal_s3.json',
# #                 r'data_1_9/nsf_uniform_easy_s3.json', r'data_1_9/nsf_uniform_normal_s3.json', r'data_1_9/nsf_uniform_hard_s3.json',
# #                 r'data_1_9/nsf_urban_easy_s3.json', r'data_1_9/nsf_urban_normal_s3.json', r'data_1_9/nsf_urban_hard_s3.json',]
#     for data_path in data_set:
#         print(data_path)
#         data = Read_data(data_path)
#         ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server, ram_max_vnf, cpu_max_vnf, mem_max_vnf, max_bandwidth = data.get_info_network()
#         function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
#         terminal_determining = [DDR(), BR(max_bandwidth), RRS(sum_ram_server), 
#                                 CRS(sum_cpu_server), MRS(sum_mem_server), FirstVNF_RAM(ram_max_vnf),
#                                 FirstVNF_CPU(cpu_max_vnf), FirstVNF_Mem(mem_max_vnf), FirstVNF_RAM_Server(ram_max_server),
#                                 FirstVNF_CPU_Server(cpu_max_server), FirstVNF_Mem_Server(mem_max_server), ARS(ram_max_server),
#                                 ACS(cpu_max_server), AMS(mem_max_server), MDR(), PN(), Const()]
        
#         terminal_ordering = [DDR(), BR(max_bandwidth), RRS(sum_ram_server), 
#                                 CRS(sum_cpu_server), MRS(sum_mem_server), FirstVNF_RAM(ram_max_vnf),
#                                 FirstVNF_CPU(cpu_max_vnf), FirstVNF_Mem(mem_max_vnf), FirstVNF_RAM_Server(ram_max_server),
#                                 FirstVNF_CPU_Server(cpu_max_server), FirstVNF_Mem_Server(mem_max_server), ARS(ram_max_server),
#                                 ACS(cpu_max_server), AMS(mem_max_server), MDR(), PN(), Const()]
#         terminal_choosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUR(), MUM()]

#         determining_tree = Const()


#         node1 = SubNode()
#         node1.AppendChild(PN())
#         node1.AppendChild(DDR())

#         node2 = AddNode()
#         node2.AppendChild(MUC())
#         node2.AppendChild(MUR())

#         node3 = AddNode()
#         node3.AppendChild(node2)
#         node3.AppendChild(MUM())

#         node4 = SubNode()
#         node4.AppendChild(Zero_Node())
#         node4.AppendChild(CS())

#         node5 = SubNode()
#         node5.AppendChild(node4)
#         node5.AppendChild(node3)
#         rule_ref = Ref_Rule(determining_tree, node1, node5)
#         surrogate = Surrogate(20, rule_ref)
#         surrogate.gen_situations_random(20, 50, 3, 10)
# #         print(len(surrogate.ordered_situations[0]))
# #         print(len(surrogate.determining_situations))
# #         print(len(surrogate.server_situations))
# #         surrogate = gen_surrogate(data_path, num_train, 10, rule_ref)
#         pop = SurrogateNSGAPopulation(pop_size, function, terminal_determining, terminal_ordering, terminal_choosing,
#                                       min_height, max_height, initialization_max_height, num_of_tour_particips,
#                                       tournament_prob, pc, pm, None, surrogate, rule_ref, num_neighbor)
#         pop.random_init()
#         print("Surrogate")
#         determining_tree_algorithm = None
#         objective_json, tree_json, test_objectives_json, time_objective, surrogate_objective, test_hv_surrogate = run_SurrogateNSGAII(data_path, num_pro, pop.indivs, num_train, function, terminal_determining, terminal_ordering,
#                             terminal_choosing, pop_size, max_gen, min_height, max_height, initialization_max_height,
#                             num_of_tour_particips, tournament_prob, pc, pm, crossover_operator_list_1, mutation_operator_list_1,
#                             num_neighbor, surrogate, rule_ref, calFitness_three_policies, determining_tree_algorithm, max_time)
    
#         name_store = "Result_selection/Pareto_tree_history/Surrogate/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(tree_json, f)
#         name_store = "Result_selection/Pareto_objective_history/Surrogate/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(objective_json, f)
#         name_store = "Result_selection/Test_result/Surrogate/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(test_objectives_json, f)
#         name_store = "Result_selection/time_objective/Surrogate/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(time_objective, f)
#         name_store = "Result_selection/Surrogate_evaluation/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(surrogate_objective, f)
        
#         print("NSGA-II")
#         objective_json, tree_json, test_objectives_json, NFE_generation, test_hv_NSGAII = run_NSGAII( data_path, num_pro, pop.indivs, num_train,  
#                 function, terminal_determining, terminal_ordering, terminal_choosing, 
#                 pop_size, max_gen,  min_height, max_height, initialization_max_height,  
#                 num_of_tour_particips, tournament_prob, pc, pm,
#                 crossover_operator_list, mutation_operator_list, calFitness_three_policies, determining_tree_algorithm, max_time)
#         name_store = "Result_selection/Pareto_tree_history/NSGAII/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(tree_json, f)
#         name_store = "Result_selection/Pareto_objective_history/NSGAII/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(objective_json, f)
#         name_store = "Result_selection/Test_result/NSGAII/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(test_objectives_json, f)
#         name_store = "Result_selection/time_objective/NSGAII/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(NFE_generation, f)
        
#         print("MOEAD")
#         objective_json, tree_json, test_objectives_json, NFE_generation, test_hv_MOEAD = run_MOEAD( data_path, num_pro, pop.indivs, num_train,  
#                 function, terminal_determining, terminal_ordering, terminal_choosing, 
#                 pop_size, max_gen,  min_height, max_height, initialization_max_height,  
#                 num_of_tour_particips, tournament_prob, pc, pm,
#                 crossover_operator_list, mutation_operator_list, calFitness_three_policies, determining_tree_algorithm, 3, max_time)
        
#         name_store = "Result_selection/Pareto_tree_history/MOEAD/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(tree_json, f)
#         name_store = "Result_selection/Pareto_objective_history/MOEAD/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(objective_json, f)
#         name_store = "Result_selection/Test_result/MOEAD/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(test_objectives_json, f)
#         name_store = "Result_selection/time_objective/MOEAD/" + data_path[9:-5] + ".json"
#         with open(name_store, 'w') as f:
#             json.dump(NFE_generation, f)
            
#         # Đường dẫn tới tệp CSV
#         file_path = "Result_selection/result_test.csv"

#         # Dữ liệu để ghi vào tệp CSV
#         data_to_append = [
#             {'name_path': data_path[9:-5], 'surrogate': test_hv_surrogate, 'nsga2': test_hv_NSGAII, 'moead': test_hv_MOEAD},
#         ]

#         # Mở tệp CSV trong chế độ ghi thêm ('a') và ghi dữ liệu
#         with open(file_path, 'a', newline='') as csv_file:
#             fieldnames = ['name_path', 'surrogate', 'nsga2', 'moead']
#             writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#             # Ghi dữ liệu mới vào tệp CSV
#             for row in data_to_append:
#                 writer.writerow(row)
