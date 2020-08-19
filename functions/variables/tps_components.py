
from functions.parameters.common import *
from functions.classes.parser import Scale
from functions.classes.notes import Notes
from functions.classes.space import Space

def i(current_key, original_chord, destination_chord):
    
    # Calculating basic spaces at levels (d) and (e)
    
    original_level_d = Space(current_key, original_chord).level_d()
    destination_level_d = Space(current_key, destination_chord).level_d()
    
    # Number of setps in the ascending chromatic circle-of-fifths
    
    ascending_signed_i = 0
    while original_level_d != destination_level_d:
        original_level_d = original_level_d[5:]+original_level_d[:5]
        ascending_signed_i += 1
        
    # Number of steps in the descending chromatic circle-of-fifths  
    
    original_level_d = Space(current_key, original_chord).level_d()
    descending_signed_i = 0
    while original_level_d != destination_level_d:
        original_level_d = original_level_d[7:]+original_level_d[:7]
        descending_signed_i += 1

    # Selecting the direction in the circle-of-fifths
    
    original_alphabet_key = Scale(current_key, original_chord).alphabet_key() 
    destination_alphabet_key = Scale(current_key, destination_chord).alphabet_key() 
    if (original_alphabet_key
        in list(sum(sharp_keys, ()))
        and destination_alphabet_key
        in list(sum(sharp_keys, ()))):
        original_idx = [x for x in range(len(sharp_keys))
                       if original_alphabet_key
                        in sharp_keys[x]][0]
        destination_idx = [x for x in range(len(sharp_keys))
                       if destination_alphabet_key 
                           in sharp_keys[x]][0]
        if original_idx <= destination_idx:
            signed_i = ascending_signed_i
        else:
            signed_i = -1*descending_signed_i            
    elif (original_alphabet_key
          in list(sum(flat_keys, ())) 
          and destination_alphabet_key 
          in list(sum(flat_keys, ()))):       
        original_idx = [x for x in range(len(flat_keys))
                       if original_alphabet_key
                        in flat_keys[x]][0]
        destination_idx = [x for x in range(len(flat_keys))
                       if destination_alphabet_key
                           in flat_keys[x]][0]
        if original_idx >= destination_idx:
            signed_i = ascending_signed_i
        else:
            signed_i = -1*descending_signed_i      
    else:
        if ascending_signed_i <= descending_signed_i:
            signed_i = ascending_signed_i
        else:
            signed_i = -1*descending_signed_i
    if abs(signed_i) > 7:
        return -1*abs(signed_i) % 12
    return abs(signed_i)

def circle_fifths(current_key, original_chord, destination_chord):
    
    # Reading the value of i
    
    i_value = i(current_key, original_chord, destination_chord)
    
    # If original chord is in both circles,
    # its direction gets determined by the sign of i,
    # otherwise, it depends on the list it can be found
    
    original_alphabet_key = Scale(current_key, original_chord).alphabet_key() 
    destination_alphabet_key = Scale(current_key, destination_chord).alphabet_key() 
    if (original_alphabet_key 
       in list(sum(sharp_keys, ()))
       and original_alphabet_key
        in list(sum(flat_keys, ()))):
        if i_value >= 0:
            direction = sharp_keys
        else:
            direction = flat_keys        
    elif (original_alphabet_key
        in list(sum(sharp_keys, ()))):
        direction = sharp_keys
    else:
        direction = flat_keys
    circle_fifths = [x[0] for x in direction]
    original_idx = [x for x in range(len(chromatic_scale)) 
                    if original_alphabet_key
                    in direction[x]][0]
    circle_fifths = (circle_fifths[original_idx:] 
                     + circle_fifths[:original_idx])     
    
    # Ensure the destination chord is found at the i_th position
    
    circle_fifths[abs(i_value)] = destination_alphabet_key
    return circle_fifths

def j(current_key, original_chord, destination_chord):

    left_right = (1, -1)
    j_values = []

    # Two directions: ascending and descending
    
    for direction in range(2):
        original_space = Space(current_key, original_chord).chordal_space()
        destination_space = Space(current_key, destination_chord).chordal_space()
        original_idx = original_space.index(
            Notes(current_key, original_chord).root())
        destination_idx = destination_space.index(
            Notes(current_key, destination_chord).root())
        chord_reached = False
        local_j = 0
        while not chord_reached:  
            if original_space[original_idx] == destination_space[destination_idx]:             
                chord_reached = True
            elif original_space == destination_space:
                original_idx = (
                    (original_idx 
                     + 4*left_right[direction]) 
                    % 7)
                local_j += 1
            else:
                original_idx = (
                    (original_idx 
                     + 4*left_right[direction]) 
                    % 7)
                next_key = next(iter(circle_fifths(
                    current_key, 
                    original_chord, 
                    destination_chord)[1:])
                               )
                if(original_space[original_idx] 
                   == destination_space[original_idx]):
                    original_space = destination_space
                elif(original_space[original_idx]
                    in Scale(next_key, 'I/I').local_diatonic_scale()):
                    original_space = Space(next_key, 'I/I').chordal_space()
                local_j += 1
            if local_j > len(chromatic_scale):
                chord_reached = True
        j_values.append(local_j)  
    return min(j_values)     

def k(current_key, original_chord, destination_chord):
    original_basic_space = Space(current_key, original_chord).basic_space()
    destination_basic_space = Space(current_key, destination_chord).basic_space()
    
    k_differences = [destination_basic_space[x] 
                     - original_basic_space[x] 
                     for x in range(len(chromatic_scale))]
    k_values = [x 
                if x > 0 
                else 0 
                for x in k_differences]
    return sum(k_values)