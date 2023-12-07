# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

has_start_coords = {"X": [], "A1": [], "A2": [], "A4": []}
has_end_coords = {"X": [], "A1": [], "A2": [], "A4": []}

start = True
skip_hit = False
current_chr = ""
current_coords = []

with open("C:/Users/mhibb/OneDrive - University of Toronto/Projects/rumex_phylogeny/sexlinked_genes/roth_sexlinked/rothhemihap1out.txt", 
          'r') as roth_hap1_file:
    
    for line in roth_hap1_file:
        
        if line.startswith(">"):
            scaffold_name = line.strip().split(">")[1]
            if start == True:
                current_chr = scaffold_name
                start = False
            else:
                if scaffold_name in has_start_coords.keys():
                    has_start_coords[current_chr].append(current_coords[0])
                    has_end_coords[current_chr].append(current_coords[-1])
                    current_chr = scaffold_name
                    current_coords = []
                    skip_hit = False
                else:
                    skip_hit = True
        else:
            if skip_hit == True:
                continue
            else:
                splitline = line.strip().split()
            
                if len(splitline) > 0:
                    if splitline[0] == "Sbjct":
                        for element in splitline:
                            if element.isdigit():
                                current_coords.append(element)
                
X_length = 483481970
A1_length = 466657150
A2_length = 320470792
A4_length = 168693024

def divide_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

X_windows = list(divide_list(list(np.linspace(0, X_length, 50)), 2))
A1_windows = list(divide_list(list(np.linspace(0, A1_length, 50)), 2))
A2_windows = list(divide_list(list(np.linspace(0, A2_length, 50)), 2))
A4_windows = list(divide_list(list(np.linspace(0, A4_length, 50)), 2))

X_window_counts = [0]*25
A1_window_counts = [0]*25
A2_window_counts = [0]*25
A4_window_counts = [0]*25

for i in range(len(X_windows)):
    
    X_window = X_windows[i]
    for j in range(len(has_start_coords["X"])):
        
        X_lower = float(has_start_coords["X"][j])
        X_upper = float(has_end_coords["X"][j])
        
        if X_lower > X_window[0] and X_upper < X_window[1]:
            X_window_counts[i] += 1
    
    A1_window = A1_windows[i]
    for j in range(len(has_start_coords["A1"])):
        
        A1_lower = float(has_start_coords["A1"][j])
        A1_upper = float(has_end_coords["A1"][j])
        
        if A1_lower > A1_window[0] and A1_upper < A1_window[1]:
            A1_window_counts[i] += 1
            
    A2_window = A2_windows[i]
    for j in range(len(has_start_coords["A2"])):
        
        A2_lower = float(has_start_coords["A2"][j])
        A2_upper = float(has_end_coords["A2"][j])
        
        if A2_lower > A2_window[0] and A2_upper < A2_window[1]:
            A2_window_counts[i] += 1
            
    A4_window = A4_windows[i]
    for j in range(len(has_start_coords["A4"])):
        
        A4_lower = float(has_start_coords["A4"][j])
        A4_upper = float(has_end_coords["A4"][j])
        
        if A4_lower > A4_window[0] and A4_upper < A4_window[1]:
            A4_window_counts[i] += 1    
            
            
X_coords = [round(x[0]/1000000) for x in X_windows]
A1_coords = [round(x[0]/1000000) for x in A1_windows]
A2_coords = [round(x[0]/1000000) for x in A2_windows]
A4_coords = [round(x[0]/1000000) for x in A4_windows]

sns.set(font_scale = 0.7)
ax = sns.barplot(x = X_coords, y = X_window_counts)
ax.set(xlabel = "Position (Mb)", ylabel = "# of hits")
ax.set(ylim=(0, 40))
plt.show()