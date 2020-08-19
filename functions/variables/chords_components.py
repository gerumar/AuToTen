

from music21 import *

from functions.parameters.common import *
from functions.classes.notes import Notes
from functions.classes.parser import Scale


def chords_parameters(file):
     
    # Key finder algorithm
    
    file_conv = converter.parse(file)
    chords_labels = file_conv.chordify()
    
    original_key = file_conv.analyze('key')
    
    original_key_2 = (str(original_key)
                      .split('minor')[0]
                      .split('major')[0][:-1])
    if original_key_2[-1] == '-':
        original_key_3 = original_key_2[:-1]+'b'
    elif original_key_2[-1] == '+':
        original_key_3 = original_key_2[:-1]+'#'
    else:
        original_key_3 = original_key_2

    keys = []
    for m in chords_labels.getElementsByClass('Measure'):
        k = m.analyze('key')
        keys.append(k)
    
    # Chords parameter calculation
    
    possible_roman = ['I', 'i', 'V', 'v']
    
    all_keys = []
    all_chords = []
    all_offsets = []
    all_inversions = []
    all_qualities = []
    all_sevenths = []
    all_nonharm = []
    all_notes = []

    all_inv = []
    all_chords_nh = []
    all_degrees = []
    all_chord_notes = []
    all_labels = []
    for k in keys:
        chords_labels = file_conv.chordify()
        for c in chords_labels.recurse().getElementsByClass('Chord'):
            rn = roman.romanNumeralFromChord(c, k)
            c.addLyric(str(rn.figure))

        k2 = str(k).split('minor')[0].split('major')[0][:-1]
        if k2[-1] == '-':
            k3 = k2[:-1]+'b'
        elif k2[-1] == '+':
            k3 = k2[:-1]+'#'
        else:
            k3 = k2
        all_keys.append(k3)

        chords = []
        offsets = []
        inversions = []
        qualities = []
        sevenths = []
        nonharm = []
        notes = []
        for c in chords_labels.flat:
            if 'Chord' not in c.classes:
                continue
            sc = scale.MajorScale(k2)
            chords.append(c.lyric)
            offsets.append(c.offset)
            inversions.append(c.inversion())
            qualities.append(c.quality)
            sevenths.append(c.seventh)
            nonharm.append([sc.getScaleDegreeFromPitch(x) 
                            for x in c.pitches])
            notes.append([str(x) 
                          for x in c.pitches])        
        all_chords.append(chords)
        all_offsets.append(offsets)
        all_inversions.append(inversions)
        all_qualities.append(qualities)
        all_sevenths.append(sevenths)
        all_nonharm.append(nonharm)
        all_notes.append(notes)
        
        # Calculating MTT's inversion
        inv = []
        for x in inversions:
            if x == 2 or x == 1:
                inv.append(2)
            else:
                inv.append(0)    
        all_inv.append(inv)

        # Calculating chords Roman labels
        roman_label = []
        if k3[0].isupper():
            of_key = '/I'
        else:
            of_key = '/i'
        for x in range(len(chords)):
            c = ''
            for y in chords[x]:
                if y in possible_roman:
                    c += y                   
                    
            # Correct any possible quality-related mismatching
            
            if qualities[x] == 'other':
                if k3[0].isupper() and c not in major_functions:
                    if c.isupper():
                        c = c.lower()
                    else:
                        c = c.upper()
                if k3[0].islower() and c not in minor_functions:
                    if c.isupper():
                        c = c.lower()
                    else:
                        c = c.upper()
                               
            if 'o' in chords[x]:
                c = c+'-'
            if sevenths[x]:
                c = c+'7'       
            roman_label.append(c+of_key)
            
        # Calculating MTT's non-harmonic and scale degrees
        
        all_labels.append(roman_label)
        chords_nh = []
        degrees = []
        chord_notes = []
        for x in range(len(notes)):
            deg = []
            nh = []
            root = Notes(k3, roman_label[x]).root()
            third = Notes(k3, roman_label[x]).third()
            fifth = Notes(k3, roman_label[x]).fifth()
            seventh = Notes(k3, roman_label[x]).seventh()
            current_scale = Scale(k3, roman_label[x]).local_sorted_scale()
            ns = []
            for y in range(len(notes[x])):
                n = notes[x][y].lower()[:-1]
                if '-' in n:
                    note = n[:-1]+'b'
                elif '+' in n:
                    note = n[:-1]+'#'
                else:
                    note = n
                ns.append(note+notes[x][y][-1])
                if note not in current_scale:
                    nh.append(4)
                    deg.append(0)
                elif note == root:
                    nh.append(0)
                    deg.append(0)
                elif note == third or note == fifth:
                    nh.append(0)
                    deg.append(1)
                elif note == seventh:
                    if '7' not in roman_label[x]:
                        nh.append(1)
                        deg.append(0)
                    else:
                        nh.append(0)
                        deg.append(0)                
                else:
                    nh.append(3)
                    deg.append(0)
            chords_nh.append(sum(nh))
            degrees.append(deg[-1])
            chord_notes.append(ns)

        all_chords_nh.append(chords_nh)
        all_degrees.append(degrees)
        all_chord_notes.append(chord_notes)
                        
    return (all_keys,
            all_labels,
            all_chords,
            all_inv,
            all_chords_nh,
            all_degrees,
            all_chord_notes,
            all_offsets,
            original_key,
            original_key_3,
            keys)
