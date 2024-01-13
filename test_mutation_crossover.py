from gp.node.function import *
from gp.node.terminal import *
from gp.population.population import *
from gp.population.ultis import reproduction, natural_selection, random_init
from run_algorithm.gp_algorithm import *
from deployment.evaluation import calFitness
function = [AddNode(), SubNode(), MulNode(), DivNode(), MaxNode(), MinNode()]
terminal_decision = [DDR(), BR(), RRS(), CRS(), MRS(), ARS(), CRS(), MRS(), MDR(), PN(), Const()]
terminal_chosing = [RCSe(), RRSe(), RMSe(), MLU(), CS(), DS(), MUC(), MUM(), MUR(), Const()]
