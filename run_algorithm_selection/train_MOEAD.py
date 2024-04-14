import multiprocessing
import random
import sys
from gp.population.population import Population
from utils.utils import *
from utils.initialization import individual_init
from utils.selection import calculate_crowding_distance
import time

def init_weight_vectors_2d(pop_size):
    wvs = []
    for i in np.arange(0, 1 + sys.float_info.epsilon, 1 / (pop_size - 1)):
        wvs.append([i, 1 - i])
    return np.array(wvs)


class MOGPDPopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree, neighborhood_size):
        super().__init__(pop_size, 
                 functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree)
        self.neighborhood_size = neighborhood_size
        self.external_pop = []
        self.weights = init_weight_vectors_2d(self.pop_size)
        self.neighborhoods = self.init_neighborhood()

    def init_neighborhood(self):
        B = np.empty([self.pop_size, self.neighborhood_size], dtype=int)
        for i in range(self.pop_size):
            wv = self.weights[i]
            euclidean_distances = np.empty([self.pop_size], dtype=float)
            for j in range(self.pop_size):
                euclidean_distances[j] = np.linalg.norm(wv - self.weights[j])
            B[i] = np.argsort(euclidean_distances)[:self.neighborhood_size]
        return B

    def reproduction(self, crossover_operator_list, mutation_operator_list):
        offspring = []
        for i in range(self.pop_size):
            i1, i2 = random.sample(self.neighborhoods[i].tolist(), 2)
            indi1 = self.indivs[i1]
            indi2 = self.indivs[i2]
            if np.random.random() < self.crossover_rate:
                for crossover_operator in crossover_operator_list:
                    children1, children2 = crossover_operator(indi1, indi2, self.min_height, self.max_height, self.determining_tree)
                    offspring.extend([children1, children2])
            if np.random.random() < self.mutation_rate:
                for mutation_operator in mutation_operator_list:
                    mutant1 = mutation_operator(indi1, self.functions, 
                                                self.determining_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, self.determining_tree)
                    mutant2 = mutation_operator(indi2, self.functions, 
                                                self.determining_terminals, self.ordering_terminals, self.choosing_terminals, 
                                                self.min_height, self.max_height, self.determining_tree)
                    offspring.extend([mutant1, mutant2])
            if np.random.random() < 1 - self.crossover_rate - self.mutation_rate:
                indi = individual_init(self.min_height, self.max_height, self.determining_tree, self.functions,
                                       self.determining_terminals, self.ordering_terminals, self.choosing_terminals)
                offspring.append(indi)
        return offspring

    def natural_selection(self):
        self.indivs, O = self.indivs[:self.pop_size], self.indivs[self.pop_size:]
        for i in range(self.pop_size):
            indi = O[i]
            wv = self.weights[i]
            value_indi = np.sum(wv * indi.objectives)
            for j in self.neighborhoods[i]:
                if value_indi < np.sum(wv * self.indivs[j].objectives):
                    self.indivs[j] = indi

    def update_external(self, indivs: list):
        for indi in indivs:
            old_size = len(self.external_pop)
            self.external_pop = [other for other in self.external_pop
                                 if not indi.dominates(other)]
            if old_size > len(self.external_pop):
                self.external_pop.append(indi)
                continue
            for other in self.external_pop:
                if other.dominates(indi):
                    break
            else:
                self.external_pop.append(indi)
        
        ########## len(self.external_pop) = pop_size based on crowding distance
        calculate_crowding_distance(self.external_pop)
        self.external_pop.sort(key=lambda indi: indi.crowding_distance, reverse=True)
        self.external_pop = self.external_pop[:self.pop_size]


def trainMOGPD(processing_number, indi_list,  network, vnf_list, request_list,
                functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree, neighborhood_size, max_time):
    
    # Return
    time_objective = {}
    Pareto_front_generations = []
    hv = []
    time_start = time.time()
    pop = MOGPDPopulation(pop_size, functions, terminal_determining, terminal_ordering, terminal_choosing, 
                 min_height, max_height, initialization_max_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree, neighborhood_size)
    # pop.initialize()
    pop.pre_indi_gen(indi_list)
    pop.update_external(pop.indivs)

    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0], indi.objectives[1], indi.reject, indi.cost = value
    print("Khởi tạo xong")

    
    Pareto_front_generations.append(pop.external_pop)
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
    time_objective[0] = {"time": time.time() - time_start, "HV": hv[-1]}
    print("The he 0: ", hv[-1])
    for i in range(max_gen):
        if time.time() - time_start >= max_time:
            pool.close()
            break
        offspring = pop.reproduction(crossover_operator_list, mutation_operator_list)
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0], indi.objectives[1], indi.reject, indi.cost = value
        pop.update_external(offspring)
        pop.indivs.extend(offspring)
        pop.natural_selection()

        Pareto_front_generations.append(pop.external_pop)
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
        time_objective[i + 1] = {"time": time.time() - time_start, "HV": hv[-1]}
        print("The he ", i + 1, ": ", hv[-1]) 
    pool.close()
    return Pareto_front_generations, time_objective