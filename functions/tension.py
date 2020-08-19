

from functions.classes.sequence import Harmony
from functions.variables.tension_components import dissonance, inherited
from functions.classes.matrix import Reduction
from functions.tps import distance

def t_calculator(piece_data, prolongational_matrix):
    
    '''
    
    This function calculates the flow of global tension of a given piece of music 
    according to Lerdahl's model of tonal tension.
    It needs from a collection of parameters: 
    the piece's key, its events' chord functions, 
    the tension contribution related to their inversion, 
    the tension contribution related to existence of non-harmonic notes 
    and the tension contribution related to the scale degree of the notes in the melody. 
    The function also needs from a representation 
    of the piece's prolongational reduction 
    in the form of a matrix.
    '''
    

    chord_functions = Harmony(piece_data).chord_functions()
    scale_degrees = Harmony(piece_data).scale_degrees()
    inversion_degrees = Harmony(piece_data).inversion_degrees()
    dissonance_degrees = Harmony(piece_data).dissonance_degrees()
    keys = Harmony(piece_data).current_key()
    subordination_matrix = Reduction(prolongational_matrix).matrix()
    global_tension = []
    

    for event in range(len(chord_functions)):
                
        # Surface tension
        
        diss_tension = dissonance(scale_degrees, 
                                  inversion_degrees, 
                                  dissonance_degrees, 
                                  event)
        # TPS distance
        
        dominating_chord_idx = [x for x in range(len(chord_functions)) 
                                if subordination_matrix[event][x] != ''][0]
        dominating_chord = chord_functions[dominating_chord_idx]
        current_chord = chord_functions[event]
        current_key = keys[event]
        tps_distance = distance(current_key, 
                               dominating_chord,
                               current_chord)[0]

        # Inherited tension
        
        inh_tension = inherited(subordination_matrix, 
                                event, 
                                dominating_chord, 
                                dominating_chord_idx, 
                                chord_functions, 
                                current_key)
        
        # Global tension
        
        global_tension.append(diss_tension
                      + tps_distance
                      + inh_tension)
    
    return global_tension