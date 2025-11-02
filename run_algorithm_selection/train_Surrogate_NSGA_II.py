from data_info.read_data import *
from network.network import Network
from utils.utils import *
from gp.population.population import *
import multiprocessing     
from surrogate.gen_pc import *
from surrogate.knn import *
from utils.utils import cal_hv_front
from utils.initialization import *
from utils.selection import *
import time
from sklearn.neighbors import KNeighborsRegressor

from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.tree import DecisionTreeRegressor

class SurrogateNSGAPopulation(Population):
    def __init__(self, pop_size, 
                    functions, determining_terminals, ordering_terminals, choosing_terminals, 
                    min_height, max_height, initialization_max_tree_height, 
                    num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                    determining_tree, 
                    situation_surrogate: Surrogate, ref_rule: Ref_Rule, neighbor_num,
                    surrogate_model_name='KNN'): 
            
            super().__init__(pop_size, 
                            functions, determining_terminals, ordering_terminals, choosing_terminals, 
                            min_height, max_height, initialization_max_tree_height, 
                            num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                            determining_tree)

            self.situation_surrogate = situation_surrogate
            self.ref_rule = ref_rule
            self.neighbor_num = neighbor_num
            self.surrogate_model_name = surrogate_model_name # Lưu tên mô hình
            self.x_train = []
            self.y_train = []
            self.objective_check = set()

    def random_init(self):
        curr_max_depth = self.min_height
        init_depth_interval = self.pop_size / (self.initialization_max_tree_height - self.min_height + 1)
        next_depth_interval = init_depth_interval
        i = 0
        pc_check = set()
        while i < self.pop_size:
            if i >= next_depth_interval:
                next_depth_interval += init_depth_interval
                curr_max_depth += 1
            inv = individual_init(self.min_height, curr_max_depth, self.determining_tree, self.functions,
                                  self.determining_terminals, self.ordering_terminals, self.choosing_terminals)
            pc_indi = self.situation_surrogate.cal_pc(inv)
            pc_indi_tuple = tuple(pc_indi)
            if pc_indi_tuple not in pc_check:
                pc_check.add(pc_indi_tuple)
                inv.pc = pc_indi
                self.indivs.append(inv)
                i += 1
            else:
                continue
    
    def update_train_data(self, indi_list):
        for indi in indi_list:
                self.x_train.append(indi.pc)
                self.y_train.append([indi.objectives[0], indi.objectives[1]])
    
    def cal_rank_individual(self):
        fast_nondominated_sort(self)
        for front in self.ParetoFront:
            calculate_crowding_distance(front)
            front.sort(key=lambda x: x.crowding_distance, reverse=True)
            for i, indi in enumerate(front):
                indi.rank_crowding_distance = i


    def gen_offspring(self, crossover_operator_list, mutation_operator_list):
        offspring = []
        pc_check = set()
        for indi in self.indivs:
            pc_indi_tuple = tuple(indi.pc)
            pc_check.add(pc_indi_tuple)
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
            if np.random.random() < self.crossover_rate:
                for crossover_operator in crossover_operator_list:
                    children1, children2 = crossover_operator(indi1, indi2, self.min_height, self.max_height, self.determining_tree)
                    for children in [children1, children2]:
                        pc_indi = self.situation_surrogate.cal_pc(children)
                        pc_indi_tuple = tuple(pc_indi)
                        if pc_indi_tuple not in pc_check:
                            children.pc = pc_indi
                            pc_check.add(pc_indi_tuple)
                            offspring.append(children)
            if np.random.random() < self.mutation_rate:
                for mutation_operator in mutation_operator_list:
                    mutant1 = mutation_operator(indi1, self.functions, 
                                                self.determining_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, self.determining_tree)
                    mutant2 = mutation_operator(indi2, self.functions, 
                                                self.determining_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, self.determining_tree)
                    for mutant in [mutant1, mutant2]:
                        pc_indi = self.situation_surrogate.cal_pc(mutant)
                        pc_indi_tuple = tuple(pc_indi)
                        if pc_indi_tuple not in pc_check:
                            mutant.pc = pc_indi
                            pc_check.add(pc_indi_tuple)
                            offspring.append(mutant)
            if np.random.random() < 1 - self.crossover_rate - self.mutation_rate:
                indi = individual_init(self.min_height, self.max_height, self.determining_tree, self.functions,
                                       self.determining_terminals, self.ordering_terminals, self.choosing_terminals)
                pc_indi = self.situation_surrogate.cal_pc(indi)
                pc_indi_tuple = tuple(pc_indi)
                if pc_indi_tuple not in pc_check:
                    indi.pc = pc_indi
                    pc_check.add(pc_indi_tuple)
                    offspring.append(indi)
        return offspring
    
    def remove_duplicated_objective(self, indi_list):
        group_list = []
        for indi in indi_list:
            in_the_group = False
            for group in group_list:
                if group[0].objectives[0] == indi.objectives[0] and group[0].objectives[1] == indi.objectives[1]:
                    group.append(indi)
                    in_the_group = True
                    break
            if in_the_group == False:
                group_list.append([indi])
        selected_indivs = []
        for group in group_list:
            best_height = max([group[0].determining_tree.GetHeight(), group[0].ordering_tree.GetHeight(), group[0].choosing_tree.GetHeight()])
            best_index = 0
            for i in range(1, len(group)):
                current_height = max([group[i].determining_tree.GetHeight(), group[i].ordering_tree.GetHeight(), group[i].choosing_tree.GetHeight()])
                if current_height < best_height:
                    best_height = current_height
                    best_index = i
            selected_indivs.append(group[best_index])
        return selected_indivs 

    def select_offspring_objectives_predict(self, offspring):
            x_train = np.array(self.x_train)
            y_train = np.array(self.y_train)
            off_new = []
            for indi in offspring:
                off_new.append(indi.pc)
            off_new = np.array(off_new)
            
            # Các mô hình đa mục tiêu (KNN, RF, MLP)
            if self.surrogate_model_name == 'RF':
                model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
                model.fit(x_train, y_train)
                predicted_costs = model.predict(off_new)
            elif self.surrogate_model_name == 'MLP':
                model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, activation='relu', solver='adam', random_state=42)
                model.fit(x_train, y_train)
                predicted_costs = model.predict(off_new)
            elif self.surrogate_model_name == 'KNN':
                model = KNeighborsRegressor(n_neighbors=self.neighbor_num, n_jobs=-1, weights='distance')
                model.fit(x_train, y_train)
                predicted_costs = model.predict(off_new)
                
            # Các mô hình đơn mục tiêu (SVR, XGBoost, LightGBM, Decision Tree)
            elif self.surrogate_model_name in ['SVM', 'XGB', 'LGBM', 'DT']:
                
                if self.surrogate_model_name == 'SVM':
                    model_cls = SVR
                    params = {'kernel':'rbf', 'C':100, 'gamma':0.1}
                elif self.surrogate_model_name == 'XGB':
                    model_cls = xgb.XGBRegressor
                    params = {'n_estimators': 100, 'objective': 'reg:squarederror', 'random_state': 42, 'n_jobs': -1}
                elif self.surrogate_model_name == 'LGBM':
                    model_cls = lgb.LGBMRegressor
                    params = {'n_estimators': 100, 'objective': 'regression', 'random_state': 42, 'n_jobs': -1}
                elif self.surrogate_model_name == 'DT':
                    model_cls = DecisionTreeRegressor
                    params = {'random_state': 42}
                
                # Trainning for Objective 1
                model1 = model_cls(**params)
                model1.fit(x_train, y_train[:, 0])
                pred1 = model1.predict(off_new)
                
                # Trainning for Objective 2
                model2 = model_cls(**params)
                model2.fit(x_train, y_train[:, 1])
                pred2 = model2.predict(off_new)
                
                predicted_costs = np.column_stack((pred1, pred2))
                
            else:
                raise ValueError(f"Unknown surrogate model: {self.surrogate_model_name}")

            # CẬP NHẬT KẾT QUẢ DỰ ĐOÁN CHUNG
            for indi, objective_pred in zip(offspring, predicted_costs):
                indi.objectives_predict[0] = objective_pred[0]
                indi.objectives_predict[1] = objective_pred[1]
                indi.objectives[0] = indi.objectives_predict[0]
                indi.objectives[1] = indi.objectives_predict[1]
                
            offspring_nonevaluation = []
            return offspring, offspring_nonevaluation

    def natural_selection(self):
        EP = natural_selection_1(self)
        return EP
    

    def remove_achive(self, offspring_achive):
        if len(offspring_achive) > self.pop_size:
            offspring_achive.sort(key = lambda x: x.age)
            return offspring_achive[:int(5*self.pop_size)]
        return offspring_achive  


