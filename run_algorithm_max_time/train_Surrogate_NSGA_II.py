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

class SurrogateNSGAPopulation(Population):
    def __init__(self, pop_size, 
                 functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree, 
                 situation_surrogate: Surrogate, ref_rule: Ref_Rule, neighbor_num):
        super().__init__(pop_size, 
                        functions, determining_terminals, ordering_terminals, choosing_terminals, 
                        min_height, max_height, initialization_max_tree_height, 
                        num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                        determining_tree)

        self.situation_surrogate = situation_surrogate
        self.ref_rule = ref_rule
        self.neighbor_num = neighbor_num
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
            if tuple(indi.objectives) not in self.objective_check:
                self.x_train.append(indi.pc)
                self.y_train.append([indi.objectives[0], indi.objectives[1]])
                self.objective_check.add(tuple(indi.objectives))
    
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
                        # print(pc_indi)
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
                        # print(pc_indi)
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
                    # print(pc_indi)
                    pc_check.add(pc_indi_tuple)
                    offspring.append(indi)
        return offspring
    

    def select_offspring(self, offspring):
        x_train = [indi.pc for indi in self.indivs]
        y_train = [[indi.rank, indi.rank_crowding_distance] for indi in self.indivs]
        objective_check = set()
        for indi in self.indivs:
            if tuple(indi.objectives) not in objective_check:
                x_train.append(indi.pc)
                y_train.append([indi.rank, indi.rank_crowding_distance])
                objective_check.add(tuple(indi.objectives))
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        for indi in offspring:
            x_new = np.array([indi.pc])
            indi.rank, indi.rank_crowding_distance = knn_predict_mean(x_train, y_train, x_new, self.neighbor_num)
        offspring.sort(key=lambda x: (x.rank, x.rank_crowding_distance))
        return offspring[:int(self.pop_size)], offspring[int(self.pop_size):]
    

    def select_offspring_objectives_predict(self, offspring):
        x_train = np.array(self.x_train)
        y_train = np.array(self.y_train)
        for indi in offspring:
            x_new = np.array([indi.pc])
            indi.objectives_predict[0], indi.objectives_predict[1] = knn_predict_mean(x_train, y_train, x_new, self.neighbor_num)
            indi.objectives[0] = indi.objectives_predict[0]
            indi.objectives[1] = indi.objectives_predict[1]
        parents = deepcopy(self.indivs)
        indi_selected = self.natural_selection(offspring)
        offspring = []
        for indi in indi_selected:
            if indi.extractly_evaluated == False:
                offspring.append(deepcopy(indi))
        self.indivs = parents
        return offspring


    def natural_selection(self, offspring):
        self.indivs.extend(offspring)
        self.cal_rank_individual()
        self.indivs.sort(key=lambda x: (x.rank, x.rank_crowding_distance))
        self.indivs = self.indivs[:self.pop_size]
        return self.indivs

    def remove_achive(self, offspring_achive):
        if len(offspring_achive) > self.pop_size:
            offspring_achive.sort(key = lambda x: x.age)
            return offspring_achive[:self.pop_size]
        return offspring_achive  


def trainSurrogateNSGAII_time(processing_number, indi_list,  network, vnf_list, request_list,
                         functions, terminal_determining, terminal_ordering, terminal_choosing, 
                         pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                        num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                        crossover_operator_list, mutation_operator_list, calFitness,
                        situation_surrogate, ref_rule, neighbor_num, determining_tree, max_time):
    

    # Return
    time_objective = {}
    Pareto_front_generations = []
    hv = []
    time_start = time.time()
    pop = SurrogateNSGAPopulation(pop_size, 
                                    functions, terminal_determining, terminal_ordering, terminal_choosing, 
                                    min_height, max_height, initialization_max_height, 
                                    num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                                    determining_tree, 
                                    situation_surrogate, ref_rule, neighbor_num)
    # pop.random_init()
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost = value
        indi.extractly_evaluated = True
    # pop.update_train_data(pop.indivs)
    print(pop.y_train)
    print("Hoan thanh khoi tao")
    pop.natural_selection([])
    Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0]) 
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
    print("The he 0: ", hv[-1])
    time_objective[0] = {"time": time.time() - time_start, "HV": hv[-1]}

    offspring_achive = []
    for i in range(max_gen):
        if time.time() - time_start >= max_time:
            pool.close()
            break
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        Surrogate
        for indi in offspring_achive:
            indi.age = indi.age + 1
        offspring_achive = offspring_achive + offspring
        offspring_evaluation, offspring_no_evaluation = pop.select_offspring(offspring_achive)
        offspring_achive = pop.remove_achive(offspring_no_evaluation)
        # offspring_evaluation = pop.select_offspring_objectives_predict(offspring)
        # number_indi = min(max_NFE - used_NFE, len(offspring_evaluation))
        # offspring_evaluation = offspring_evaluation[:number_indi]
        print(len(offspring_evaluation))

        arg = []
        for indi in offspring_evaluation:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring_evaluation, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost = value
            indi.extractly_evaluated = True

        pop.update_train_data(offspring_evaluation)
        pop.natural_selection(offspring_evaluation)
        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
        
        print("The he ", i+ 1, ":", hv[-1])
        time_objective[i + 1] = {"time": time.time() - time_start, "HV": hv[-1]}

        if len(hv) > 10:
            if hv[-1] - hv[-10] < 0.001:
                pool.close()
                break 
        
    pool.close()
    return Pareto_front_generations, time_objective