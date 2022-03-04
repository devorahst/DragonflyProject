import os
import csv
from_dir = '.'
comparison = 'EE' #EE EO OO OE

with open ('fig2_summary.csv','w', newline = '' ) as csvfile:
        summarywriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        summarywriter.writerow(['Comparison', 'Species', 'Percent_Recovery'])
        files_in_directory = os.listdir(from_dir)
        filtered_files = [file for file in files_in_directory if file.endswith(".fasta")]
        filtered_files.sort()
        for i in range(0, len(filtered_files), 2):
                filepath1 = os.path.join(from_dir, filtered_files[i]) #FULL.fasta
                species_id = filepath1[2:10]
                filepath2 = os.path.join(from_dir, species_id + "_targetsFULL_ORTHO.fasta")#complimentary ORTHO.fasta
                #print(filepath1, type(filepath1), filepath2)
                try:
                        with open(filepath1, 'r') as FULL_file, open(filepath2, 'r') as ORTHO_file:
                                full = FULL_file.read()
                                ortho = ORTHO_file.read()
                                total_possible_locii = full.count('>L')
                                num_ortho_found = ortho.count('>L')
                                percent_recovery = 100*(num_ortho_found/total_possible_locii)
                                summarywriter.writerow([comparison, species_id, str(percent_recovery)])
                except IOError as e:# ignore unpaired files
                        if e.errno != errno.ENOENT:# reraise exception if different from "file or directory doesn't exist"
                                raise
