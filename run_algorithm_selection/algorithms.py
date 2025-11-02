from gp.node.function import *
from gp.node.terminal import *
from data_info.read_data import *
from network.network import Network
from utils.utils import *
from .train_NSGA_II import *
from .train_MOEAD import *
from .train_Surrogate_NSGA_II import trainSurrogateNSGAII
from .train_SPEA import *
import time


def run_NSGAII( data_path, processing_num, indi_list, num_train,  
                functions, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, max_NFE):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
    time_start = time.time()
    Pareto_front_generations, NFE_generations = trainNSGAII(processing_num, indi_list,  network, vnf_list, request_train,
                    functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, max_NFE)
    time_end = time.time()
    # Store the Pareto front and objective Pareto
    objective_json = {}
    tree_json = {}
    gen = 1
    for indi_list_gen in Pareto_front_generations:
        objectives= []
        trees = []
        for indi in indi_list_gen:
            objective_temp = {}
            tree_temp = {}
            objective_temp["obj1"] = indi.objectives[0]
            objective_temp["obj2"] = indi.objectives[1]
            tree_temp["determining"] = indi.determining_tree.GetHumanExpression()
            tree_temp["choosing"] = indi.choosing_tree.GetHumanExpression()
            tree_temp["obj1"] = indi.objectives[0]
            tree_temp["obj2"] = indi.objectives[1]
            objectives.append(objective_temp)
            trees.append(tree_temp)
        objective_json[str(gen)] = objectives
        tree_json[str(gen)] = trees
        gen += 1
    
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_test, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    hv_supported_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
        hv_supported_objectives.append([normal_reject, normal_cost])
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()
    print("Gia tri mục tiêu")
    test_hv = cal_hv(np.array(hv_supported_objectives), np.array([1, 1]))
    print(test_hv)
    return objective_json, tree_json, test_objectives_json, NFE_generations, test_hv, time_end - time_start

def run_MOEAD( data_path, processing_num, indi_list, num_train,  
                functions, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree,
                neighbor_num, max_NFE):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
    time_start = time.time()
    Pareto_front_generations, NFE_generations = trainMOGPD(processing_num, indi_list,  network, vnf_list, request_train,
                    functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree,
                neighbor_num, max_NFE)
    time_end = time.time()
    # Store the Pareto front and objective Pareto
    objective_json = {}
    tree_json = {}
    gen = 1
    for indi_list_gen in Pareto_front_generations:
        objectives= []
        trees = []
        for indi in indi_list_gen:
            objective_temp = {}
            tree_temp = {}
            objective_temp["obj1"] = indi.objectives[0]
            objective_temp["obj2"] = indi.objectives[1]
            tree_temp["determining"] = indi.determining_tree.GetHumanExpression()
            tree_temp["choosing"] = indi.choosing_tree.GetHumanExpression()
            tree_temp["obj1"] = indi.objectives[0]
            tree_temp["obj2"] = indi.objectives[1]
            objectives.append(objective_temp)
            trees.append(tree_temp)
        objective_json[str(gen)] = objectives
        tree_json[str(gen)] = trees
        gen += 1
    
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_test, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    hv_supported_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
        hv_supported_objectives.append([normal_reject, normal_cost])
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()
    print("Gia tri mục tiêu")
    test_hv = cal_hv(np.array(hv_supported_objectives), np.array([1, 1]))
    print(test_hv)
    return objective_json, tree_json, test_objectives_json, NFE_generations, test_hv

    


