# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:00:48 2023

@author: Mark
"""

import statsmodels.stats.multitest as smm
import csv
import re 

raw_result_lines = []

with open("C:/Users/18126/OneDrive - University of Toronto/Projects/rumex_phylogeny/introgression/rumex_buckwheat_deltastats_results.txt", "r") as raw_results:
    for line in raw_results:
        raw_result_lines.append(line.strip().split(","))
        
raw_pvals = []

for i in range(len(raw_result_lines)):
    pval = raw_result_lines[i][-1]
    
    if pval == 0:
        pval = 0.001
        
    raw_pvals.append(float(pval))
    
tests, corrected_pvals = smm.fdrcorrection(raw_pvals)

results = []

def is_meaningful(line):
    conc, disc1, disc2 = float(line[4]), float(line[5]), float(line[6])
    
    if (disc1+disc2)/conc < 0.05:
        return False
    else:
        return True

for i in range(len(corrected_pvals)):
        if corrected_pvals[i] < 0.05 and is_meaningful(raw_result_lines[i]):
            total_results = raw_result_lines[i]
            total_results.append(corrected_pvals[i])
            results.append(total_results)
            
with open("C:/Users/18126/OneDrive - University of Toronto/Projects/rumex_phylogeny/introgression/rumex_buckwheat_deltastats_parsed_results.txt", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(results)

        