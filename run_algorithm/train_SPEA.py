import heapq

import numpy as np

from gp.population.individual import Individual
from gp.population.population import Population
import multiprocessing
import random
from utils.selection import fast_nondominated_sort
from utils.initialization import individual_init
from utils.utils import *
import time

def distance(p1: Individual, p2: Individual):
    return np.linalg.norm(p1.objectives - p2.objectives)


def fitness_assignment(P: list):
    N = len(P)
    # calculate raw fitness R
    dominators = np.empty(N, dtype=object)
    S = np.zeros(N, dtype=int)
    R = np.empty(N, dtype=float)
    for i, p in enumerate(P):
        dominators[i] = []
        for j, q in enumerate(P):
            if i != j and q.dominates(p):
                dominators[i].append(j)
                S[j] += 1
    for i in range(N):
        R[i] = sum(S[j] for j in dominators[i])

    # Calculate density D
    k = int(np.sqrt(N))
    D = np.empty(N, dtype=float)
    for i, p in enumerate(P):
        distances = [distance(p, q) for q in P if p != q]
        if len(distances) == 0:
            print(P)
        assert k <= len(distances)
        sigma = heapq.nsmallest(k, distances)[-1]
        D[i] = 1 / (sigma + 2)

    F = R + D
    for i, p in enumerate(P):
        p.F = F[i]
    return F


def environmental_selection(P: list, N: int):
    F = fitness_assignment(P)
    P1_idx = [i for i, p in enumerate(P) if p.F < 1]

    # add
    if len(P1_idx) < N:
        dominated = [i for i, p in enumerate(P) if p.F >= 1]
        dominated.sort(key=lambda i: F[i])
        P1_idx.extend(dominated[:N - len(P1_idx)])
    # truncate
    else:
        while len(P1_idx) > N:
            N1 = len(P1_idx)
            mat = np.empty([N1, N1], dtype=float)
            for i in range(N1):
                for j in range(N1):
                    mat[i, j] = float('inf') if i == j else distance(P[P1_idx[i]], P[P1_idx[j]])
            np.sort(mat, axis=0)
            candidates = list(range(N1))
            for j in range(N1):
                candidates = [i for i in candidates if mat[i, j] ==
                              min([mat[i, j] for i in candidates])]
                if len(candidates) == 1:
                    break
            del P1_idx[candidates[0]]

    return [P[idx] for idx in P1_idx]

class SPEAPopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree):
        super().__init__(pop_size, 
                 functions, determining_terminals, ordering_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 determining_tree) 
    def gen_offspring(self, crossover_operator_list, mutation_operator_list):
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
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
    def SPEA_selection(self):
        self.indivs = environmental_selection(self.indivs, self.pop_size)
    def natural_selection(self):
        fast_nondominated_sort(self)
def trainSPEA_time(processing_number, indi_list,  network, vnf_list, request_list,
                functions, terminal_determining,terminal_ordering,  terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                crossover_operator_list, mutation_operator_list, calFitness, determining_tree,
                max_time):

    time_objective = {}
    Pareto_front_generations = []
    hv = []
    time_start = time.time()
    pop = SPEAPopulation(pop_size, functions, terminal_determining, terminal_ordering, terminal_choosing, 
                        min_height, max_height, initialization_max_height, 
                        num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                        determining_tree)
    # pop.initialize()
    pop.pre_indi_gen(indi_list)
    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    # len_decision = len(pop.indivs)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost= value 
    print("Khởi tạo xong")
    pop.SPEA_selection()
    pop.natural_selection()   
    Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0]) 
    hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
    time_objective[0] = {"time": time.time() - time_start, "HV": hv[-1]}
    print("The he 0: ", hv[-1])

    for i in range(max_gen):
        if time.time() - time_start >= max_time:
            pool.close()
            break
        offspring = pop.gen_offspring(crossover_operator_list, mutation_operator_list)
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost = value

        pop.indivs.extend(offspring)
        pop.SPEA_selection()
        pop.natural_selection()    

        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])  
        hv.append(cal_hv_front(Pareto_front_generations[-1], np.array([1, 1])))
        time_objective[i + 1] = {"time": time.time() - time_start, "HV": hv[-1]}
        print("The he ", i+1, ": ", hv[-1])
     
    pool.close()
    return Pareto_front_generations, time_objective


# Pareto front across generations (list of Individuals)