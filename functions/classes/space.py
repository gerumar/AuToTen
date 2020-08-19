
from functions.parameters.common import *
from functions.classes.notes import Notes

class Space(Notes):
    
    def __init__(self, current_key, chord):
        super().__init__(current_key, chord) 
    
    # Number of moves made to sort the diatonic scale
    def sorting_shift_idx(self):
        return self.local_diatonic_scale().index(self.local_sorted_scale()[0])

    # Rewriting the diatonic space based on the chordal data
    def sorted_chordal_space(self):
        space = self.local_sorted_scale()
        space[self.root_idx()] = self.root()
        space[self.diatonic_third_idx()] = self.third()
        space[self.diatonic_fifth_idx()] = self.fifth()
        return space

    # Chordal space starting at c
    def chordal_space(self):
        sorted_chordal_space = self.sorted_chordal_space()
        shift_index = (-1*self.sorting_shift_idx()) % 7
        return (sorted_chordal_space[shift_index:] 
                + sorted_chordal_space[:shift_index])

    # Basic space just at TPS' level (d)
    def level_d(self):
        local_diatonic_scale = self.local_diatonic_scale()
        return [2 if any(y in local_diatonic_scale
                       for y in chromatic_scale[x]) 
                else 1 for x in range(len(chromatic_scale))]

    # TPS' basic space
    def basic_space(self):
        chordal_space = self.chordal_space()
        root = self.root()
        if root in enharmonics:
            root = enharmonics[root]
        third = self.third()
        if third in enharmonics:
            third = enharmonics[third]
        fifth = self.fifth()
        if fifth in enharmonics:
            fifth = enharmonics[fifth]
        seventh = self.seventh()
        if seventh in enharmonics:
            seventh = enharmonics[seventh]
        space = [2 if any(y in chordal_space
                       for y in chromatic_scale[x]) 
                else 1 for x in range(len(chromatic_scale))]
        space[[x for x in range(len(chromatic_scale)) 
                if root in chromatic_scale[x]][0]] = 5
        space[[x for x in range(len(chromatic_scale)) 
                if third in chromatic_scale[x]][0]] = 3        
        space[[x for x in range(len(chromatic_scale)) 
                if fifth in chromatic_scale[x]][0]] = 4
        if seventh:
            space[[x for x in range(len(chromatic_scale)) 
                if seventh in chromatic_scale[x]][0]] = 3
        return space