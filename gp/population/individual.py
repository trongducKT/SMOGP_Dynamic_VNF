import numpy as np
class Individual:
    def __init__(self, determining_tree, choosing_tree):
        self.determining_tree = determining_tree
        self.choosing_tree = choosing_tree
        self.objectives = np.zeros(2)
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None # be dominated
        self.dominated_solutions = None # dominate
        self.pc = []
    # Dominate operator
    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)   
    # Individual equation
    def __eq__(self, other):
        # Tree 1
        expr1 = self.determining_tree.GetHumanExpression()
        expr2 = other.determining_tree.GetHumanExpression()
        if expr1 != expr2:
            return False
        # Tree 2
        expr1 = self.choosing_tree.GetHumanExpression()
        expr2 = other.choosing_tree.GetHumanExpression()
        if expr1 != expr2:
            return False
        return True