# Name Changing

1. After all of the data has been run through the assembler, copy all of the files that end with targetsFULL_ORTHO.fasta into the respective results directory. This has already been done for you and all of the results can be found in the results directory.
    1. For example: "cp ../assembly/ephem_on_odonata_assembly/*targetsFULL_ORTHO.fasta* ../results/ephem_on_odonata_results/."

2. Activate the pipeline environment if you have not already done so.
    1. "module load miniconda3"
    2. "source activate chase"

3. Run the name changing script.
    1. "python change_names.py"