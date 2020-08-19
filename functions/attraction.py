

import csv
from music21 import *

from functions.parameters.common import *
from functions.classes.space import Space
from functions.tps import distance


def a_calculator(attraction_parameters):
    
    '''
    
    This function calculates the flow of harmonic attraction 
    of a given piece of music according to 
    Lerdahl's model of tonal tension.
    '''
    
    # Reading intermediate parameters
    
    (final_notes,
     final_key,
     final_label,
     keys,
     key_idx) = attraction_parameters
    
    # Calculating octave-range
    
    octaves = []
    for x in final_notes:
        for y in x:
            if int(y[-1]) not in octaves:
                octaves.append(int(y[-1]))
    octaves.sort()
    octaves = [str(x) for x in octaves]
    ranges = []
    for x in octaves:
        for y in chromatic_scale:
             ranges.append((y[0]+x,y[1]+x))
                
    diatonic_functions = ('i','ii','iii','iv','v','vi, vii')
    
    previous = final_notes[0]
    harmonic_attraction = []
    previous_d = 1
    for x in range(1,len(final_notes)):

        # Calculating anchoring spaces
        
        if final_key[x-1].isupper():
            scale1 = Space(final_key[x-1],'I/I').basic_space()
        else:
            scale1 = Space(final_key[x-1],'i/i').basic_space()      
        anchoring1 = []
        for y in scale1:
            if y == 5:
                anchoring1.append(4)
            elif y == 4:
                anchoring1.append(3)
            else:
                anchoring1.append(y)
        anchoring1 = anchoring1*len(ranges)    

        if final_key[x].isupper():
            scale2 = Space(final_key[x],'I/I').basic_space()
        else:
            scale2 = Space(final_key[x],'i/i').basic_space()      
        anchoring2 = []
        for y in scale2:
            if y == 5:
                anchoring2.append(4)
            elif y == 4:
                anchoring2.append(3)
            else:
                anchoring2.append(y)
        anchoring2 = anchoring2*len(ranges)        

        # calculating attraction

        v1 = previous
        v2 = final_notes[x]
        if len(previous) < len(final_notes[x]):
            for y in range(len(final_notes[x])-len(previous)):
                v1.append(previous[-1])
        elif len(final_notes[x]) < len(previous):
            for y in range(len(previous)-len(final_notes[x])):
                v2.append(final_notes[x])
        mel_att = []
        for y in range(len(v1)):
            for z in range(len(ranges)):
                if v1[y] in ranges[z]:
                    s1 = anchoring1[z]
                    idx_1 = z
                if v2[y] in ranges[z]:
                    s2 = anchoring2[z]   
                    idx_2 = z
            n = abs(idx_1-idx_2)
            if n == 0:
                mel_att.append(0.0)
            else:
                mel_att.append((s2/s1)/(n**2))

        if final_key[x-1][0].isupper():
            primary_key =  '/I'
        else:
            primary_key = '/i'    


        if final_key[x-1] != final_key[x]:
            
            # Tonicization of final_key[x]

            current_tonic = keys[key_idx[x-1]].tonic
            next_tonic = keys[key_idx[x]].tonic


            inter_dist = interval.Interval(noteStart=current_tonic, noteEnd=next_tonic)
            inter = inter_dist.name

            inter_quality = inter[0]
            inter_value = int(inter[-1])

            if str(next_tonic)[0].isupper():
                secondary_key = diatonic_functions[inter_value-1].upper()
            else:
                secondary_key = diatonic_functions[inter_value-1]        

            if inter_quality == 'm' or inter_quality == 'd':
                secondary_key = 'b'+secondary_key
            elif inter_quality == 'A':
                secondary_key = '#'+secondary_key

        else:
            if final_key[x][0].isupper():
                secondary_key = '/I'
            else:
                secondary_key = '/i'


            d = distance(final_key[x-1],
                         final_label[x-1].split('/')[0]+primary_key, 
                         final_label[x].split('/')[0] + secondary_key)[0]


        if d == 0:
            d = previous_d
        a = 10*sum(mel_att)/d
        harmonic_attraction.append(a)
        previous = final_notes[x]
        if d!=0:
            previous_d = d
            
    return harmonic_attraction