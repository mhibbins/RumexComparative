import sys
import os
import csv

def is_integer(n):
	try:
		float(n)
	except ValueError:
		return False
	else:
		return float(n).is_integer()

def parse_paml_output_comparison(comparison_linelist):

	if "in paml version" in comparison_linelist[0]:
		return
	else:
		spnames = comparison_linelist[0].split("...")

		if len(spnames) == 2:

			spname1 = spnames[0][spnames[0].find("(")+1:spnames[0].find(")")]

			if "FtPin" in spname1:
				spname1 = "F_tataricum"
			else:
				spname1 = spname1.split("_")
				spname1 = "_".join([spname1[0], spname1[1]])
			
			spname2 = spnames[1][spnames[1].find("(")+1:spnames[1].find(")")]
			
			if "FtPin" in spname2:
				spname2 = "F_tataricum"
			else:
				spname2 = spname2.split("_")
				spname2 = "_".join([spname2[0], spname2[1]])
		else:
			return
		
		if spname1 == spname2:
			if len(comparison_linelist) == 4:
				splitline = comparison_linelist[3].split()
				dS = float(splitline[-1].replace('=', ''))
				return [spname1, dS]
			else:
				return
		else:
			return	

def parse_paml_output(paml_output_file):

	species = []
	dS = []

	with open(paml_output_file, 'r') as outfile:

		new_comparison = False
		current_comparison = []

		for line in outfile:

			splitline = line.strip().split()

			if len(splitline) > 0 and is_integer(splitline[0]):
				comparison = parse_paml_output_comparison(current_comparison)

				if comparison is not None:
					species.append(comparison[0])
					dS.append(comparison[1])

				new_comparison = True

			if new_comparison == True:
				current_comparison = []
				current_comparison.append(line.strip())
				new_comparison = False

			elif new_comparison == False and len(splitline) > 0:
				current_comparison.append(line.strip())

	return species, dS

all_species = []
all_dS = []

file_counter = 0

for filename in os.listdir(sys.argv[1]):
	
	pamlfile = os.path.join(sys.argv[1], filename)
	species, dS = parse_paml_output(pamlfile)
	all_species.extend(species)
	all_dS.extend(dS)
	file_counter +=1

	if file_counter%100 == 0:
		print("Finished parsing file " + str(file_counter) + " out of " + str(26348))

with open('rumex_dS_values.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerows(zip(all_species, all_dS))
