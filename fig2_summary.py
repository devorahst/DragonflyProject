import os
import csv
from_dir = '.'
comparison = 'EE' #EE EO OO OE

with open ('fig2_summary.csv','w', newline = '' ) as csvfile:
        summarywriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        summarywriter.writerow(['Comparison', 'Species', 'Recovered_loci'])
        files_in_directory = os.listdir(from_dir)
        filtered_files = [file for file in files_in_directory if file.endswith(".fasta")]
        filtered_files.sort()
        for filename in filtered_files:
                if filename.find("ORTHO") != -1:
                        species_id = filename[0:8]
                        filepath = os.path.join(from_dir, filename)#complimentary ORTHO.fasta
                        with open(filepath, 'r') as ORTHO_file:
                                ortho = ORTHO_file.read()
                                recovered_loci = ortho.count('>L')#count # loci
                                summarywriter.writerow([comparison, species_id, str(recovered_loci)])
