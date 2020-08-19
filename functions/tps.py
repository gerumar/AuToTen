
from functions.variables.tps_components import i, j, k

def distance(current_key, original_chord, destination_chord):
    
    '''
    
    This function calculates the distance between two chords in the Tonal Pitch Space.
    As inputs, the function needs from the transition's key, current_key,
    and the chords in the transition, original_chord and destination_chord.
    Use the alphabetic system to input the current key (e.g. C, a, Bb, g#, etcetera),
    where upper case denotes major keys and lower case denotes minor keys.
    Characters '#' and 'b' stand for sharp and flat, respectively.
    Use Roman Numeral analysis to input the original_chord and the destination_chord.   
    That is  X/Y, where X indicates a chord function and Y a key.   
    Input major functions (X) and major keys (Y) in upper case, 
    and minor functions (x) and minor keys (y) in lower case.
    When using non-diatonic functions,  add '#' (sharp), 'b' (flat) or 'n' (natural) characters
    preceding the corresponding function or key (e.g. bIII or #i).
    When using augmented or diminished diatonic chords, add '+' or '-' characters 
    following the chord function label respectively (e.g. I+/I or vii-/I). 
    Augmented chords (+) should be written in upper case (i.e. major third), 
    and diminished chords (-) should be written in lower case (i.e. minor third).
    When a chord function contains a diatonic seventh, use '7' following X or x (e.g. V7 or ii-7).
    Do not include characters concerning inversions or any other non-harmonic note.
    
    e.g.: 
    
        Calculating the distance in the Tonal Pitch Space 
        between the tonic chord (I/I) 
        and the Neapolitan sixth chord (bII/I) 
        in the key of C major (C).
    
        Inputs: (current_key='C', 
                original_chord='I/I', 
                destination_chord='bII/I')
        
        Output: (10, 0, 2, 8)
    
    The given outputs correspond to the distance (d = 10) in the Tonal Pitch Space
    and its components: i (= 0), j (= 2) and k (= 8).
    '''
    
    i_calc = i(current_key, original_chord, destination_chord)
    j_calc = j(current_key, original_chord, destination_chord)
    k_calc = k(current_key, original_chord, destination_chord)
    d = i_calc + j_calc + k_calc
    
    return d, i_calc, j_calc, k_calc
            