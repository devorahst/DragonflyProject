#!/usr/bin/env python


# Script was written by Jesse Breinholt (jessebreinholt@gmail.com)
# assume linux command line tools, usearch, ncbi blast, SPADES assembler in path


# UF cluster---- module load gcc/5.2.0 spades python ncbi_blast usearch



import os, sys
import gzip
import multiprocessing
import math



blastdb="makeblastdb -dbtype \"nucl\" -in %s -out %s"
mtemp="mkdir %s"
ass="spades.py --careful -o %s -1 %s -2 %s -t %s"
ucollapse="usearch -cluster_fast %s -id 0.98 -query_cov 0.98 -strand both -sort length -centroids %s"
blastdb="makeblastdb -dbtype \"nucl\" -in %s -out %s"
realblast= "blastn -query %s -db %s -out %s -outfmt 6 -evalue 0.0001 -qcov_hsp_perc 80 -num_threads %s"
rblast= "tblastx -query %s -db %s -out %s -outfmt 6 -evalue 0.01 -num_threads %s"
rblast2= "tblastx -query %s -db %s -out %s -outfmt \"6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qframe\" -evalue 0.0001 -qcov_hsp_perc 0.50 -num_threads %s"
filter1="sort -k12,12rn %s | sort -u -k1,2 > %s"
filter2="sort -k12,12rn %s | sort -u -k1,1 > %s"
joincat="cat %s %s > %s"
cat4="cat %s %s %s %s > %s"
cat7="cat %s %s %s %s %s %s %s | sort -k1,1 -k12,12nr > %s"
fasta_filter="grep --no-group-separator -A1 -F -f %s %s > %s"
key_filter="grep --no-group-separator -F -f %s %s > %s"
kkill="rm -r %s"

blastdict= {}
locidict={}
lista = []
arguments = sys.argv

if len(arguments) == 1:
	sys.exit("try python genome_getprobe_BLAST.py -h for help")
try:
	hflag = arguments.index("-h")
except:
	hflag = None

if hflag:
	sys.exit("\n\n#################################################################\n\n./ASS_F.py -inp REF_Probe.fasta -inpc REF_Probe.topblasthits -ing genome.fasta.db -threads ## -tname taxaname -flanksize ## -1 read1 -2 read2  -rname Reference name in target file \n\n\n\t\t-inp: fasta file of probe sequences\n\t\t-inpc: Coordinate position of reference probes to genome in blast6 format.\n\r\r -ing: genome or transcriptome file with sequnces data for each sequnces on a single line\n\t\t-threads: number of threads to use in blast\n\t\t-tname: taxa name you want to put on the output sequnces\n\t\t-flanksize: number of base pairs you want inclulded before or after the probe hit\n\t\t\t-setupGenome_db: makes a NCBI blast data dase for the refrence genome that can then be uses for the -ing flag\n\t\t\t-findprobehit: uses NCBI blastn to find the coordinates of the probes on the genome and filters for the best hit and the output ending in probehits_out can be used for input to -inpc")#################################################################\n\n")

try:
	threads = int(arguments[arguments.index("-threads")+1])
except:
	threads = 16

try:
	makeGblastdb = arguments[arguments.index("-setupGenome_db")+1]
except:
	makeGblastdb = None

if makeGblastdb:
	os.system(blastdb % (makeGblastdb, makeGblastdb+"_db"))	
	# sys.exit("made genome blast data base "+makeGblastdb+"_db")
	
try:
	genome = arguments[arguments.index("-ing")+1]
except:
	sys.exit("Error: need genome blastdb use -setupGenome_db flag to set up the genome blast database")

try:
	probeset = arguments[arguments.index("-inp")+1]
except:
	sys.exit("Error: need probe fasta")

try:
	taxaname = arguments[arguments.index("-tname")+1]
except:
	sys.exit("Error: need taxa name")
	
try:
	findprobehitblast = arguments[arguments.index("-findprobehit")+1]
except:
	findprobehitblast = None

if findprobehitblast:
	os.system(realblast % (probeset, genome+"_db", taxaname+"preprobehits_out", threads))
	os.system(filter2 % (taxaname+"preprobehits_out", taxaname+"probehits_out"))
	os.system(kkill %(taxaname+"preprobehits_out"))
	sys.exit("used blast to find probe locations in the genome use "+taxaname+"probehits_out as -inpc")

try:
	coordsprobeset = arguments[arguments.index("-inpc")+1]
