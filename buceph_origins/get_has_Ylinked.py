import sys
from Bio.Seq import Seq

Ylinked_genes = []
complements = []

with open(sys.argv[1], 'r') as gff_file:
	
	for line in gff_file:
		splitline = line.strip().split("\t")
		
		if splitline[0] == "Y1" and splitline[2] == "CDS":

			lower_coord = float(splitline[3])/1000000
			upper_coord = float(splitline[4])/1000000
			 
			if lower_coord > 64 and upper_coord < 272:
				gene_ID = splitline[-1]
				
				if gene_ID not in Ylinked_genes:
					Ylinked_genes.append(splitline[-1])

		elif splitline[0] == "Y2" and splitline[2] == "CDS":
			
			lower_coord = float(splitline[3])/1000000
			
			if lower_coord > 159:
				gene_ID = splitline[-1]

				if gene_ID not in Ylinked_genes:
					Ylinked_genes.append(splitline[-1])
					complements.append(splitline[6])

with open(sys.argv[2], 'r') as cds_file:
	
	good_transcript = False
	current_seq = ""
	current_complement = ""
	used_genes = []
	
	for line in cds_file:
		if line.startswith(">"):

			gene_ID = line.strip().split()[0]
			gene_ID = gene_ID.replace(">", "")
			
			if any(gene_ID in string for string in Ylinked_genes):
				print(line.strip())

				if len(used_genes) == 0:

					used_genes.append(gene_ID)
					complement_index = [i for i, s in enumerate(Ylinked_genes) if gene_ID in s][0]
					current_complement = complements[complement_index]
				else:
					if current_complement == "+":
						print(current_seq)
					elif current_complement == "-":
						reverse_seq = Seq(current_seq)
						reverse_seq = reverse_seq.reverse_complement()
						print(reverse_seq)

					used_genes.append(gene_ID)
					complement_index = [i for i, s in enumerate(Ylinked_genes) if gene_ID in s][0]
					current_complement = complements[complement_index]
					current_seq = ""
				
				good_transcript = True
			else:
				good_transcript = False

		elif good_transcript == True:
			current_seq = current_seq + line.strip()
		elif good_transcript == False:
			continue
