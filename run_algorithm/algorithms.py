from gp.node.function import *
from gp.node.terminal import *
from data_info.read_data import *
from network.network import Network
from utils.utils import *
from .train_NSGA_II import *
from .train_MOEAD import *
from .train_Surrogate_NSGA_II import trainSurrogateNSGAII
from .train_SPEA import *


def run_NSGAII( data_path, processing_num, indi_list, num_train,  
                functions, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                calFitness):
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
    Pareto_front_generations = trainNSGAII(
                processing_num, indi_list,  network, vnf_list, request_list,
                functions, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                calFitness)
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

    day = time.strftime("%d_%m_%Y")
    object_file_name = "./Pareto_objective_history/NSGAII/"+ str(day) +"_" + data_path[11:-5] + ".json"
    front_file_name = "./Pareto_tree_history/NSGAII/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(object_file_name, 'w') as file:
        json.dump(objective_json, file)
    with open(front_file_name, 'w') as file:
        json.dump(tree_json, file)
    
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost, history = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()

    test_file_name = "./Test_result/NSGAII/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(test_file_name, 'w') as file:
        json.dump(test_objectives_json, file)

def run_MOEAD(data_path, processing_num, indi_list,  num_train,  
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                crossover_rate, mutation_rate, 
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                neighborhood_size,
                calFitness):
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
    Pareto_front_generations = trainMOGPD(processing_num,indi_list,  network, vnf_list, request_list,
               functions, terminal_determining, terminal_choosing,
               pop_size, max_gen, min_height, max_height, initialization_max_height,
               crossover_rate, mutation_rate, neighborhood_size,
               initialize_operator, crossover_operator, mutation_operator, selection_operator,
               calFitness)
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

    day = time.strftime("%d_%m_%Y")
    object_file_name = "./Pareto_objective_history/MOEAD/"+ str(day) +"_" + data_path[11:-5] + ".json"
    front_file_name = "./Pareto_tree_history/MOEAD/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(object_file_name, 'w') as file:
        json.dump(objective_json, file)
    with open(front_file_name, 'w') as file:
        json.dump(tree_json, file)
    
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost, history = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()

    test_file_name = "./Test_result/MOEAD/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(test_file_name, 'w') as file:
        json.dump(test_objectives_json, file)

    


def run_SurrogateNSGAII(data_path, processing_num,indi_list,  num_train,  
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, neighbor_num, situation_surrogate, ref_rule,
                calFitness):
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
    Pareto_front_generations = trainSurrogateNSGAII(processing_num,indi_list,  network, vnf_list, request_list,
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness,
                situation_surrogate, ref_rule, neighbor_num)
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

    day = time.strftime("%d_%m_%Y")
    object_file_name = "./Pareto_objective_history/Surrogate/"+ str(day) +"_" + data_path[11:-5] + ".json"
    front_file_name = "./Pareto_tree_history/Surrogate/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(object_file_name, 'w') as file:
        json.dump(objective_json, file)
    with open(front_file_name, 'w') as file:
        json.dump(tree_json, file)

    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost, history = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()

    test_file_name = "./Test_result/Surrogate/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(test_file_name, 'w') as file:
        json.dump(test_objectives_json, file)


def run_SPEA( data_path, processing_num,indi_list,  num_train,  
                functions, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                calFitness):
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
    Pareto_front_generations = trainSPEA(
                processing_num,indi_list,  network, vnf_list, request_list,
                functions, terminal_decision, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                calFitness)
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

    day = time.strftime("%d_%m_%Y")
    object_file_name = "./Pareto_objective_history/SPEA/"+ str(day) +"_" + data_path[11:-5] + ".json"
    front_file_name = "./Pareto_tree_history/SPEA/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(object_file_name, 'w') as file:
        json.dump(objective_json, file)
    with open(front_file_name, 'w') as file:
        json.dump(tree_json, file)
    
    pool = multiprocessing.Pool(processes=processing_num)
    arg = []
    for indi in Pareto_front_generations[-1]:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    test_objectives = []
    for value in result:
        objectives_temp= {}
        normal_reject, normal_cost, reject, cost, history = value
        objectives_temp["normal_reject"] = normal_reject
        objectives_temp["normal_cost"] = normal_cost
        objectives_temp["reject"] = reject
        objectives_temp["cost"] = cost
        test_objectives.append(objectives_temp)
    test_objectives_json = {}
    test_objectives_json["test_result"] = test_objectives
    test_objectives_json["time_train"] = time_end - time_start
    pool.close()

    test_file_name = "./Test_result/SPEA/"+ str(day) +"_" + data_path[11:-5] + ".json"
    with open(test_file_name, 'w') as file:
        json.dump(test_objectives_json, file)