except:
	sys.exit("Error: coordinate position of reference probes to genome in blast 6 format you can use -findprobehit to blast probe to genome and get coordinates file")


try:
	R1 = arguments[arguments.index("-1")+1]
except:
	sys.exit("Error: need read 1")
try:
	R2 = arguments[arguments.index("-2")+1]
except:
	sys.exit("Error: need read 2")

try:
	flank = int(arguments[arguments.index("-flanksize")+1])
except:
	flank = 0


try:
	refname= arguments[arguments.index("-rname")+1]
except:
	sys.exit("Error: need ref name")

try:
	fullprobeset = arguments[arguments.index("-inpf")+1]
except:
	fullprobeset = arguments[arguments.index("-inp")+1]




#S1 make taxa dir
print("\n\n making tmp dir: "+ taxaname+"_tmp\n\n")
os.system(mtemp % (taxaname+"_tmp"))


#S2 assembly
print("\n\nSPADES error correction and Assembly\n\n")
os.system(ass % ("$TMPDIR/ASS/",R1,R2,threads))



#S3 Collapsing ASSEMBLY [id:0.98, query_cov: 0.98]
print("\n\nCollapsing Assembly [id:0.98, query_cov: 0.98]\n\n")
os.system( ucollapse % ("$TMPDIR/ASS/scaffolds.fasta",taxaname+"_tmp/rscaffolds.fasta"))


#S4 making blast databases
print("Making assembly blast databases")
os.system(blastdb % (taxaname+"_tmp/rscaffolds.fasta", taxaname+"_tmp/rscaffolds.fasta_db"))


#S5 split probe fasta for TBLASTX to Assembly
print("Splitting probe fasta")
seqcount=0
with open(probeset) as pf:
	for line in pf:
		if line.startswith(">"):
			seqcount+=1
print("Probe set has "+str(seqcount)+" loci" )

seqdiv=math.ceil(seqcount/7)

p1=open(taxaname+"_tmp/p1.fa", "w")
p2=open(taxaname+"_tmp/p2.fa", "w")
p3=open(taxaname+"_tmp/p3.fa", "w")
p4=open(taxaname+"_tmp/p4.fa", "w")
p5=open(taxaname+"_tmp/p5.fa", "w")
p6=open(taxaname+"_tmp/p6.fa", "w")
p7=open(taxaname+"_tmp/p7.fa", "w")

p1c=0
p2c=0
p3c=0
p4c=0
p5c=0
p6c=0
p7c=0

with open(probeset) as pf:
	for line in pf:
		if p1c <= seqdiv:
			if line.startswith(">"):
				p1.write(line)
			elif ">" not in line:
				p1.write(line)
				p1c+=1
		elif p1c > seqdiv and p2c <= seqdiv:
			if line.startswith(">"):
				p2.write(line)
			elif ">" not in line:
				p2.write(line)
				p2c+=1
		elif p1c > seqdiv and p2c > seqdiv and p3c <= seqdiv:
			if line.startswith(">"):
				p3.write(line)
			elif ">" not in line:
				p3.write(line)
				p3c+=1
		elif p1c > seqdiv and p2c > seqdiv and p3c > seqdiv and p4c <= seqdiv:
			if line.startswith(">"):
				p4.write(line)
			elif ">" not in line:
				p4.write(line)
				p4c+=1

		elif p1c > seqdiv and p2c > seqdiv and p3c > seqdiv and p4c > seqdiv and p5c <= seqdiv:
			if line.startswith(">"):
				p5.write(line)
			elif ">" not in line:
				p5.write(line)
				p5c+=1
		elif p1c > seqdiv and p2c > seqdiv and p3c > seqdiv and p4c > seqdiv and p5c > seqdiv and p6c <= seqdiv:
			if line.startswith(">"):
				p6.write(line)
			elif ">" not in line:
				p6.write(line)
				p6c+=1
		elif p1c > seqdiv and p2c > seqdiv and p3c > seqdiv and p4c > seqdiv and p5c > seqdiv and p6c > seqdiv:
			if line.startswith(">"):
				p7.write(line)
			elif ">" not in line:
				p7.write(line)
				p7c+=1





p1.close()
p2.close()
p3.close()
p4.close()		
p5.close()
p6.close()
p7.close()


#S6 Blast the 4 part of the probes to assembly
print("TBLASTX probes to Assembly")

