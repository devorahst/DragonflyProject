# Running the assembler

1. Download the reference genomes by running "wget https://byu.box.com/s/0a11f9u7obzegcyfvhz20ob3t5kcivej" inside of the assembly directory.
    1. Move the files to their correct locations by running the following commands while in the assembly directory.
        1. "cp reference_genomes/G* odonata_on_ephem_assembly/."
        2. "cp reference_genomes/t* odonata_on_odonata_assembly/."
        3. "cp reference_genomes/G* ephem_on_ephem_assembly/."
        4. "cp reference_genomes/t* ephem_on_odonata_assembly/."

2. You should have already downloaded the [pipeline environment](../environments/)

3. You should have [trimmed](../trim_data/) the raw data and all of the trimmed data should be in the trim_data directory.

4. In order to launch each job, the directory needs a text file with the species files and names in a tab delimited format with correct file paths, the reference genome, the probe hits, and the reference loci, and the database files. If you have followed all of the above steps this should already be the case.

5. The .job file is dependent on a python file called “ASS_F4_fast.py” this script requires access to usearch. Make sure usearch is in the directory and is executable.

6. The array number for the slurm file will be the same size as the number of species in the species names file. For our test 261 for Odonata and 96 for Ephemeroptera.

7. Change the email to your email in each .job file.

8. Use "sbatch" followed by the job file to launch the script. Correctly running jobs will produce A LOT of files. The files that are needed end in targetsFULL_ORTHO.fasta and targets_ORTHO.fasta.