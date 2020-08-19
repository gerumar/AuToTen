import os
import csv
from functions.tension import t_calculator

def tension_tests():
    
    # Reading parameters data
    
    prolongational_matrix = 'wagner_prolongational_matrix.csv'
    piece_data = 'wagner_piece_data.csv'
    
    # Calculating tension
    
    tension = t_calculator(os.path.join(os.getcwd(),
                                        'tests',
                                        piece_data), 
                           os.path.join(os.getcwd(),
                                        'tests',
                                        prolongational_matrix))
    
    # Input ground-truth
    
    tension_data = 'wagner_tension_data.csv'
    with open(os.path.join(os.getcwd(),'tests',tension_data)) as csv_file:
        csv_reader = csv.reader(csv_file)
        wagner_ground_truth = [row for row in csv_reader][0]
    wagner_ground_truth = [int(x) for x in wagner_ground_truth]

    # Test cases
    
    counter = 0
    for x in range(len(tension)):
        if tension[x] != wagner_ground_truth[x]:
            print('Event', x+1, 'failed', tension[x], wagner_ground_truth[x])
        else:
            counter +=1
    print('A total of ', counter, ' out of ', len(tension), 'cases passed Wagner test.')        
    print()

    # Reading parameters data
    
    prolongational_matrix = 'bach_prolongational_matrix.csv'
    piece_data = 'bach_piece_data.csv'
    
    # Calculating tension
        
    tension = t_calculator(os.path.join(os.getcwd(),
                                        'tests',
                                        piece_data), 
                           os.path.join(os.getcwd(),
                                        'tests',
                                        prolongational_matrix))    
    
    # Input ground-truth
    
    tension_data = 'bach_tension_data.csv'
    with open(os.path.join(os.getcwd(),'tests',tension_data)) as csv_file:
        csv_reader = csv.reader(csv_file)
        bach_ground_truth = [row for row in csv_reader][0]
    bach_ground_truth = [int(x) for x in bach_ground_truth]
    
    # Test cases
    
    counter = 0
    for x in range(len(tension)):
        if tension[x] != bach_ground_truth[x]:
            print('Event', x+1, 'failed', tension[x], bach_ground_truth[x])
        else:
            counter +=1
    print('A total of ', counter, ' out of ', len(tension), 'cases passed Bach test.')