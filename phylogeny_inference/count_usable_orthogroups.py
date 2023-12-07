import sys

with open(sys.argv[1], 'r') as genecounts:

	next(genecounts)
	usable_count = 0

	for line in genecounts:

		splitline = line.strip().split("\t")
		orthogroup_name = splitline[0]
		counts = splitline[1:-1]
		counts = [int(x) for x in counts]
		
		num_species = 0
		num_duplicates = 0

		for count in counts:	
			if count >= 1:
				num_species +=1
			if count >= 2:
				num_duplicates +=1

		if num_species >= 9 and num_duplicates <= 1:
			usable_count +=1 
			print(orthogroup_name)