qthreads=int(threads/4)



def pbf(i):
	istr=str(i)
	print("Running TBLASTX probe subset_"+istr)
	os.system(rblast2 % (taxaname+"_tmp/p"+istr+".fa",taxaname+"_tmp/rscaffolds.fasta_db",taxaname+"_tmp/screen"+istr+"_out",2))
	print("subset "+istr+" done")

def pbf_process(i):
	with multiprocessing.Pool() as pool:
		pool.map(pbf,i)

if __name__ == "__main__":
	i=[1,2,3,4,5,6,7]
	pbf_process(i)


#S6 Joining TBLASTX of probes and colloapsing identicals
print("\n\ASSEMBLY on Target screen\n\n")
os.system(cat7 % (taxaname+"_tmp/screen1_out",taxaname+"_tmp/screen2_out",taxaname+"_tmp/screen3_out",taxaname+"_tmp/screen4_out",taxaname+"_tmp/screen5_out",taxaname+"_tmp/screen6_out",taxaname+"_tmp/screen7_out", taxaname+"_tmp/screenall_out"))

###os.system(filter1 % (taxaname+"_tmp/screenall_out", taxaname+"_tmp/clean_screen_out"))
##################


#keep best bit score any any 80 of the best bit score
bitcheck=0
seqcheck = ''
namelist = set()


soutfile = open(taxaname+"_tmp/clean_screen_out", "w")
table = open(taxaname+"_tmp/screenall_out","r")
line = table.readline()
count1=0
keepcount=0

while line:
	seqname, scaf, id, alen, missm, gap, qs, qend, ts, tend, eval, bit, qframe =line.split()
	bit = float(bit)
	count1+=1
	if seqname == seqcheck:
		if bit/bitcheck >= 0.80:
			soutfile.write(line)
			keepcount+=1
			line = table.readline()
		if bit/bitcheck < 0.80:
			line = table.readline()
	if seqname != seqcheck:
		seqcheck = seqname
		bitcheck = bit
		soutfile.write(line)
		keepcount+=1
		line = table.readline()

table.close()
soutfile.close()

##########################################


#S7 Make Assembly a single line fasta
mfasta2=open(taxaname+"_tmp/sl_rscaffolds.fasta", "w")
lc=0
with open(taxaname+"_tmp/rscaffolds.fasta") as f:
	for line in f:
		if line.startswith(">"):
			if lc==0:
				mfasta2.write(line)
				lc+=1
			elif lc !=0:
				mfasta2.write("\n"+line)
		else:	
			mfasta2.write(line.strip("\n"))
mfasta2.close()


#S8 Identifying Loci and trimming to target region
print("\n\nUsing TBLASTX results to identifying possible Loci and trimming to target region\n\n")
blastfile=open(taxaname+"_tmp/clean_screen_out")

print("\n\nMaking hit dictionary\n\n")
#qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qframe

for line in blastfile:
	line = line.strip().split()
	if line[1] in blastdict.keys():
		lista = blastdict[line[1]]
		locilist = line[0].split("_")
		lista.append(locilist[0]+"_"+line[8]+"_"+line[9]+"_"+line[11]+"_"+line[12])
		blastdict[line[1]] = lista
	else:
		lista = []
		locilist = line[0].split("_")
		lista.append(locilist[0]+"_"+line[8]+"_"+line[9]+"_"+line[11]+"_"+line[12])
		blastdict[line[1]] = lista
		
print("\n\nGetting sequences\n\n")

tb=open(taxaname + "_table.Key", "w")
RCLIST=open(taxaname + "_RC.list", "w")
FL=open(taxaname + "_targetsFULL.fasta", "w")

with open(taxaname + "_targets.fasta", "w") as out:
	with open(taxaname+"_tmp/sl_rscaffolds.fasta") as GG:
		line=GG.readline()
		while line:
			if line[0] == ">":
				try:
					line = line.split()
					id = line[0].lstrip(">")
				except:
					id = line.strip().lstrip(">")
			if id in blastdict.keys():
				line=GG.readline()
				for info in blastdict[id]:
					#a loci b d (bit score) e(qframe)
					a, b, c, d, e= info.split("_")
					if a in locidict:
						locidict[a] += 1
					else:
						locidict[a] = 1
					b = int(b)
					c = int(c)
					e = int(e)
					
					if e < 0:
						RCLIST.write(a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"|"+id+"\n")
					
					if c > b:
						if b > flank:
							start_rec = b - 1 - flank
						else:
							start_rec = 0
						end_rec = c + flank
						out.write(">"+a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"\n")
						out.write(line[start_rec:end_rec].strip()+"\n")
						tb.write(id+"\t"+a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"\n")
						FL.write(">"+a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"|"+id+"\n"+line)
					
					elif b > c:
					#backwards coordinated given
						if c > flank:
							start_rec = c - 1 - flank
						else:
							start_rec = 0
						end_rec = b + flank
						out.write(">"+a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"\n")
