import os

name_reference = {}
with open("error.txt", 'w') as errors:
    with open("../odonata_raw_data/names_trimmed_species.txt", 'r') as ref:
        lines = ref.readlines()
        for line in lines:
            line = line.rstrip()
            columns = line.split('\t')
            if columns[1][33:39] in name_reference.keys():
                name_reference[columns[1][33:39]].append(columns[2])
            else:
                name_reference[columns[1][33:39]] = [columns[2]]
    species_reference = {}
    with open("./species_data_edited.csv", 'r') as ref:
        lines = ref.readlines()
        for line in lines[11:]:
            line = line.rstrip()
            columns = line.split(',')
            if columns[5] != '-' and columns[5] != '':
                for name in name_reference[columns[5]]:
                    if columns[1].startswith("IS_group"):
                        species_reference[name] = "OD_" + "Family" + "_" + columns[2] + "_" + columns[3]
                    else:
                        species_reference[name] = "OD_" + columns[1] + "_" + columns[2] + "_" + columns[3]
    
    errors.write("ODONATA_on_ODONATA\n")
    for name in species_reference.keys():
        try:
            with open("../results/odonata_on_odonata_results/" + name + "_targetsFULL_ORTHO.fasta", 'r') as old:
                old_content = old.read().rstrip()
                new_content=old_content.replace(name, species_reference[name])
                with open("../results/odonata_on_odonata_final/" + species_reference[name] + "_targetsFULL_ORTHO.fasta", 'w') as new:
                    new.write(new_content + '\n')
        except Exception as e:
            errors.write(str(e) + '\n')

    errors.write("ODONATA_on_EPHEM\n")
    for name in species_reference.keys():
        try:
            with open("../results/odonata_on_ephem_results/" + name + "_targetsFULL_ORTHO.fasta", 'r') as old:
                old_content = old.read().rstrip()
                new_content=old_content.replace(name, species_reference[name])
                with open("../results/odonata_on_ephem_final/" + species_reference[name] + "_targetsFULL_ORTHO.fasta", 'w') as new:
                    new.write(new_content + '\n')
        except Exception as e:
            errors.write(str(e) + '\n')
    
    errors.write("EPHEM_on_EPHEM\n")
    for old_name in os.listdir("../results/ephem_on_ephem_results/"):
        new_name = "EP_" + old_name.split('_')[4] + '_' + old_name.split('_')[5] + '_' + old_name.split('_')[6]
        with open("../results/ephem_on_ephem_results/" + old_name, 'r') as old:
            old_content = old.read().rstrip()
            new_content = old_content.replace(old_name[:-24], new_name)
            with open("../results/ephem_on_ephem_final/" + new_name  + "_targetsFULL_ORTHO.fasta", 'w') as new:
                new.write(new_content + '\n')
    
    errors.write("EPHEM_on_ODONATA\n")
    for old_name in os.listdir("../results/ephem_on_odonata_results/"):
        new_name = "EP_" + old_name.split('_')[4] + '_' + old_name.split('_')[5] + '_' + old_name.split('_')[6]
        with open("../results/ephem_on_odonata_results/" + old_name, 'r') as old:
            old_content = old.read().rstrip()
            new_content = old_content.replace(old_name[:-24], new_name)
            with open("../results/ephem_on_odonata_final/" + new_name + "_targetsFULL_ORTHO.fasta", 'w') as new:
                new.write(new_content + '\n')