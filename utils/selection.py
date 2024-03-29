# Fast Non-dominated Sort
def fast_nondominated_sort(pop):
    pop.ParetoFront = [[]]
    for individual in pop.indivs:
        individual.domination_count = 0
        individual.dominated_solutions = []
        for other_individual in pop.indivs:
            if individual.dominates(other_individual):
                individual.dominated_solutions.append(other_individual)
            elif other_individual.dominates(individual):
                individual.domination_count += 1
        if individual.domination_count == 0:
            individual.rank = 0
            pop.ParetoFront[0].append(individual)
    i = 0
    while len(pop.ParetoFront[i]) > 0:
        temp = []
        for individual in pop.ParetoFront[i]:
            for other_individual in individual.dominated_solutions:
                other_individual.domination_count -= 1
                if other_individual.domination_count == 0:
                    other_individual.rank = i + 1
                    temp.append(other_individual)
        i = i + 1
        pop.ParetoFront.append(temp)


def calculate_crowding_distance(front):
    if len(front) > 0:
        solutions_num = len(front)
        for individual in front:
            individual.crowding_distance = 0

        for m in range(len(front[0].objectives)):
            front.sort(key=lambda individual: individual.objectives[m])
            front[0].crowding_distance = 10 ** 9
            front[solutions_num - 1].crowding_distance = 10 ** 9
            m_values = [individual.objectives[m] for individual in front]
            scale = max(m_values) - min(m_values)
            if scale == 0: scale = 1
            for i in range(1, solutions_num - 1):
                front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale

# Crowding Operator
def crowding_operator( individual, other_individual):
    if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (
                    individual.crowding_distance > other_individual.crowding_distance)):
        return 1
    else:
        return -1

def natural_selection(pop):
    fast_nondominated_sort(pop)
    new_indivs = []
    new_fronts = []
    front_num = 0
    while len(new_indivs) + len(pop.ParetoFront[front_num]) <= pop.pop_size:
        new_indivs.extend(pop.ParetoFront[front_num])
        new_fronts.append(pop.ParetoFront[front_num])
        if len(new_indivs) == pop.pop_size:
            break
        front_num += 1
    calculate_crowding_distance(pop.ParetoFront[front_num])
    pop.ParetoFront[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
    new_indivs.extend(pop.ParetoFront[front_num][0:pop.pop_size - len(new_indivs)])
    new_fronts.append(pop.ParetoFront[front_num][0:pop.pop_size - len(new_indivs)])
    pop.ParetoFront = new_fronts
    pop.indivs = new_indivs