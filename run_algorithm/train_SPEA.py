import heapq

import numpy as np

from gp.population.individual import Individual
from gp.population.population import Population
import multiprocessing
import random
from utils.function_operator import fast_nondominated_sort

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
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                 initialize_operator, crossover_operator, mutation_operator, selection_operator):
        super().__init__(pop_size, functions, determining_terminals, choosing_terminals, 
                 min_height, max_height, initialization_max_tree_height, 
                 num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator) 
    def reproduction(self):
        offspring = []
        for i in range(self.pop_size):
            indi1, indi2 = random.choices(self.indivs, k=2)
            if np.random.random() < self.crossover_rate:
                children1, children2 = self.crossover_operator(indi1, indi2, self.min_height, self.max_height)
                offspring.extend([children1, children2])
            if np.random.random() < self.mutation_rate:
                mutant1 = self.mutation_operator(indi1, self.functions, self.determining_terminals, 
                                    self.choosing_terminals, self.min_height, self.max_height)
                mutant2 = self.mutation_operator(indi2, self.functions, self.determining_terminals,
                                    self.choosing_terminals, self.min_height, self.max_height)
                offspring.extend([mutant1, mutant2])
        return offspring
    def SPEA_selection(self):
        self.indivs = environmental_selection(self.indivs, self.pop_size)
    def natural_selection(self):
        fast_nondominated_sort(self)
def trainSPEA(processing_number, network, vnf_list, request_list,
                functions, terminal_determining, terminal_choosing, 
                pop_size, max_gen,  min_height, max_height, initialization_max_height,  
                num_of_tour_particips, tournament_prob,crossover_rate, mutation_rate,
                initialize_operator, crossover_operator, mutation_operator, selection_operator,
                calFitness):
    Pareto_front_generations = []
    
    pop = SPEAPopulation(pop_size, functions, terminal_determining, terminal_choosing,
                          min_height, max_height, initialization_max_height,
                          num_of_tour_particips, tournament_prob, crossover_rate, mutation_rate,
                          initialize_operator, crossover_operator, mutation_operator, selection_operator)
    pop.initialize()

    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    result = pool.starmap(calFitness, arg)
    # len_decision = len(pop.indivs)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0],indi.objectives[1], indi.reject, indi.cost, a = value
    print("Hoan thanh khoi tao")      
    for i in range(max_gen):
        offspring = pop.reproduction()
        print("reproduction xong")
        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0],indi.objectives[1],  indi.reject, indi.cost, a = value

        pop.indivs.extend(offspring)
        pop.SPEA_selection()
        pop.natural_selection()    

        Pareto_front_generations.append([indi for indi in pop.indivs if indi.rank == 0])  
        print("The he ",i)
        for indi in pop.indivs:
            if(indi.rank == 0):
                print(indi.objectives)
                print(indi.determining_tree.GetHumanExpression())
                print(indi.choosing_tree.GetHumanExpression())
                print("Ket thuc mot ca the")
        
    pool.close()
    return Pareto_front_generations


# Pareto front across generations (list of Individuals)