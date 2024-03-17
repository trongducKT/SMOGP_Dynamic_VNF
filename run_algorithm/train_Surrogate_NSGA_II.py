from data_info.read_data import *
from network.network import Network
from utils.utils import *
from utils.function_operator import GenerateRandomTree
from gp.population.population import *
import time 
import multiprocessing     
import matplotlib.pyplot as plt
from surrogate.gen_pc import *
from surrogate.knn import *
from utils. function_operator import *
from utils.utils import cal_hv_front

class SurrogateNSGAPopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 initialize_operator, crossover_operator, mutation_operator, selection_operator, 
                 reproduce_opertation, situation_surrogate: Surrogate, ref_rule: Ref_Rule, neighbor_num):
        super().__init__(pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator)

        self.reproduce_opertation = reproduce_opertation
        self.situation_surrogate = situation_surrogate
        self.ref_rule = ref_rule
        self.neighbor_num = neighbor_num

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
            determining_tree = GenerateRandomTree( self.functions, self.determining_terminals, curr_max_depth, 
                                                        curr_height=0, 
                method='grow' if np.random.random() < .5 else 'full', min_height=self.min_height )
            choosing_tree = GenerateRandomTree( self.functions, self.choosing_terminals, curr_max_depth, 
                                                    curr_height=0, 
                method='grow' if np.random.random() < .5 else 'full', min_height=self.min_height )
            inv = Individual(determining_tree, choosing_tree)
            pc_indi = self.situation_surrogate.cal_pc(inv)
            pc_indi_tuple = tuple(pc_indi)
            if pc_indi_tuple not in pc_check:
                pc_check.add(pc_indi_tuple)
                inv.pc = pc_indi
                self.indivs.append(inv)
                i += 1
            else:
                continue
    
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
                    children1, children2 = crossover_operator(indi1, indi2, self.min_height, self.max_height)
                    for children in [children1, children2]:
                        pc_indi = self.situation_surrogate.cal_pc(children)
                        pc_indi_tuple = tuple(pc_indi)
                        if pc_indi_tuple not in pc_check:
                            children.pc = pc_indi
                            pc_check.add(pc_indi_tuple)
                            offspring.append(children)
            if np.random.random() < self.mutation_rate:
                for mutation_operator in mutation_operator_list:
                    mutant1 = mutation_operator(indi1, self.functions, self.determining_terminals, 
                                      self.choosing_terminals, self.min_height, self.max_height)
                    mutant2 = mutation_operator(indi2, self.functions, self.determining_terminals,
                                        self.choosing_terminals, self.min_height, self.max_height)
                    for mutant in [mutant1, mutant2]:
                        pc_indi = self.situation_surrogate.cal_pc(mutant)
                        pc_indi_tuple = tuple(pc_indi)
                        if pc_indi_tuple not in pc_check:
                            mutant.pc = pc_indi
                            pc_check.add(pc_indi_tuple)
                            offspring.append(mutant)
        return offspring
    
    def select_offspring(self, offspring):
        # x_train = np.array([indi.pc for indi in self.indivs])
        # y_train = np.array([[indi.rank, indi.rank_crowding_distance] for indi in self.indivs])
        x_train = []
        y_train = []
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
        return offspring[:int(self.pop_size/2)], offspring[int(self.pop_size/2):]
    
    def natural_selection(self, offspring):
        self.indivs.extend(offspring)
        self.cal_rank_individual()
        self.indivs.sort(key=lambda x: (x.rank, x.rank_crowding_distance))
        self.indivs = self.indivs[:self.pop_size]

    def remove_achive(self, offspring_achive):
        if len(offspring_achive) > self.pop_size:
            offspring_achive.sort(key = lambda x: x.age)
            return offspring_achive[:self.pop_size]
        return offspring_achive



    


def trainSurrogateNSGAII(processing_number, indi_list,  network, vnf_list, request_list,
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness,
                situation_surrogate, ref_rule, neighbor_num):
    

    # Return
    Pareto_front_generations = []
    hv = []
    pop = SurrogateNSGAPopulation(pop_size, functions, terminal_determining, terminal_choosing, min_height,
                                  max_height, initialization_max_height, num_of_tour_particips, tournament_prob,
                                  crossover_rate, mutation_rate, None, None, None, None, None, 
                                  situation_surrogate, ref_rule, neighbor_num)
    # pop.random_init()
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost, a = value
    
    print("Hoan thanh khoi tao")
    pop.natural_selection([])

    Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0]) 
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))

    offspring_achive = []
    for i in range(max_gen):
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        # Surrogate
        for indi in offspring_achive:
            indi.age = indi.age + 1
        offspring_achive = offspring_achive + offspring
        offspring_evaluation, offspring_no_evaluation = pop.select_offspring(offspring_achive)

        offspring_achive = pop.remove_achive(offspring_no_evaluation)

        arg = []
        for indi in offspring_evaluation:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring_evaluation, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost, a = value


        pop.natural_selection(offspring_evaluation)

        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
        
        print("The he ",i)
        for indi in pop.indivs:
            if(indi.rank == 0):
                print(indi.objectives)
                print("Ket thuc mot ca the")

        if len(hv) > 10:
            if hv[-1] - hv[-10] < 0.01:
                pool.close()
                break 
        # if checkChange(pop.history) == True and checkChange(pop.history) == True:
        #     break
        
    pool.close()
    return Pareto_front_generations


# Pareto front across generations (list of Individuals)