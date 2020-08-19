
import os
import pandas as pd
from functions.tps import distance
        
def distance_tests():
    
    # Reading ground-truths
    
    file = (os.path.join(os.getcwd(),
                         'tests',
                         'distance-test-cases.csv'))
    fields = ['key', 
              'original_chord', 
              'destination_chord', 
              'i', 
              'j', 
              'k', 
              'd'
             ]
    data = pd.read_csv(file, skipinitialspace=True, usecols=fields)
    original = data['original_chord']
    original = [" ".join(x.split()) for x  in original]
    destination = data['destination_chord']
    destination = [" ".join(x.split()) for x  in destination]
    keys = data['key']
    i = data['i']
    j = data['j']
    k = data['k']
    d = data['d']
    chord_pairs = [(original[x], destination[x]) for x in range(len(data))]

    # Test cases
    
    counter = 0
    for x in range(len(data)):
        print(x+1,'/',len(data), original[x], destination[x])
        calc_d, calc_i, calc_j, calc_k = distance(keys[x], original[x], destination[x])
        if(i[x] != calc_i 
           or j[x] != calc_j 
           or k[x]!= calc_k 
           or d[x] != calc_d):
            print('Transition:', original[x],'--->', destination[x], 'failed')
            print('i (ground-truth VS system)', i[x], 'VS', calc_i)
            print('j (ground-truth VS system)',j[x], 'VS', calc_j)
            print('k (ground-truth VS system)',k[x], 'VS', calc_k)
            print()
        else:
            counter += 1
    print()
    print('A total of ', counter, ' out of', len(data), 'cases passed the test.')