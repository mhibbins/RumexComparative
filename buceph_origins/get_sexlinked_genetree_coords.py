import sys
from ete3 import Tree
import random
import copy

trees = []
Xlinked_coords = {}

with open(sys.argv[1], 'r') as treefile:
	for line in treefile:
		trees.append(Tree(line))

with open(sys.argv[2], 'r') as gff_file:
	
	for line in gff_file:
		splitline = line.strip().split("\t")

		if splitline[0] == "X" and splitline[2] == "CDS":

			lower_coord = float(splitline[3])
			upper_coord = float(splitline[4])

			if lower_coord > 71*1000000 and upper_coord < 261*1000000:
				gene_ID = splitline[-1]

				Xlinked_coords[gene_ID] = [lower_coord, upper_coord]

def get_tree_topology(genetree):

	genetree_copy = copy.deepcopy(genetree)
	
	spleaves = {"R_hastatulus_NC_X": [],
		    "R_hastatulus_NC_Y": [], "R_bucephalophorus": [],
		    "R_amurensis": [], "R_trisetifer": [],
		    "R_salicifolius": []}

	for leaf in genetree_copy.iter_leaves():

		leafname = leaf.name

		if "RBuc" in leafname:

			spleaves["R_bucephalophorus"].append(leafname)

		elif "NChap1" in leafname and "RBuc" not in leafname:

			spleaves["R_hastatulus_NC_X"].append(leafname)

			leafkey = leafname.split("-")[0]

			for key in Xlinked_coords.keys():
				if leafkey in key:
					genetree_coords = Xlinked_coords[key]

		elif "NChap2" in leafname and "RBuc" not in leafname:

			spleaves["R_hastatulus_NC_Y"].append(leafname)

		elif "R_amurensis" in leafname:
			
			spleaves["R_amurensis"].append(leafname)

		elif "R_trisetifer" in leafname:
			
			spleaves["R_trisetifer"].append(leafname)

		elif "R_salicifolius" in leafname:
	
			spleaves["R_salicifolius"].append(leafname)

	outgroup_leaves = []
	leaves_toprune = []

	for leaf in genetree_copy.iter_leaves():
		leafname = leaf.name

		if "R_amurensis" in leafname or "R_trisetifer" in leafname or "R_salicifolius" in leafname:
			outgroup_leaves.append(leafname)

	rootsp = random.sample(outgroup_leaves, 1)[0]
	leaves_toprune.append(rootsp)

	outgroups_combined = '\t'.join(outgroup_leaves)

	for key, val in spleaves.items():
	
		if key in outgroups_combined:
			pass
		else:
			if len(val) == 1:
				leaves_toprune.append(val[0])
			elif len(val) >= 2:
				prune_copy = random.choice(val)
				leaves_toprune.append(prune_copy)

	genetree_copy.prune(leaves_toprune, preserve_branch_length = True)

	genetree_copy.set_outgroup(rootsp)

	for leaf in genetree_copy.iter_leaves():
		
		leafname = leaf.name

		if "RBuc" in leafname:
			leaf.name = "R_bucephalophorus"
		elif "NChap1" in leafname and "RBuc" not in leafname:
			leaf.name = "R_hastatulus_NC_X"
		elif "NChap2" in leafname and "RBuc" not in leafname:
			leaf.name = "R_hastatulus_NC_Y"
		elif "R_amurensis" in leafname:
			leaf.name = "R_amurensis"
		elif "R_trisetifer" in leafname:
			leaf.name = "R_trisetifer"
		elif "R_salicifolius" in leafname:
			leaf.name = "R_salicifolius"

	hasXY_dist = genetree_copy.get_distance("R_hastatulus_NC_X", "R_hastatulus_NC_Y", topology_only = True)
	bucX_dist = genetree_copy.get_distance("R_bucephalophorus", "R_hastatulus_NC_X", topology_only = True)
	bucY_dist = genetree_copy.get_distance("R_bucephalophorus", "R_hastatulus_NC_Y", topology_only = True)
	

	if hasXY_dist < bucX_dist and hasXY_dist < bucY_dist:
		topology = "hasXY"
	elif bucX_dist < hasXY_dist and bucX_dist < bucY_dist:
		topology = "bucX"
	elif bucY_dist < bucX_dist and bucY_dist < hasXY_dist:
		topology = "bucY"

	return topology, genetree_coords

for tree in trees:
	
	topology, coords = get_tree_topology(tree)
	print(topology, coords[0], coords[1])

		
