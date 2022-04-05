import os
import csv
#TO DO: Replace from_dir with the file path from this file to the directory that contains your data
from_dir = os.path.join('.','results') 
# TO DO: replace directory_key_word with a key word in the title of your directories that contain the recovered orthologs
directory_key_word = 'final'
# TO DO: replace data_file_key_word with a key word in the title of your data files that contain the recovered orthologs
data_file_key_word = 'targetsFULL_ORTHO'
	
with open ('fig2_summary.csv','w', newline = '' ) as csvfile:
	summarywriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	summarywriter.writerow(['Comparison', 'Comparison_Type', 'Species', 'Recovered_loci'])
	directories_in_directory = os.listdir(from_dir)
	for directory in directories_in_directory:
		if directory.find(directory_key_word) != -1:#finds the right directories, edit to match your directory names
			comparison = directory[0] + '/' + directory.split('_', 2)[-1][0] #Abreviate to first letters
			comparison = comparison.upper()
			if comparison[0] == comparison[2]:
				comparison_type = 'Matched'#Is O/O or E/E?
			else:
				comparison_type = 'Mismatched' #Is O/E or E/O
			files_in_directory = os.listdir(from_dir + '/' + directory)
			files_in_directory.sort()
			for filename in files_in_directory:
				if filename.find(data_file_key_word) != -1 and filename.find('.fasta') != -1:
					species_id = filename.split('_', 1)[0]#find the string until '_', species#
					filepath = os.path.join(from_dir, directory, filename)#complimentary ORTHO.fasta
					try:
						loci_list = []
						with open(filepath) as ORTHO_file:
							for line in ORTHO_file:
								if line.find('>L') == 0:
									loci_temp = line.split('_')
									loci = '_'.join(loci_temp[:5])
									if (loci not in loci_list): #get rid of duplicates
										loci_list.append(loci)
							recovered_loci = len(loci_list)		
							summarywriter.writerow([comparison, comparison_type, species_id, str(recovered_loci)])
					except IOError as e:# ignore directiories that don't contain the fasta
						if e.errno != errno.ENOENT:#raise exception if dif from "file or directory doesn't exist"
							raise
