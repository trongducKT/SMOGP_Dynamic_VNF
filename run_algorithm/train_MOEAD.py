import multiprocessing
import random
import sys
import time

import matplotlib.pyplot as plt

from gp.population.individual import Individual
from gp.population.population import Population
from gp.population.ultis import crossover, mutation, GenerateRandomTree
from utils.utils import *


def init_weight_vectors_2d(pop_size):
    wvs = []
    for i in np.arange(0, 1 + sys.float_info.epsilon, 1 / (pop_size - 1)):
        wvs.append([i, 1 - i])
    return np.array(wvs)


class MOGPDPopulation(Population):
    def __init__(self, pop_size, functions, determining_terminals, choosing_terminals, min_height, max_height,
                 initialization_max_tree_height, crossover_rate, mutation_rate,
                 neighborhood_size, initialize_operator):
        super().__init__(pop_size, functions, determining_terminals, choosing_terminals, min_height, max_height,
                         initialization_max_tree_height, None, None, crossover_rate,
                         mutation_rate, None, initialize_operator, None)
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
        # print(B)
        return B

    def reproduction(self):
        O = []
        for i in range(self.pop_size):
            i1, i2 = random.sample(self.neighborhoods[i], 2)
            O.append(self.pair_reproduction(self.indivs[i1], self.indivs[i2]))
        return O

    def pair_reproduction(self, individual1, individual2):
        operator_prob = np.random.rand()
        # SD = np.linalg.norm(individual1.objectives - individual2.objectives)
        # print("SD", SD)

        # crossover
        if operator_prob > self.crossover_rate:
            part_crossover = np.random.rand()
            # determining tree crossover
            if part_crossover < 1 / 3:
                o1 = crossover(individual1.determining_tree, individual2.determining_tree, self.max_height)
                height1 = o1.GetHeight()
                if self.min_height <= height1 <= self.max_height:
                    return Individual(o1, individual1.choosing_tree)
            # choosing tree crossover
            elif part_crossover > 2 / 3:
                o1 = crossover(individual1.choosing_tree, individual2.choosing_tree, self.max_height)
                height2 = o1.GetHeight()
                if self.min_height <= height2 <= self.max_height:
                    return Individual(individual1.determining_tree, o1)
            # both trees crossover
            else:
                o1 = crossover(individual1.determining_tree, individual2.determining_tree, self.max_height)
                height1 = o1.GetHeight()
                if self.min_height <= height1 <= self.max_height:
                    o2 = crossover(individual1.choosing_tree, individual2.choosing_tree, self.max_height)
                    height2 = o2.GetHeight()
                    if self.min_height <= height2 <= self.max_height:
                        return Individual(o1, o2)

        # mutation
        elif operator_prob < self.mutation_rate:
            part_mutation = np.random.rand()
            # determining tree mutation
            if part_mutation < 1 / 3:
                o = mutation(individual1.determining_tree, self.functions, self.determining_terminals,
                             self.min_height.self.max_height)
                height1 = o.GetHeight()
                if self.min_height <= height1 <= self.max_height:
                    return Individual(o, individual1.choosing_tree)
            # choosing tree mutation
            elif part_mutation > 2 / 3:
                o = mutation(individual1.choosing_tree, self.functions, self.choosing_terminals,
                             self.min_height, self.max_height)
                height2 = o.GetHeight()
                if self.min_height <= height2 <= self.max_height:
                    return Individual(individual1.determining_tree, o)
            # both trees mutation
            else:
                o1 = mutation(individual1.determining_tree, self.functions, self.determining_terminals,
                              self.min_height, self.max_height)
                height1 = o1.GetHeight()
                if self.min_height <= height1 <= self.max_height:
                    o2 = mutation(individual1.choosing_tree, self.functions, self.choosing_terminals,
                                  self.min_height, self.max_height)
                    height2 = o2.GetHeight()
                    if self.min_height <= height2 <= self.max_height:
                        return Individual(o1, o2)

        # reproduction
        tree1 = GenerateRandomTree(self.functions, self.determining_terminals,
                                   self.max_height, min_height=self.min_height)
        tree2 = GenerateRandomTree(self.functions, self.choosing_terminals,
                                   self.max_height, min_height=self.min_height)
        return Individual(tree1, tree2)

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


def trainMOGPD(processing_number, network, vnf_list, request_list,
               functions, terminal_decision, terminal_choosing,
               pop_size, max_gen, min_height, max_height, initialization_max_height,
               crossover_rate, mutation_rate, neighborhood_size,
               initialize_operator,
               calFitness):
    fitness_history = {}
    fitness_history["decision"] = []
    fitness_history["chosing"] = []
    time_start = time.time()

    pop = MOGPDPopulation(pop_size, functions, terminal_decision, terminal_choosing,
                          min_height, max_height, initialization_max_height,
                          crossover_rate, mutation_rate, neighborhood_size, initialize_operator)
    pop.initialize()

    print("Danh sach ca the khoi tao")
    for indi in pop.indivs:
        print(indi.determining_tree.GetHumanExpression())
        print(indi.choosing_tree.GetHumanExpression())
    print("Khoi tao xong")
    pop.update_external(pop.indivs)

    pool = multiprocessing.Pool(processes=processing_number)
    arg = []
    for indi in pop.indivs:
        arg.append((indi, network, request_list, vnf_list))
    print("Bat dau tinh fitness")
    result = pool.starmap(calFitness, arg)
    # len_decision = len(pop.indivs)
    for indi, value in zip(pop.indivs, result):
        indi.objectives[0], indi.objectives[1], indi.reject, indi.cost, a = value
    print("Tinh fitness xong")
    sum_gen = 0
    for i in range(max_gen):
        offspring = pop.reproduction()

        arg = []
        for indi in offspring:
            arg.append((indi, network, request_list, vnf_list))
        result = pool.starmap(calFitness, arg)
        for indi, value in zip(offspring, result):
            indi.objectives[0], indi.objectives[1], indi.reject, indi.cost, a = value

        pop.update_external(offspring)
        pop.indivs.extend(offspring)
        pop.natural_selection()

        sum_gen = i + 1
        print("The he ", i)
        for indi in pop.indivs:
            if indi.rank == 0:
                print(indi.objectives)
                print(indi.determining_tree.GetHumanExpression())
                print(indi.choosing_tree.GetHumanExpression())
                print("Ket thuc mot ca the")
        if checkChange(pop.history) == True and checkChange(pop.history) == True:
            break

        if True:
            x = [indi.objectives[0] for indi in pop.indivs if indi.rank == 0]
            y = [indi.objectives[1] for indi in pop.indivs if indi.rank == 0]
            print(len(x))
            plt.scatter(x, y)
            plt.show()
    pool.close()
    return sum_gen, time.time() - time_start, fitness_history