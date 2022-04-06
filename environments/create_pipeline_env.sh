#!/bin/bash
module load miniconda3
conda env create -f pipeline_env.yml
conda activate chase

# IF THIS EXITS WITH AN ERROR SAYING THE ENVIRONMENT EXISTS JUST ACTIVATE THE ENVIRONMENT
