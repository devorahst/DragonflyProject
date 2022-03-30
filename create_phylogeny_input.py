import os

clustal = open("../clustal.txt", "r")
analysis_range = clustal.readlines()[5128:5210] #keep reference area with good coverage
clustal.close()

#keep areas of 100% coverage
with open("../phylogeny_input.txt", "a+") as phylogeny:
    for line in analysis_range:
        if "-----" in line:
            continue
        name = line.split()[0]
        sequence = line.split()[1][:-7]
        phylogeny.write(">" + name + "\n" + sequence + "\n")