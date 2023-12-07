import sys
from ete3 import Tree
import itertools
import copy

rumex_sptree = Tree(sys.argv[1], format = 1)
rumex_relevant_spnames = []
rumex_exclude = ["F_tataricum"]

for leaf in rumex_sptree.iter_leaves():
	name = leaf.name
	if name not in rumex_exclude:
		rumex_relevant_spnames.append(name)

def get_triplet_topology(triplet):

	triplet_tree = copy.deepcopy(rumex_sptree)
	triplet_tree.prune(triplet, preserve_branch_length = True)
	pairs = itertools.combinations(triplet, 2)

	P1P2P3 = []

	for pair in pairs:
		dist = triplet_tree.get_distance(pair[0], pair[1], topology_only = True)
		if dist == 1:
			P1P2P3.append(pair[0])
			P1P2P3.append(pair[1])

	for leaf in triplet_tree.iter_leaves():
		if leaf.name not in P1P2P3:
			P1P2P3.append(leaf.name)

	return(P1P2P3)


triplets = itertools.combinations(rumex_relevant_spnames, 3)

for triplet in triplets:

	Dstat_triplet = get_triplet_topology(triplet)
	Dstat_triplet.append("F_tataricum")
	print("\t".join(map(str, Dstat_triplet)))

 