def trainSurrogateNSGAII(processing_number, indi_list,  network, vnf_list, request_list,
                         functions, terminal_determining, terminal_ordering, terminal_choosing, 
                         pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                         num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                         crossover_operator_list, mutation_operator_list, calFitness,
                         situation_surrogate, ref_rule, neighbor_num, determining_tree, max_time,
                         surrogate_model_name='KNN'):
    
    EP = []
    # Return
    time_objective = {}
    Pareto_front_generations = []
    hv = []
    surrogate_objectives = {}
    time_start = time.time()
    pop = SurrogateNSGAPopulation(pop_size, 
                                    functions, terminal_determining, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, initialization_max_height, 
                                    num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                                    determining_tree, 
                                    situation_surrogate, ref_rule, neighbor_num,
                                    surrogate_model_name=surrogate_model_name)
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost = value
        indi.extractly_evaluated = True
    pop.update_train_data(pop.indivs)
    print("Hoan thanh khoi tao")
    non_dominated_solution = pop.natural_selection()
    Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0]) 
    EP.extend(non_dominated_solution)
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
    print("The he 0: ", hv[-1])
    time_objective[0] = {"time": time.time() - time_start, "HV": hv[-1]}
    for i in range(max_gen):
        if time.time() - time_start >= max_time:
            pool.close()
            break
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        print("The number of offspring:", len(offspring))
        offspring_evaluation, a = pop.select_offspring_objectives_predict(offspring)
        arg = []
        for indi in offspring_evaluation:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        predict_objectives_1 = []
        extractly_objectvies_1 = []
        predict_objectives_2 = []
        extractly_objectvies_2 = []
        for indi, value in zip(offspring_evaluation, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost = value
            indi.extractly_evaluated = True
            predict_objectives_1.append(indi.objectives_predict[0])
            extractly_objectvies_1.append(indi.objectives[0])
            predict_objectives_2.append(indi.objectives_predict[1])
            extractly_objectvies_2.append(indi.objectives[1])
        
        pop.indivs.extend(offspring_evaluation)
        non_dominated_solution = pop.natural_selection()
        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])
        EP.extend(non_dominated_solution)
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
        
        print("The he ", i+ 1, ":", hv[-1])
        time_objective[i + 1] = {"time": time.time() - time_start, "HV": hv[-1]}

        rmse1 = np.sqrt(mean_squared_error(extractly_objectvies_1, predict_objectives_1))
        rmse2 = np.sqrt(mean_squared_error(extractly_objectvies_2, predict_objectives_2))
        surrogate_objectives[i + 1] = {"predict1": predict_objectives_1, "extractly1": extractly_objectvies_1,
                                         "predict2": predict_objectives_2, "extractly2": extractly_objectvies_2,
                                         "rmse1": rmse1, "rmse2": rmse2} 
        print(f"   RMSE Objective 1: {rmse1:.4f}, RMSE Objective 2: {rmse2:.4f}")   
    pool.close()
    return Pareto_front_generations, time_objective, surrogate_objectives, EP