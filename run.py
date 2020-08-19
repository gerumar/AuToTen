import os
import csv

import tkinter as tk
from tkinter import filedialog

from setup import *


# Input the piece of music

input('Select a piece of music, in XML format.')
print()

root = tk.Tk()
root.withdraw()

piece_path = filedialog.askopenfilename()
file_name = piece_path.split('/')[-1].split('.')[0]

# Input the piece's prolongational reduction

input('Select the piece\'s prolongational reduction file, in XML format.')
print()

pr_path = filedialog.askopenfilename()

# Input the piece's metrical reduction

input('Select the piece\'s metrical reduction file, in XML format.')
print()

mr_path = filedialog.askopenfilename()

# Calculating the piece's prolongational matrix

prolongational_matrix = generator(pr_path)

# Calculating the piece's offsets 

auto_offsets = offset(mr_path)

# Calculating the piece's surface parameters

(surface_parameters,
 attraction_parameters) = parameters_finder(piece_path,
                                             auto_offsets)

# Calculating the piece's values of global tension

global_tension = t_calculator(surface_parameters,
                       prolongational_matrix)

# Calculating the piece's values of attraction

harmonic_attraction = a_calculator(attraction_parameters)

# Input the output directory

input('Please select where you want to store the output data.')
print()

output_dir = filedialog.askdirectory()

# Writing output files

with open(os.path.join(output_dir, 
                       file_name
                       +'-auto-matrix.csv'), 
          'w') as f1, open(os.path.join(output_dir, 
                                        file_name
                                        +'-auto-offsets.csv'), 
                           'w') as f2, open(os.path.join(output_dir, 
                                                         file_name
                                                         +'-auto-piece-data.csv'), 
                                            'w') as f3, open(os.path.join(output_dir, 
                                                                          file_name
                                                                          +'-auto-tension.csv'), 
                                                             'w') as f4, open(os.path.join(output_dir, 
                                                                                         file_name
                                                                                         +'-auto-attraction.csv'), 
                                                                            'w') as f5:

    writer1 = csv.writer(f1)
    writer2 = csv.writer(f2)
    writer3 = csv.writer(f3)
    writer4 = csv.writer(f4)
    writer5 = csv.writer(f5)
        
    writer1.writerows(prolongational_matrix)
    writer2.writerow(auto_offsets) 
    writer3.writerows(surface_parameters) 
    writer4.writerow(global_tension) 
    writer5.writerow(harmonic_attraction) 
    