def run_SurrogateNSGAII(data_path, processing_num, indi_list, num_train,  
                        functions, terminal_determining, terminal_ordering, terminal_choosing, 
                        pop_size, max_gen, min_height, max_height, initialization_max_height,  
                        num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                        crossover_operator_list, mutation_operator_list, neighbor_num, 
                        situation_surrogate, ref_rule, calFitness, determining_tree, max_NFE,
                        surrogate_model_name='KNN'): 
    
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)

    get_max_cost_vnf(network.MDC_nodes, vnf_list)
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
            
    time_start = time.time()
    
    # TRUYỀN THÊM THAM SỐ surrogate_model_name VÀO trainSurrogateNSGAII
    Pareto_front_generations, NFE_generation, surrogate_objective, EP = trainSurrogateNSGAII(
        processing_num, indi_list, network, vnf_list, request_train,
        functions, terminal_determining, terminal_ordering, terminal_choosing, 
        pop_size, max_gen, min_height, max_height, initialization_max_height,  
        num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
        crossover_operator_list, mutation_operator_list, calFitness,
        situation_surrogate, ref_rule, neighbor_num, determining_tree, max_NFE,
        surrogate_model_name=surrogate_model_name # Tham số mới
    )
    
    time_end = time.time()
    
    # Store the Pareto front and objective Pareto
    objective_json = {}
    tree_json = {}
    gen = 1
    for indi_list_gen in Pareto_front_generations:
        objectives= []
        trees = []
        for indi in indi_list_gen:
            objective_temp = {}
            tree_temp = {}
            objective_temp["obj1"] = indi.objectives[0]
            objective_temp["obj2"] = indi.objectives[1]
            tree_temp["determining"] = indi.determining_tree.GetHumanExpression()
            tree_temp["choosing"] = indi.choosing_tree.GetHumanExpression()
            tree_temp["obj1"] = indi.objectives[0]
            tree_temp["obj2"] = indi.objectives[1]
            objectives.append(objective_temp)
            trees.append(tree_temp)
        objective_json[str(gen)] = objectives
        tree_json[str(gen)] = trees
        gen += 1
        
    # # Lựa chọn lời giải không bị thống trị (non-dominated) từ EP
    # non_dominated_EP = []
    # # Khởi tạo lại thuộc tính non-dominated
    # for individual in EP:
    #     individual.domination_count = 0
    #     individual.dominated_solutions = []

    # # Thực hiện kiểm tra thống trị (domination check)
    # for individual in EP:
    #     for other_individual in EP:
    #         if individual != other_individual: # Đảm bảo không so sánh với chính nó
    #             if individual.dominates(other_individual):
    #                 individual.dominated_solutions.append(other_individual)
    #             elif other_individual.dominates(individual):
    #                 individual.domination_count += 1
        
    # for individual in EP:
    #     if individual.domination_count == 0:
    #         individual.rank = 0
    #         non_dominated_EP.append(individual)

    # print("Số lời giải (EP non-dominated):", len(non_dominated_EP))
    
    # ĐÁNH GIÁ TRÊN TẬP TEST
    non_dominated_EP = Pareto_front_generations[-1]
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in non_dominated_EP:
        arg.append((indi, network, request_test, vnf_list))
        
    result = pool.starmap(calFitness, arg)
    
    test_objectives = []
    hv_supported_objectives = []
    for value in result:
        objectives_temp= {}
        # Giả sử calFitness trả về 4 giá trị: normal_reject, normal_cost, reject, cost
        normal_reject, normal_cost, reject, cost = value 
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
        # Sử dụng các mục tiêu đã chuẩn hóa (normalized) để tính HV (giả sử normal_reject và normal_cost là đã chuẩn hóa)
        hv_supported_objectives.append([normal_reject, normal_cost])
        
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    time_train = time_end - time_start
    test_objectives_json["time_train"] = time_train
    
    pool.close()
    
    # Tính Hypervolume trên tập Test
    test_hv = cal_hv(np.array(hv_supported_objectives), np.array([1, 1])) # Giả sử điểm tham chiếu là [1, 1]
    print("Giá trị HV trên tập Test:", test_hv)
    
    return objective_json, tree_json, test_objectives_json, NFE_generation, surrogate_objective, test_hv, time_train


def run_SPEA( data_path, processing_num, indi_list, num_train,  
                functions, terminal_determining, terminal_ordering, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, max_NFE):
    data = Read_data(data_path)
    request_list = data.get_R()
    vnf_list = data.get_F()
    node_list = data.get_V()
    link_node = data.get_E()

    network = Network()
    network.add_node_to_network(node_list)
    network.add_link_to_network(link_node)
    get_max_cost_vnf(network.MDC_nodes, vnf_list)
        
    request_train = []
    request_test = []
    for request in request_list:
        if request.arrival <= num_train:
            request_train.append(request)
        else: 
            request_test.append(request)
    time_start = time.time()
    Pareto_front_generations, NFE_generation = trainSPEA(processing_num, indi_list,  network, vnf_list, request_train,
                    functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                    pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                    num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, max_NFE)
    time_end = time.time()
    # Store the Pareto front and objective Pareto
    objective_json = {}
    tree_json = {}
    gen = 1
    for indi_list_gen in Pareto_front_generations:
        objectives= []
        trees = []
        for indi in indi_list_gen:
            objective_temp = {}
            tree_temp = {}
            objective_temp["obj1"] = indi.objectives[0]
            objective_temp["obj2"] = indi.objectives[1]
            tree_temp["determining"] = indi.determining_tree.GetHumanExpression()
            tree_temp["choosing"] = indi.choosing_tree.GetHumanExpression()
            tree_temp["obj1"] = indi.objectives[0]
            tree_temp["obj2"] = indi.objectives[1]
            objectives.append(objective_temp)
            trees.append(tree_temp)
        objective_json[str(gen)] = objectives
        tree_json[str(gen)] = trees
        gen += 1
    
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_test, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()
    return objective_json, tree_json, test_objectives_json, NFE_generation