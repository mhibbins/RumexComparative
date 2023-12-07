import sys
from ete3 import Tree
import numpy as np
import copy
import csv

genetrees = []

with open(sys.argv[1], 'r') as genetree_file:
	for line in genetree_file:
		tree = Tree(line.strip())
		genetrees.append(tree)

def calc_delta(trees, P1, P2, P3):

	P1P2_counts, P1P3_counts, P2P3_counts = 0, 0, 0
	
	for tree in trees:
			
		leaf_names = [leaf.name for leaf in tree.iter_leaves()]		

		if P1 in leaf_names and P2 in leaf_names and P3 in leaf_names:

			P1P2_dist = tree.get_distance(P1, P2, topology_only = True)
			P1P3_dist = tree.get_distance(P1, P3, topology_only = True)
			P2P3_dist = tree.get_distance(P2, P3, topology_only = True)

			if P1P2_dist < P1P3_dist and P1P2_dist < P2P3_dist:
				P1P2_counts += 1
			elif P1P3_dist < P1P2_dist and P1P3_dist < P2P3_dist:
				P1P3_counts += 1
			elif P2P3_dist < P1P2_dist and P2P3_dist < P1P3_dist:
				P2P3_counts += 1
		else:
			continue

	if (P1P3_counts + P2P3_counts) == 0:
		delta = 0
	else:
		delta = (P1P3_counts - P2P3_counts) / (P1P3_counts + P2P3_counts)

	return delta, P1P2_counts, P1P3_counts, P2P3_counts

def delta_bootstrap(trees, P1, P2, P3, n_replicates):

	delta_estimates = []

	n_trees = len(trees)

	for i in range(n_replicates):
		bootstrapped_trees = np.random.choice(trees, len(trees))
		delta, P1P2_counts, P1P3_counts, P2P3_counts = calc_delta(bootstrapped_trees, P1, P2, P3)
		delta_estimates.append(delta)

	n_estimates = len(delta_estimates)

	mean_delta = sum(delta_estimates)/float(n_estimates)

	delta_stdev = ((sum([(x - mean_delta)**2 for x in delta_estimates]))/float(n_estimates-1))**(0.5)
	delta_se = delta_stdev/float(n_estimates)**(0.5)
	CI_lower = mean_delta - (1.96)*float(delta_stdev)
	CI_upper = mean_delta + (1.96)*float(delta_stdev)

	if mean_delta > 0:
		pval = sum(1 for i in delta_estimates if i <= 0)/float(n_estimates)
	elif mean_delta < 0:
		pval = sum(1 for i in delta_estimates if i >= 0)/float(n_estimates)

	delta, P1P2_counts, P1P3_counts, P2P3_counts = calc_delta(trees, P1, P2, P3)

	test = ",".join([P1, P2, P3])

	return [test, delta, P1P2_counts, P1P3_counts, P2P3_counts, delta_stdev, delta_se, CI_lower, CI_upper, pval]

all_delta_results = []

with open(sys.argv[2], 'r') as quartet_file:

	first = quartet_file.readline()
	quartet = first.strip().split("\t")
	P1, P2, P3 = quartet[0], quartet[1], quartet[2]
	delta_result = delta_bootstrap(genetrees, P1, P2, P3, 1000)
	print(*delta_result, sep = ",")
	






			

		
