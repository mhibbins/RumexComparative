import sys
from Bio.Seq import Seq

buceph_cds_contig = []
buceph_cds_coords = []
buceph_cds_name = []
complements = []

with open(sys.argv[1], 'r') as gff_file:
	
	for line in gff_file:
		splitline = line.strip().split("\t")

		if len(splitline) >= 3:	
			if splitline[2] == "CDS":
				
				buceph_cds_contig.append(splitline[0])
				buceph_cds_name.append(splitline[-1])

				coord_lower = float(splitline[3])
				coord_upper = float(splitline[4])
				coords = [coord_lower, coord_upper]
				buceph_cds_coords.append(coords)
				complements.append(splitline[6])	

buceph_coding_seqs = []

with open(sys.argv[2], 'r') as cds_file:
	
	current_contig_ID = ""
	used_contigs = []
	current_contig_sequence = ""
		
	for line in cds_file:
				
		if line.startswith(">"):
			if len(used_contigs) == 0:
				current_contig_ID = line.strip()[1:]
				used_contigs.append(current_contig_ID)
				continue
			else:
				contig_indices = [i for i, x in enumerate(buceph_cds_contig) if x == current_contig_ID]
				contig_cds_coords = [buceph_cds_coords[i] for i in contig_indices]
				
				for i, coord in enumerate(contig_cds_coords):
					lower_coord = int(coord[0]) - 1
					upper_coord = int(coord[1]) - 1
					coding_seq = current_contig_sequence[lower_coord:upper_coord]

					if complements[i] == "+":
						buceph_coding_seqs.append(coding_seq)
					elif complements[i] == "-":
						coding_seq = Seq(coding_seq)
						coding_seq = coding_seq.reverse_complement()
						buceph_coding_seqs.append(coding_seq)
				
				current_contig_ID = line.strip()[1:]

				if current_contig_ID not in used_contigs:
					current_contig_sequence = ""				
		else:
			current_contig_sequence = current_contig_sequence + line.strip()

for i in range(len(buceph_coding_seqs)):

	print(">" + buceph_cds_name[i])
	print(buceph_coding_seqs[i])

		
			

