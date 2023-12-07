import sys
from ete3 import Tree 
trees = []

with open(sys.argv[1], 'r') as treesfile:

	for line in treesfile:
		if line.startswith("("):

			tree = Tree(line)
			tree.convert_to_ultrametric()
			species_to_keep = []
			
			for leaf in tree.iter_leaves():
				species_to_keep.append(leaf.name)

			tree.prune(species_to_keep, preserve_branch_length = True)

			try:
				tree.set_outgroup("F_tataricum")
			except:
				continue


			trees.append(tree.write())

with open(sys.argv[2], 'w+') as nex_file:

	genetree_string = []

	nex_file.write("#NEXUS\n")
	nex_file.write("\n")
	nex_file.write("BEGIN TREES;\n")
	nex_file.write("\n")
		
	for i in range(len(trees)):
		nex_file.write("Tree geneTree" + str(i) + " = " + trees[i] + "\n")
		genetree_string.append("geneTree" + str(i))

	genetree_string = ','.join(genetree_string)

	nex_file.write("\n")
	nex_file.write("END;\n")
	nex_file.write("\n")
	nex_file.write("\n")
	nex_file.write("BEGIN PHYLONET;\n")
	nex_file.write("\n")
	nex_file.write("InferNetwork_MPL (" + genetree_string + ") 6 -pl 60 -di;\n")
	nex_file.write("\n")
	nex_file.write("END;")
