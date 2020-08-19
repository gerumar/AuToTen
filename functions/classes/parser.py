
from functions.parameters.common import *

class Key:
    
    def __init__(self, current_key, chord):
        self.global_key = current_key
        self.local_function, self.local_key = chord.split('/')  
    
    # Is the global key in the ascending circle-of-fifths?
    def global_has_sharp(self):
        if self.global_key in list(sum(sharp_keys, ())):
            return True
        return False
    
    # Is the local key in the ascending circle-of-fifths?    
    def local_has_sharp(self):
        if self.local_key in list(sum(sharp_functions, ())):
            return True
        return False

    # Is the local key a major key?
    def local_is_major(self):
        if self.local_key[-1].isupper():
            return True
        return False

    # Local key without alterations
    def natural_key(self):
        local_key = self.local_key
        if(local_key.startswith('#') 
           or local_key.startswith('b')):
            return local_key[1:]
        return local_key

    # Local function without alterations
    def natural_function(self):
        local_function = self.local_function
        if(local_function.startswith('#') 
           or local_function.startswith('b')
           or local_function.startswith('n')):
            return local_function[1:].split('7')[0].split('+')[0].split('-')[0]
        return local_function.split('7')[0].split('+')[0].split('-')[0]

    # Number of alterations in the global key signature
    def global_alterations(self):
        global_key = self.global_key
        if self.global_has_sharp():
            return [x for x in range(len(sharp_keys)) 
                    if global_key in sharp_keys[x]][0]
        return [x for x in range(len(flat_keys)) 
                if global_key in flat_keys[x]][0]  
    
class Scale(Key):
    
    def __init__(self, current_key, chord):
        super().__init__(current_key, chord)

    # Diatonic scale of the global key starting at c
    def global_diatonic_scale(self):
        global_has_sharp = self.global_has_sharp()
        scale = [x for x in diatonic_notes]
        for num_alteration in range(self.global_alterations()):
            if global_has_sharp:
                to_be_altered = scale.index(order_of_sharps[num_alteration][:-1])
                scale[to_be_altered] = order_of_sharps[num_alteration]
            else:
                to_be_altered = scale.index(order_of_flats[num_alteration][:-1])
                scale[to_be_altered] = order_of_flats[num_alteration]
        return scale

    # Diatonic scale of global key starting at its tonal centre
    def global_sorted_scale(self):
        global_diatonic_scale = self.global_diatonic_scale()
        tonal_centre = global_diatonic_scale.index(self.global_key.lower())      
        return (global_diatonic_scale[tonal_centre:] 
                + global_diatonic_scale[:tonal_centre]) 
    
    # Adding sharps
    @staticmethod
    def sharppen(note):
        if note.endswith('b') and len(note) > 1:
            note = note[:-1]
        else:
            note = note + '#'
        if '###' in note:
            raise ValueError('note {} is not supported'.format(note))
        return note

    # Adding flats
    @staticmethod
    def flatten(note):
        if note.endswith('#'):
            note = note[:-1]
        else:
            note = note + 'b'
        if 'bbb' in note and note != 'bbb':
            raise ValueError('note {} is not supported'.format(note))    
        return note

    # Local key alphabetic name, with regards to global key
    def alphabet_key(self):
        natural_key = self.natural_key()
        tonal_centre_idx = [x for x in range(len(diatonic_functions))
                           if natural_key in diatonic_functions[x]][0]
        tonal_centre = self.global_sorted_scale()[tonal_centre_idx]
        local_key = self.local_key
        if local_key.startswith('#'): 
            tonal_centre = self.sharppen(tonal_centre)
        elif local_key.startswith('b'): 
            tonal_centre = self.flatten(tonal_centre)      
        alpha_key = tonal_centre   
        local_is_major = self.local_is_major()
        if local_is_major:
            alpha_key = tonal_centre[0].upper()+tonal_centre[1:]
        if(alpha_key not in list(sum(sharp_keys, ())) 
           and alpha_key not in list(sum(flat_keys, ()))):
            tonal_centre = enharmonics[tonal_centre]
            if local_is_major():
                alpha_key = tonal_centre[0].upper()+tonal_centre[1:]
        if alpha_key in enharmonic_keys:
            return enharmonic_keys[alpha_key]
        return alpha_key      

    # Is the local key in the ascending circle-of-fifths?
    def local_alpha_sharp(self):
        if self.alphabet_key() in list(sum(sharp_keys, ())):
            return True
        return False        
    
    # Number of alterations in the local key signature
    def local_alterations(self):
        alphabet_key = self.alphabet_key()
        if self.local_alpha_sharp():
            return [x for x in range(len(sharp_keys)) 
                    if alphabet_key in sharp_keys[x]][0]
        return [x for x in range(len(flat_keys)) 
                if alphabet_key in flat_keys[x]][0]  
    
    # Diatonic scale of the local key starting at c    
    def local_diatonic_scale(self):
        local_alpha_sharp = self.local_alpha_sharp()
        scale = [x for x in diatonic_notes]
        for num_alteration in range(self.local_alterations()):
            if local_alpha_sharp:
                to_be_altered = scale.index(order_of_sharps[num_alteration][:-1])
                scale[to_be_altered] = order_of_sharps[num_alteration]
            else:
                to_be_altered = scale.index(order_of_flats[num_alteration][:-1])
                scale[to_be_altered] = order_of_flats[num_alteration]
        return scale
    
    # Diatonic scale of local key starting at its tonal centre    
    def local_sorted_scale(self):
        local_diatonic_scale = self.local_diatonic_scale()
        tonal_centre = local_diatonic_scale.index(self.alphabet_key().lower())      
        return (local_diatonic_scale[tonal_centre:] 
                + local_diatonic_scale[:tonal_centre])  