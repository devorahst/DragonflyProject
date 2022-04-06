#/bin/bash
module load miniconda3
conda env create -f trim_env.yml
source activate trimenv 

# IF THIS EXITS WITH AN ERROR SAYING THE ENVIRONMENT EXISTS JUST ACTIVATE THE ENVIRONMENT
