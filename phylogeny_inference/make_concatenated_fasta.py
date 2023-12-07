import sys
import os
import re

usable_orthogroups = []
seqname_dict = {}

with open(sys.argv[1], 'r') as orthogroups_file:
	for line in orthogroups_file:
		usable_orthogroups.append(line.strip())


sequences_dict = {">R_salicifolius": "", ">R_trisetifer": "", ">R_amurensis": "",
                  ">R_sagittatus": "", ">R_scutatus": "", ">R_rothschildianus": "",
		  ">R_thyrsiflorus": "", ">R_bucephalophorus": "", ">R_acetosella": "",
		  ">R_hastatulus": "", ">R_paucifolius": "", ">F_tataricum": ""}

def get_orthogroup_alignment_length(ortho_dict):
	
	for key, val in ortho_dict.items():
		if len(val) > 0:
			return(len(val))

def parse_orthogroup_fasta(orthogroup_file):

	with open(orthogroup_file, 'r') as orthofile:
		
		current_sp = ""
		parsed_sp = []
		skipping_duplicate = False
		current_sequences = {">R_salicifolius": "", ">R_trisetifer": "", ">R_amurensis": "",
                  ">R_sagittatus": "", ">R_scutatus": "", ">R_rothschildianus": "",
                  ">R_thyrsiflorus": "", ">R_bucephalophorus": "", ">R_acetosella": "",
                  ">R_hastatulus": "", ">R_paucifolius": "", ">F_tataricum": ""}


		#Add sequences for species with a copy
		for line in orthofile:
			if line.strip():
				if line.startswith(">"):

					if "FtPin" in line:
						sp_name = ">F_tataricum"
					else:
						sp_name = line.strip().split("_")
						sp_name = "_".join([sp_name[0], sp_name[1]])

					if sp_name not in parsed_sp:
						current_sp = sp_name
						parsed_sp.append(sp_name)
						skipping_duplicate = False
					elif sp_name in parsed_sp:
						skipping_duplicate = True
					
				else:
					if skipping_duplicate == False:
						sequences_dict[current_sp] = sequences_dict[current_sp] + line.strip()
						current_sequences[current_sp] = current_sequences[current_sp] + line.strip()
					elif skipping_duplicate == True:
						next	

		#Add in gaps for missing species
		sequence_length = get_orthogroup_alignment_length(current_sequences)

		for key in sequences_dict.keys():
			if len(current_sequences[key]) == 0:
				gaps = "-"*sequence_length
				sequences_dict[key] = sequences_dict[key] + gaps
				

file_counter = 0

for filename in os.listdir(sys.argv[2]):

	file_orthogroup = filename.split("_")[0]

	if file_orthogroup in usable_orthogroups:

		orthogroup_file = os.path.join(sys.argv[2], filename)
		parse_orthogroup_fasta(orthogroup_file)
		file_counter +=1

		if file_counter%100 == 0:
			print("Finished parsing file " + str(file_counter) + " out of " + str(len(usable_orthogroups)))

with open("rumex_concatenated_buckwheat.fasta", 'w') as f:
	
	for key, val in sequences_dict.items():
		f.write(key + "\n")
		f.write(val + "\n")



