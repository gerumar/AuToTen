
import os
import pandas as pd

class Harmony:
    
    def __init__(self, filename):
        self.file = filename
        
    def harmonic_data(self):
        if isinstance(self.file, str):
            return pd.read_csv(self.file) 
        else:
            return pd.DataFrame(self.file[1:], 
                                columns=['key',
                                         'chord function',
                                         'inversion',
                                         'chords non-harmonic',
                                         'melody non-harmonic',
                                         'scale degree'])
    
    def current_key(self):
        harmonic_data = self.harmonic_data()        
        return harmonic_data['key']
    
    def chord_functions(self):
        harmonic_data = self.harmonic_data()
        return list(harmonic_data['chord function'])
    
    def inversion_degrees(self):
        harmonic_data = self.harmonic_data()
        return list(harmonic_data['inversion'])
    
    def dissonance_degrees(self):
        harmonic_data = self.harmonic_data()
        return [sum(x) 
                for x in zip(list(harmonic_data['chords non-harmonic']), 
                             list(harmonic_data['melody non-harmonic']))]
    def scale_degrees(self):
        harmonic_data = self.harmonic_data()
        return list(harmonic_data['scale degree'])        