#						out.write(line[start_rec:end_rec].strip()[::-1]+"\n")
						out.write(line[start_rec:end_rec].strip()+"\n")
						tb.write(id+"\t"+a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"\n")
						FL.write(">"+a+"_"+taxaname+"_comp"+str(locidict[a])+"_"+d+"|"+id+"\n"+line)
						
				line = GG.readline()
			else:
				line=GG.readline()
				line=GG.readline()	
tb.close()
FL.close()

#S9 Split loci into 4 fasta files for TBLASTX

print("\n\nTBLASTX of found Loci to GENOME for Ortholog filter\n\n")

seqcount=0
with open(taxaname + "_targets.fasta") as pf:
	for line in pf:
		if line.startswith(">"):
			seqcount+=1
print("Sequence number to test  for othology is "+str(seqcount)+" loci" )
seqdiv=seqcount/4

s1=open(taxaname+"_tmp/s1.fa", "w")
s2=open(taxaname+"_tmp/s2.fa", "w")
s3=open(taxaname+"_tmp/s3.fa", "w")
s4=open(taxaname+"_tmp/s4.fa", "w")

s1c=0
s2c=0
s3c=0
s4c=0
with open(taxaname + "_targets.fasta") as pf:
	for line in pf:
		if s1c <= seqdiv:
			if line.startswith(">"):
				s1.write(line)
			elif ">" not in line:
				s1.write(line)
				s1c+=1
		elif s1c > seqdiv and s2c <= seqdiv:
			if line.startswith(">"):
				s2.write(line)
			elif ">" not in line:
				s2.write(line)
				s2c+=1
		elif s1c > seqdiv and s2c > seqdiv and s3c <= seqdiv:
			if line.startswith(">"):
				s3.write(line)
			elif ">" not in line:
				s3.write(line)
				s3c+=1
		elif s1c > seqdiv and s2c > seqdiv and s3c > seqdiv and s4c <= seqdiv:
			if line.startswith(">"):
				s4.write(line)
			elif ">" not in line:
				s4.write(line)
				s4c+=1
s1.close()
s2.close()
s3.close()
s4.close()		

#S10 NCBI TBLASTX for Ortholog filter
def pbf(i):
	istr=str(i)
	print("Running TBLASTX LOCI subset_"+istr)
	os.system(rblast % (taxaname+"_tmp/s"+istr+".fa",genome+"_db",taxaname+"_tmp/preFass_"+istr+"_out",qthreads))
	print("LOCI subset_"+istr+" done")

def pbf_process(i):
	with multiprocessing.Pool() as pool:
		pool.map(pbf,i)

if __name__ == "__main__":
	i=[1,2,3,4]
	pbf_process(i)

#S11 join and filter to top hit using bit score of TBLASTX results
os.system(cat4 % (taxaname+"_tmp/preFass_1_out",taxaname+"_tmp/preFass_2_out",taxaname+"_tmp/preFass_3_out",taxaname+"_tmp/preFass_4_out", taxaname+"_tmp/preFass_out"))
os.system(filter2 % (taxaname+"_tmp/preFass_out", taxaname+"_tmp/Fass_out"))
#S12 JOIN top hit to 
os.system(joincat % (coordsprobeset,taxaname+"_tmp/Fass_out", taxaname+"_tmp/Ortho.in"))

#S13 Ortholog filter


print("\n\nNCBI TBLASTX for Ortholog filter Breinholt et al 2018\n\n")
outfile1 =open(taxaname + "_del_list.txt", "w")
outfile2 =open(taxaname + "_keep_list", "w")

hit=[]
loci=set([])
count=0
seqset=set([])
#open table and parse for scaford hit and coordinates of reference
with open(taxaname+"_tmp/Ortho.in", "r") as table:
	makein=table.readlines()
	for i in makein:
		loci.add(i.split("_",-1)[0])
		ALL_loci=list(loci)
