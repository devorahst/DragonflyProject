# Trim Data

1. You must have obtained all of the raw data and placed the data in odonata_raw_data and ephem_raw_data respectively.

2. You must have created and activated the trim environment. If you have not follow the instructions [here](../environments/).

3. Once this is done, ensure that the names_to_trim.txt files in the raw_data directories match the paths to the actual raw data.

4. Add your personal email to each .job file.

5. Run each job
    1. "sbatch trim_ephem.job"
    2. "sbatch trim_odonata.job"