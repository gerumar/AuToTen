
import os
import sys

sys.path.append(os.getcwd()+'/tests')
from transition_cases import distance_tests
from sequences_cases import tension_tests

sys.path.append(os.getcwd()+'/functions')
from functions.tps import distance
from functions.tension import t_calculator
from functions.attraction import a_calculator
from functions.prolongation import generator
from functions.metre import offset
from functions.surface import parameters_finder
