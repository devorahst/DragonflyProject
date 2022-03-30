import os
import itertools
		
from_dir = '../on_odonata_results'
files_in_directory = os.listdir(from_dir)
files_in_directory.sort()
species_in_files = {}
odo_ref = open("../ODONATA/names_trimmed_species.txt", 'r')
#Get list of odonata species
odo_species = []
for line in odo_ref.readlines():
	odo_species.append(line.split('\t')[2][:-3])
may_ref = open("../EPHEM/ephem_names_new.txt", 'r')
#Get list of mayfly species
may_species = []
for line in may_ref.readlines():
	may_species.append(line.split('\t')[2][6:-1])
odo_ref.close()
may_ref.close()
#Create multi-fasta files based on locus with only one species per file
for filename in files_in_directory:
	if filename.find('targetsFULL_ORTHO.fasta') != -1: #if "targetsFULL_ORTHO" in the name of the fasta file
		species_id = filename.split('_targets', 1)[0]
		if species_id.startswith("EP"):
			species_id = species_id[6:]
		filepath = os.path.join(from_dir, filename)
		with open(filepath, 'r') as ORTHO_file:
			for line1,line2 in itertools.zip_longest(*[ORTHO_file]*2):#look and 2 lines at a time
				if (line1[0] == '>'):
					locus =line1.partition('_')[0] + '.fasta'
					locus = locus[1:] #get rid of ">"
					with open(locus, 'a+') as writefile:
						if locus not in species_in_files.keys():
							species_in_files[locus] = []
						if (species_id not in species_in_files[locus]): #Don't allow duplicates
							species_in_files[locus].append(species_id)
							writefile.write('>' + species_id + '\n')
							writefile.write(line2)
							#File just for mayfly
							if species_id in may_species:
								with open(locus+"_mayfly", 'a+') as mayfly:
									mayfly.write('>' + species_id.split("_")[4].capitalize() + '_' + species_id.split("_")[5].lower() + '\n') #Only write genus and species
									mayfly.write(line2)
							#File just for odonata
							if species_id in odo_species and "UNKNOWN" not in species_id and "group" not in species_id: #Only allow known names
								with open(locus+"_odonata", 'a+') as odonata: #Only write genus and species
									odonata.write('>' + species_id.split("_")[1].capitalize() + "_sp" + '\n')
									odonata.write(line2)
							if "group" in species_id:
								with open(locus+"_odonata", 'a+') as odonata: #Only write genus and species
									odonata.write('>' + species_id.split("_")[3].capitalize() + "_sp" + '\n')
									odonata.write(line2)

						else: 
							continue

#Isolate 910 for figure3
os.system("cat L910.fasta_mayfly >> clustal_input.txt")
os.system("cat L910.fasta_odonata >> clustal_input.txt")
os.system("rm L*.fasta*")
		



