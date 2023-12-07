import sys
import os
from Bio import SeqIO
from Bio.Seq import Seq

file_counter = 0

for file in os.listdir(sys.argv[1]):

	if file.endswith(".fa"):
		fasta_file = os.path.join(sys.argv[1], file)

	aa_dict = {}

	for record in SeqIO.parse(fasta_file, 'fasta'):

		dna_seq = record.seq
		protein_seq = dna_seq.translate()
		aa_dict[record.id] = str(protein_seq)

	orthogroup_name = file.split(".")[0]
	newfile = orthogroup_name + "_aa.fa"
	new_aa_file = os.path.join(sys.argv[2], newfile)

	with open(new_aa_file, 'w') as aa_file:
		for key, val in aa_dict.items():
			aa_file.write(key + "\n")
			aa_file.write(val + "\n")

	file_counter += 1

	if file_counter%1000 == 0:
		print("Finished parsing file " + str(file_counter) + " out of " + str(141888))

		
