
from functions.parameters.common import *
from functions.tps import distance

def dissonance(scale_degrees, inversion_degrees, dissonance_degrees, event):

    return (scale_degrees[event]
           + inversion_degrees[event]
           + dissonance_degrees[event])       

def inherited(subordination_matrix, 
              event, 
              dominating_chord, 
              dominating_chord_idx, 
              chord_functions, 
              current_key):
    
    if (subordination_matrix[event][event] == '0' 
        or subordination_matrix[event][event] == 0):
        sub_0_reached = True
    else:
        sub_0_reached = False
    inh_tension = 0
    intermediate_subordinate = dominating_chord
    intermediate_subordinate_idx= dominating_chord_idx
    while sub_0_reached == False:
        intermediate_dominating_idx = [x for x in range(len(subordination_matrix)) 
                                       if subordination_matrix[intermediate_subordinate_idx][x] != ''][0]
        intermediate_dominating = chord_functions[intermediate_dominating_idx]
        inh_tension += distance(current_key, 
                                intermediate_dominating,
                                intermediate_subordinate)[0]
        intermediate_subordinate_idx = intermediate_dominating_idx
        intermediate_subordinate = intermediate_dominating
        if (subordination_matrix[intermediate_subordinate_idx][intermediate_subordinate_idx] == '0' 
            or subordination_matrix[intermediate_subordinate_idx][intermediate_subordinate_idx] == 0):
            sub_0_reached = True
    return inh_tension