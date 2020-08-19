

from functions.variables.chords_components import chords_parameters

def parameters_finder(file, auto_offsets):
    
    '''
    
    This function calculates the 'scale degree',
    'inversion' and 'non-harmonic' weightings of the
    events in the input piece of music 
    according to Lerdahl's model of tonal tension.
    '''
    
    # Extracting piece's data with music21
    
    (all_keys,
     all_labels,
     all_chords,
     all_inv,
     all_chords_nh,
     all_degrees,
     all_chord_notes,
     all_offsets,
     original_key,
     original_key_3,
     keys) = chords_parameters(file)

    # Deciding the final version of the parameters
    
    original_idx = -1
    counter = 0
    while original_idx == -1:
        if original_key == keys[counter]:
            original_idx = counter
        counter +=1    

    original_nh = all_chords_nh[original_idx]

    secondary_idx = []
    for x in range(len(original_nh)):
        if original_nh[x] > 0:
            secondary_idx.append(x)

    key_idx = []
    final_key = []
    final_label = []
    final_chord = []
    final_inv = []
    final_nh = []
    final_degree = []
    final_notes = []
    for x in range(len(original_nh)):   
        if x in secondary_idx:
            minimum_idx = original_nh[x]
            measure_idx = original_idx
            for y in range(len(all_chords)):
                if all_chords_nh[y][x] < minimum_idx:
                    minimim_idx = all_chords_nh[y][x]
                    measure_idx = y            

            if (all_chords_nh[measure_idx][x] 
                < all_chords_nh[original_idx][x]):    # secondary_chord         
                key_idx.append(measure_idx)
                final_key.append(all_keys[measure_idx])
                final_label.append(all_labels[measure_idx][x])
                final_chord.append(all_chords[measure_idx][x])
                final_inv.append(all_inv[measure_idx][x])
                final_nh.append(all_chords_nh[measure_idx][x])
                final_degree.append(all_degrees[measure_idx][x])                   
                final_notes.append(all_chord_notes[measure_idx][x])
            else:
                key_idx.append(original_idx)
                final_key.append(original_key_3)
                final_label.append(all_labels[original_idx][x])
                final_chord.append(all_chords[original_idx][x])
                final_inv.append(all_inv[original_idx][x])
                final_nh.append(all_chords_nh[original_idx][x])
                final_degree.append(all_degrees[original_idx][x])           
                final_notes.append(all_chord_notes[original_idx][x])

        else:
            key_idx.append(original_idx)
            final_key.append(original_key_3)
            final_label.append(all_labels[original_idx][x])
            final_chord.append(all_chords[original_idx][x])
            final_inv.append(all_inv[original_idx][x])
            final_nh.append(all_chords_nh[original_idx][x])
            final_degree.append(all_degrees[original_idx][x])      
            final_notes.append(all_chord_notes[original_idx][x])

    # Correct any offset mismatchings that might exist
    
    new_distribution = []
    previous = auto_offsets
    counter = 0
    for x in range(len(auto_offsets)-1):
        new_offset = []
        for y in range(len(all_offsets[0])):
            if (float(all_offsets[0][y]) >= float(auto_offsets[x])
               and float(all_offsets[0][y]) < float(auto_offsets[x+1])):
                new_offset.append(all_offsets[0][y])
                counter += 1
        new_distribution.append(new_offset)

    if new_distribution[-1][-1] != all_offsets[0][-1]:
        # there are extra offsets calculated by music21
        new_distribution.append(all_offsets[0][counter:])
        
    if not all(len(x)==1 for x in new_distribution):
        # there have been mismatchings
        mismat_idx = [len(x) for x in new_distribution]
        final_idx = []
        counter = 0
        for x in range(len(mismat_idx)):
            final_idx.append(counter)            
            if mismat_idx[x] != 1:    # mismatching!
                distances = []
                for y in range(len(new_distribution[x])):
                    distances.append(abs(float(auto_offsets[x])-new_distribution[x][y]))
                counter += 1+[y for y in range(len(distances)) 
                            if distances[y] ==  min(distances)][0]
            else:
                counter += 1
        final_key = [final_key[x] for x in range(len(all_offsets[0])) if x in final_idx]
        final_label = [final_label[x] for x in range(len(all_offsets[0])) if x in final_idx] 
        final_inv = [final_inv[x] for x in range(len(all_offsets[0])) if x in final_idx] 
        final_nh = [final_nh[x] for x in range(len(all_offsets[0])) if x in final_idx] 
        final_degree = [final_degree[x] for x in range(len(all_offsets[0])) if x in final_idx]   
        final_notes = [final_notes[x] for x in range(len(all_offsets[0])) if x in final_idx]   
    
    # Writing final surface parameters  
    
    surface_parameters = [['key', 
                         'chord function', 
                         'inversion', 
                         'chords non-harmonic', 
                         'melody non-harmonic', 
                         'scale degree']]

    for x in range(len(auto_offsets)):
        surface_parameters.append([final_key[x],
                                   final_label[x],
                                   final_inv[x],
                                   final_nh[x],
                                   0,
                                   final_degree[x]])
    # Writing intermediate parameters
    
    attraction_parameters = [final_notes,
                             final_key,
                             final_label,
                             keys,
                             key_idx]
    
    return surface_parameters, attraction_parameters