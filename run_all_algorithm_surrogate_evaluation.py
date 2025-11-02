from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from utils.function_operator import *
from run_algorithm_selection.algorithms import *
from deployment.evaluation import calFitness_three_policies
from surrogate.gen_pc import *
from utils.crossover import *
from utils.mutation import *
from run_algorithm_selection.train_Surrogate_NSGA_II import SurrogateNSGAPopulation
import multiprocessing
from surrogate.gen_surrogate_data import gen_surrogate
from data_info.read_data import *
import csv
import json

if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    SURROGATE_MODELS = ['KNN', 'RF', 'MLP', 'SVM', 'XGB', 'LGBM', 'DT'] 
    
#     data_set = [r'data_1_9/conus_centers_easy_s3.json', r'data_1_9/conus_centers_normal_s3.json', r'data_1_9/conus_centers_hard_s3.json', 
#             r'data_1_9/conus_rural_easy_s3.json', r'data_1_9/conus_rural_normal_s3.json', r'data_1_9/conus_rural_hard_s3.json',
#             r'data_1_9/conus_uniform_easy_s3.json', r'data_1_9/conus_uniform_normal_s3.json', r'data_1_9/conus_uniform_hard_s3.json',
#             r'data_1_9/conus_urban_easy_s3.json', r'data_1_9/conus_urban_normal_s3.json', r'data_1_9/conus_urban_hard_s3.json']
    data_set = [r'data_1_9/nsf_centers_easy_s3.json', r'data_1_9/nsf_centers_normal_s3.json', r'data_1_9/nsf_centers_hard_s3.json', 
                r'data_1_9/nsf_rural_easy_s3.json', r'data_1_9/nsf_rural_normal_s3.json', r'data_1_9/nsf_rural_hard_s3.json',
                r'data_1_9/nsf_uniform_easy_s3.json', r'data_1_9/nsf_uniform_normal_s3.json', r'data_1_9/nsf_uniform_hard_s3.json',
                r'data_1_9/nsf_urban_easy_s3.json', r'data_1_9/nsf_urban_normal_s3.json', r'data_1_9/nsf_urban_hard_s3.json',]
    
    num_pro = 10
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
    max_gen = 5
    
    RESULT_CSV_FILE = 'Surrogate_Comparison_Summary.csv'
    # DANH SÁCH TOÁN TỬ
    crossover_operator_list = [crossover_branch_individual_swap, crossover_sub_tree_swap]
    mutation_operator_list = [mutation_individual_branch_replace, mutation_individual_node_replace, mutation_individual_branch_swap, mutation_value_determining]

    try:
        with open(RESULT_CSV_FILE, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Data_Name', 'Surrogate_Model', 'Test_HV', 'Train_Time_s'])
    except FileExistsError:
        # Nếu file đã tồn tại, tiếp tục ghi vào đó
        pass
    
    for data_path in data_set:
        print(f"\n==================== Dữ liệu: {data_path} ====================")
        data_name = data_path.split('/')[-1]
        # KHỞI TẠO CẤU TRÚC MẠNG VÀ THAM SỐ GP (KHÔNG ĐỔI GIỮA CÁC MÔ HÌNH)
        data = Read_data(data_path)
        ram_max_server, cpu_max_server, mem_max_server, sum_ram_server, sum_cpu_server, sum_mem_server, ram_max_vnf, cpu_max_vnf, mem_max_vnf, max_bandwidth = data.get_info_network()
        
        function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
        terminal_determining = [DDR(), BR(max_bandwidth), RRS(sum_ram_server), 
                                 CRS(sum_cpu_server), MRS(sum_mem_server), FirstVNF_RAM(ram_max_vnf),
                                 FirstVNF_CPU(cpu_max_vnf), FirstVNF_Mem(mem_max_vnf), FirstVNF_RAM_Server(ram_max_server),
                                 FirstVNF_CPU_Server(cpu_max_server), FirstVNF_Mem_Server(mem_max_server), ARS(ram_max_server),
                                 ACS(cpu_max_server), AMS(mem_max_server), MDR(), PN(), Const()]
        terminal_ordering = terminal_determining
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
        
        surrogate.cal_ordered_ref()

        pop = SurrogateNSGAPopulation(pop_size, function, terminal_determining, terminal_ordering, terminal_choosing,
                                      min_height, max_height, initialization_max_height, num_of_tour_particips,
                                      tournament_prob, pc, pm, None, surrogate, rule_ref, num_neighbor,
                                      surrogate_model_name='KNN') # Tên mô hình chỉ là tạm thời cho init
        pop.random_init()
        initial_indivs = [deepcopy(indi) for indi in pop.indivs]
        
        determining_tree_algorithm = None

        
        for model_name in SURROGATE_MODELS:
            print(f"\n--- Bắt đầu chạy với Mô hình Surrogate: {model_name} ---")
            
            # Reset population cho mỗi lần chạy mô hình
            pop_indivs_for_run = [deepcopy(indi) for indi in initial_indivs]
            
            # GỌI HÀM RUN
            objective_json, tree_json, test_objectives_json, time_objective, surrogate_objective, test_hv_surrogate, time_train = run_SurrogateNSGAII(
                data_path, num_pro, pop_indivs_for_run, num_train, function, terminal_determining, terminal_ordering,
                terminal_choosing, pop_size, max_gen, min_height, max_height, initialization_max_height,
                num_of_tour_particips, tournament_prob, pc, pm, crossover_operator_list, mutation_operator_list,
                num_neighbor, surrogate, rule_ref, calFitness_three_policies, determining_tree_algorithm, max_time,
                surrogate_model_name=model_name # TRUYỀN TÊN MÔ HÌNH VÀO RUN
            )
            
            print(f"Hoàn thành {model_name}. HV Test: {test_hv_surrogate:.4f}. Time train: {time_train:.2f}s")

            with open(RESULT_CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data_name, model_name, test_hv_surrogate, time_train]) # Ghi dữ liệu
            base_name = data_path[9:-5] 
            model_suffix = "_" + model_name
            
            name_store_tree = "Result_selection/Pareto_tree_history/Surrogate/" + base_name + model_suffix + ".json"
            with open(name_store_tree, 'w') as f:
                json.dump(tree_json, f)
            name_store_obj = "Result_selection/Pareto_objective_history/Surrogate/" + base_name + model_suffix + ".json"
            with open(name_store_obj, 'w') as f:
                json.dump(objective_json, f)
                
            name_store_test = "Result_selection/Test_result/Surrogate/" + base_name + model_suffix + ".json"
            with open(name_store_test, 'w') as f:
                json.dump(test_objectives_json, f)
                
            name_store_time = "Result_selection/time_objective/Surrogate/" + base_name + model_suffix + ".json"
            with open(name_store_time, 'w') as f:
                json.dump(time_objective, f)

            name_store_surr_obj = "Result_selection/surrogate_objective/Surrogate/" + base_name + model_suffix + ".json"
            with open(name_store_surr_obj, 'w') as f:
                json.dump(surrogate_objective, f)