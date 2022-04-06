import os

clustal = open("./clustal.txt", "r")
analysis_range = clustal.readlines()[10073:10261] #keep reference area with good coverage
clustal.close()

#keep areas of 100% coverage
with open("./phylogeny_input.txt", "w+") as phylogeny:
    for line in analysis_range:
        if "-" in line:
            continue
        name = line.split()[0]
        sequence = line.split()[1][:-1]
        phylogeny.write(">" + name + "\n" + sequence + "\n")
