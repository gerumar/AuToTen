
from functions.parameters.common import *
from functions.classes.parser import Scale

class Notes(Scale):
    
    def __init__(self, current_key, chord):
        super().__init__(current_key, chord)    
    
    # Local function is non-harmonic (#)
    def fun_has_sharp(self):
        if self.local_function.startswith('#'):
            return True
        return False
    
    # Local function is non-harmonic (b)
    def fun_has_flat(self):
        if self.local_function.startswith('b'):
            return True
        return False

    # Calculating the root of local function
    def root_idx(self):
        natural_function = self.natural_function()
        return [x for x in range(len(diatonic_functions)) 
                if natural_function in diatonic_functions[x]][0]
    
    def chromatic_root_idx(self):
        root = self.root()
        return [x for x in range(len(chromatic_scale)) 
                if root in chromatic_scale[x]][0]
    
    def root(self):
        local_function = self.local_function
        if local_function.startswith('#'):
            return self.sharppen(self.local_sorted_scale()[self.root_idx()])
        elif local_function.startswith('b'):
            return self.flatten(self.local_sorted_scale()[self.root_idx()])         
        elif local_function.startswith('n'):
            return self.local_sorted_scale()[self.root_idx()][:-1]
        return self.local_sorted_scale()[self.root_idx()]

    # Calculating the third of local function
    def diatonic_third_idx(self):
        return (self.root_idx() + 2) % 7
    
    def chromatic_third_idx(self):
        local_sorted_scale = self.local_sorted_scale()
        return [x for x in range(len(chromatic_scale)) 
                if local_sorted_scale[self.diatonic_third_idx()] 
                in chromatic_scale[x]][0]
    
    def interval_to_root(self):
        return abs(self.chromatic_root_idx() 
                   - self.chromatic_third_idx())   
    
    def third(self):  
        interval = self.interval_to_root()
        if interval not in (2,3,4,5):
            interval = (-1*interval) % 12
        if self.natural_function().isupper():       
            if interval == 5:
                return self.flatten(self.local_sorted_scale()[self.diatonic_third_idx()])              
            elif interval == 4:
                # Major third
                return self.local_sorted_scale()[self.diatonic_third_idx()]
            elif interval == 3:
                return self.sharppen(self.local_sorted_scale()[self.diatonic_third_idx()]) 
            elif interval == 2:
                return (self.sharppen(
                    self.sharppen(self.local_sorted_scale()[self.diatonic_third_idx()])))          
        else:
            if interval == 2:
                return self.sharppen(self.local_sorted_scale()[self.diatonic_third_idx()])                        
            elif interval == 3:
                # Minor third
                return self.local_sorted_scale()[self.diatonic_third_idx()]
            elif interval == 4:
                return self.flatten(self.local_sorted_scale()[self.diatonic_third_idx()])  
            elif interval == 5:
                return(self.flatten(
                    self.flatten(self.local_sorted_scale()[self.diatonic_third_idx()]))
                )
    # Calculating the fifth of local function
    def diatonic_fifth_idx(self):
        return (self.root_idx() + 4) % 7
    
    def chromatic_fifth_idx(self):
        return (self.chromatic_root_idx() + 7) % 12

    def fifth(self):
        chromatic_pair = chromatic_scale[self.chromatic_fifth_idx()]
        if self.local_alpha_sharp():
            if( chromatic_pair[1] 
               in order_of_sharps[:self.local_alterations()]
              ):
                diatonic_fifth = chromatic_pair[1]
            else:
                diatonic_fifth = chromatic_pair[0]
        else:
            if( chromatic_pair[1]
               in order_of_flats[:self.local_alterations()]
              ):
                diatonic_fifth = chromatic_pair[1]
            else:
                diatonic_fifth = chromatic_pair[0]
        local_function = self.local_function
        if '+' in local_function:
            return self.sharppen(diatonic_fifth) 
        elif '-' in local_function:
            return self.flatten(diatonic_fifth) 
        return diatonic_fifth

    # Calculating the seventh of local function, if any
    def diatonic_seventh_idx(self):
        return (self.root_idx() + 6) % 7
    
    def chromatic_seventh_idx(self):
        local_sorted_scale = self.local_sorted_scale()
        diatonic_seventh_idx = self.diatonic_seventh_idx()
        return [x for x in range(len(chromatic_scale)) 
                if local_sorted_scale[diatonic_seventh_idx] 
                in chromatic_scale[x]][0]
    
    def seventh(self):
        if '7' in self.local_function:
            return self.local_sorted_scale()[self.diatonic_seventh_idx()]
        return None