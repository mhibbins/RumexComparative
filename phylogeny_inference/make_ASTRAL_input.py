import sys
import os
from ete3 import Tree
import random

usable_orthogroups = []

with open(sys.argv[1], 'r') as orthogroups_file:
	for line in orthogroups_file:
		usable_orthogroups.append(line.strip())

usable_genetrees = []

def prune_orthogroup_genetree(orthogroup_file):

	genetree = Tree(orthogroup_file, format = 1)

	spleaves = {"R_salicifolius": [], "R_trisetifer": [], "R_amurensis": [],
                  "R_sagittatus": [], "R_scutatus": [], "R_rothschildianus": [],
                  "R_thyrsiflorus": [], "R_bucephalophorus": [], "R_acetosella": [],
                  "R_hastatulus": [], "R_paucifolius": [], "F_tataricum": []}

	for leaf in genetree.iter_leaves():

		if "FtPin" in leaf.name:
			leafspecies = "F_tataricum"
			spleaves[leafspecies].append(leaf.name)
		else:
			leafname = leaf.name.split("_")
			leafspecies = "_".join([leafname[0], leafname[1]])
			spleaves[leafspecies].append(leaf.name)

	leaves_toprune = []

	for val in spleaves.values():
		if len(val) == 1:
			leaves_toprune.append(val[0])
		elif len(val) >= 2:
			prune_copy = random.choice(val)
			leaves_toprune.append(prune_copy)		
			
	genetree.prune(leaves_toprune, preserve_branch_length = True)
	
	for leaf in genetree.iter_leaves():

		if "FtPin" in leaf.name:
			leaf.name = "F_tataricum"
		else:
			leafsplit = leaf.name.split("_")
			leafspecies = "_".join([leafsplit[0], leafsplit[1]])
			leaf.name = leafspecies

	try:
		genetree.set_outgroup("F_tataricum")
	except:
		pass

	return(genetree.write())			
		
#
#		genetree = Tree(orthofile)
#		print(genetree)


		#Add sequences for species with a copy
		
				

file_counter = 0

for filename in os.listdir(sys.argv[2]):

	file_orthogroup = filename.split("_")[0]

	if file_orthogroup in usable_orthogroups:
		orthogroup_file = os.path.join(sys.argv[2], filename)
		usable_genetrees.append(prune_orthogroup_genetree(orthogroup_file))
		file_counter +=1
		if file_counter%100 == 0:
			print("Finished parsing file " + str(file_counter) + " out of " + str(len(usable_orthogroups)))

with open("rumex_ASTRAL_genetrees_buckwheat.txt", 'w') as f:

	for tree in usable_genetrees:
		f.write(tree + "\n")

	


