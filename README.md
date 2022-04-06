# DragonflyProject
#####################################################################################################

**Get the data** 

The Ephemeroptera dataset was created by Miller et. al. [DOI: 10.1111/syen.12298] for use in analyzing the evolution of tusks in burrowing mayflies. The Odonata dataset was created by Bybee et. al. [10.1186/s12983-016-0176-7] for use in an evolutionary analysis. Data was obtained from these researchers with authorization for use in our analysis. Data is stored on the Mary Lou computing cluster at Brigham Young University. For access please reach out to the authors.


#####################################################################################################

**Create Environment**

In Anaconda Prompt, run the following commands:   
1. Module load miniconda3
2. Conda Create -n name (this is saved locally so you can name it anything)
3. Conda activate/source activate name 

-Download these four packages while in the environment: 
1. Biopython  v.1.78
conda install -c conda-forge biopython
2. Spades v.3.13.0
conda install --channel bioconda spades=3.13.0
3.Numpy v.1.19.1
conda install -c anaconda numpy
4. Mafft
conda install -c bioconda mafft
        or
conda install --channel bioconda mafft=7.475


#####################################################################################################
**Trim the data**

Follow the directions in the trim_data directory

#####################################################################################################
**Run the assembly**

Follow the directions in the assembly directory

#####################################################################################################

**Concatenate and rename data**

#####################################################################################################

**[Create](/create_figure2) figure 2**

#####################################################################################################

**[Create](/create_figure3) figure 3**

#####################################################################################################
