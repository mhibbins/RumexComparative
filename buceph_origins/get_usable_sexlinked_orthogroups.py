import sys

with open(sys.argv[1], 'r') as genecounts:

	next(genecounts)
	usable_count = 0

	for line in genecounts:

		Xseq = False
		Yseq = False
		outseq = False
		bucseq = False

		splitline = line.strip().split("\t")
		orthogroup_name = splitline[0]
		counts = splitline[1:-1]
		counts = [int(x) for x in counts]
		
		num_duplicates = 0

		for count in counts:	
			if count >= 2:
				num_duplicates +=1

		if counts[0] >= 1:
			Xseq = True
		if counts[1] >= 1:
			Yseq = True
		if counts[2] >= 1 or counts[3] >= 1 or counts[4] >= 1:
			outseq = True
		if counts[5] >= 1:
			bucseq = True
		

		if num_duplicates <= 1 and Xseq and Yseq and outseq and bucseq:
			print(orthogroup_name)

