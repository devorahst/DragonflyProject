# Running the assembler.

1. Download the reference genomes by running "wget https://byu.box.com/s/0a11f9u7obzegcyfvhz20ob3t5kcivej"

2. Data should be previously trimmed and the user should be in the chase conda environment.

3. In order to launch each job, the directory needs the species names file in the correct format, the reference genome, the probe hits, and the sample sequences.

4. The slurm file/job job is dependent on a python file called “ASS_F4_fast.py” this script requires access to usearch to function. So make sure usearch is in the directory and is executable.

5. The array number for the slurm file will be the same size as the number of species in the species names file. For our test 260 for Odonata and 95 for Ephem.

6. Use "sbatch" followed by the job file to launch the script. Correctly running jobs will produce A LOT of files. The files that are needed end in targetsFULL_ORTHO.fasta and targets_ORTHO.fasta.