table.close()


for x in ALL_loci:
	print("Processing " + x + " .............\n")
	with open(taxaname+"_tmp/Ortho.in", "r") as table2:
		makein2=table2.readlines()
		for i in makein2:
			taxa, scaf, id, length, mismatch, gaps, qs, qend, ts, tend, evalue, bit=i.split()
			if taxa.startswith(str(x) + "_"):
				if taxa == str(x) + "__" + refname + "_R":
					hit.append(scaf)
					print(taxa + " scaffold : " + scaf)
					leftcoord=int(ts)
					rightcoord=int(tend)
					if int(ts) < int(tend):
						direction= int(1)
					if int(ts) > int(tend):
						direction = int(0)
	table2.close()		


# open again as diffrent names to start at the top check to see if it hit scaf and coordinates
	with open(taxaname+"_tmp/Ortho.in", "r") as table3:
		makein3=table3.readlines()
		for i in makein3:
			taxa3, scaf3, id3, length3, mismatch3, gaps3, qs3, qend3, ts3, tend3, evalue3, bit3=i.split()
			seqset.add(taxa3)
			if int(ts3) < int(tend3):
				seqdirection= int(1)
			if int(ts3) > int(tend3):
				seqdirection = int(0)
#			print("seq direction(fwd=1, rev=0) : " + str(seqdirection))
			if taxa3.startswith(str(x) + "_"):
				if scaf3 not in hit:
					print("diffent scaffold " + taxa3 + " scaffold : " + scaf3)
					outfile1.write(taxa3 + "\n")
					count +=1
				if scaf3 in hit: 
					if direction == 1 and seqdirection == 1:
						if int(ts3) < rightcoord and int(tend3) > leftcoord:
							outfile2.write(taxa3 + "\n")
						else:
							outfile1.write(taxa3 + "\n")
							print("Same scaffold diffrent location Direction (ref fwd : seq fwd) " + str(direction) + ":"+ str(seqdirection))
							print(str(leftcoord) + " " + str(rightcoord) + "|" + i)
							count +=1
					
					if direction == 1 and seqdirection == 0:
						if int(tend3) < rightcoord and int(ts3) > leftcoord:
							outfile2.write(taxa3 + "\n")
						else:
							outfile1.write(taxa3 + "\n")
							print("Same scaffold diffrent location Direction(ref fwd: seq rev) " + str(direction) + ":"+ str(seqdirection))
							print(str(leftcoord) + " " + str(rightcoord) + "|" + i)
							count +=1					
					if direction == 0 and seqdirection == 0:
						if int(tend3) < leftcoord and int(ts3) > rightcoord:
							outfile2.write(taxa3 + "\n")
						else:
							outfile1.write(taxa3 + "\n")
							print("Same scaffold diffrent location Direction(ref rev: seq rev) " + str(direction) + ":"+ str(seqdirection))
							print(str(leftcoord) + " " + str(rightcoord) + "|" + i)
							count +=1
					if direction == 0 and seqdirection == 1:
						if int(ts3) < leftcoord and int(tend3) > rightcoord:
							outfile2.write(taxa3 + "\n")
						else:
							outfile1.write(taxa3 + "\n")
							print("Same scaffold diffrent location Direction(ref rev: seq fwds) " + str(direction) + ":"+ str(seqdirection))
							print(str(leftcoord) + " " + str(rightcoord) + "|" + i)
							count +=1


print("Ortholog filter results: "+str(count) + "/" + str(len(seqset)) + " (delete/total)")

table3.close()
outfile1.close()
outfile2.close()

#S21 Generating ortholog fasta files

print("\n\nGenerating ortholog fasta files\n\n")

os.system(fasta_filter % (taxaname+"_keep_list",taxaname+"_targets.fasta",taxaname+"_targets_ORTHO.fasta"))
os.system(fasta_filter % (taxaname+"_keep_list",taxaname+"_targetsFULL.fasta",taxaname+"_targetsFULL_ORTHO.fasta"))
os.system(key_filter % (taxaname+"_keep_list",taxaname+"_table.Key",taxaname+"_keep_list_ORTHO"))



#S22 CLean
print("\n\nclearing tmp files\n\n")
#os.system( kkill % (taxaname+"_tmp"))
os.system( kkill % ("$TMPDIR/ASS/"))

print("\n\n!!!!!Complete!!!!!\n\n")

sys.exit()
