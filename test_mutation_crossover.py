from gp.node.terminal import *
from gp.node.function import *
from gp.population.gp import *

function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
terminal_chosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR(), Const()]

pop = Population(10, function, terminal_chosing, 2, 4, 4, 10)

pop.random_init()

# for indi in pop.indivs:
#     print(indi.chromosomes.GetHumanExpression())
#     print(indi.chromosomes.GetSubtree())
#     print(indi.chromosomes.GetDepth())
#     print(indi.chromosomes.GetHeight())
    

# indi = pop.indivs[-1]
# print(indi.chromosomes.GetHumanExpression())
# print(indi.chromosomes.GetHeight())
# indi_mutation = pop.mutation(indi.chromosomes, 4, 2)
# print(indi_mutation.GetHumanExpression())
# print(indi_mutation.GetHeight())


indi_crossover = pop.crossover(pop.indivs[-1].chromosomes, pop.indivs[-2].chromosomes, 4, 2)
print(pop.indivs[-1].chromosomes.GetHumanExpression())
print(pop.indivs[-2].chromosomes.GetHumanExpression())
print(pop.indivs[-1].chromosomes.GetSubtree())
print(pop.indivs[-2].chromosomes.GetSubtree())
print(indi_crossover.GetHumanExpression())
print(indi_crossover.GetHeight())