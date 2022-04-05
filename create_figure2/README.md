README:
################################################################################################
REQUIREMENTS:

create_figure2 uses Python version 2.7.5

Python libraries that must be installed include:

1. os
2. cv2

If any of those libraries is not currently in your Python Path, use the following command:
pip install --user [library_name]
to install the library in your path.

R Libraries that must be installed include:

1. tidyverse
2. ggplot2

################################################################################################

Input Files:
This algorithm requires a directory containing at least 1 fasta file that have header/sequence alternating lines with a greater than symbol (>) 
between every CDS region and at the end of each sequence. To create this file, look at the example files in
the directory smallTest.

################################################################################################

USAGE:

Specify the version of python and then fig2_summary.py

Example usage:

python3 fig2_summary.py

Running the above command will produce a single output file called fig2_summary.csv in the current directory. For us, this test took
approximately 4 seconds of real time and 41 seconds of user time.

Once fig2_summary.csv has been created, import fig2_summary.csv from test(base) into RStudio and run fig2_plot.R in RStudio. 

################################################################################################


