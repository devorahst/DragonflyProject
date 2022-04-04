#Figure 3
Run create_clustal_input.py: This will create clustal_input.txt
Copy and paste the contents of clustal_input.txt into https://www.ebi.ac.uk/Tools/msa/clustalo/, make sure you select DNA. All other parameters should be left at the default.
Select "Download Alignment File" and copy and paste the contents into clustal.txt.
Run create_phylogeny_input.py: This will create phylogeny_input.txt.
Copy and paste the contents of phylogeny_input.txt into https://www.ebi.ac.uk/Tools/phylogeny/simple_phylogeny/. All parameters should be left at the default.
Note: For this figure L910 was used as the input Loci for the alignment. This can be changed on line 58 and 59 of create_clustal_input.py. After the multiple sequence alignment was created an arbitrary region that showed good coverage for the majority of species was used for the phylogeny. This can be changed on line 4 of create_phylogeny_input.py.
