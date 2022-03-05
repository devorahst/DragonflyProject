import os
import csv
from_dir = '.'


with open ('fig2_summary.csv','w', newline = '' ) as csvfile:
        summarywriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        summarywriter.writerow(['Comparison', 'Comparison_Type', 'Species', 'Recovered_loci'])
        directories_in_directory = os.listdir(from_dir)
        for directory in directories_in_directory:
                if directory.find('ephem') != -1 or directory.find('odonata') != -1:
                        comparison = directory[0] + '/' + directory.split('_', 2)[-1][0]
                        comparison = comparison.upper()
                        if comparison[0] == comparison[2]:
                                comparison_type = 'Matched'
                        else:
                                comparison_type = 'Mismatched'
                        files_in_directory = os.listdir(directory)
                        files_in_directory.sort()
                        for filename in files_in_directory:
                                if filename.find('ORTHO') != -1 and filename.find('.fasta') != -1:
                                        species_id = filename[0:8]
                                        filepath = os.path.join(from_dir, directory, filename)#complimentary ORTHO.fasta
                                        try:
                                                with open(filepath, 'r') as ORTHO_file:
                                                        ortho = ORTHO_file.read()
                                                        recovered_loci = ortho.count('>L')#count # loci
                                                        summarywriter.writerow([comparison, comparison_type, species_id, str(recovered_loci)])
                                        except IOError as e:# ignore directiories that don't contain the fasta
                                                if e.errno != errno.ENOENT:#raise exception if dif from "file or directory doesn't exist"
                                                        raise
