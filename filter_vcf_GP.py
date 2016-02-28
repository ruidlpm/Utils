#!/bin/python
#
# Rui Martiniano 12/2015
#
# filter_vcf_GP.py - Filters VCF according to specified Genotype probability threshold
# usage:
# filter_vcf_GP.py [-h] [-i VCF_INPUT] [-o VCF_OUTPUT] [-t GENOTYPE_PROBABILITY_THRESHOLD]
# #example usage
# python filter_vcf_GP.py -i chr1.1.out.vcf -o test.out -t 0.90


from __future__ import print_function
import argparse
import sys
import time

parser = argparse.ArgumentParser(description="Filters phased genotypes with genotype probability lower than the threshold provided. It also replaces triallelic genotypes with ./. ")


#add options to argparser
parser.add_argument('-i', action="store", dest="vcf_input", type=str)
parser.add_argument('-o', action="store", dest="vcf_output", type=str)
parser.add_argument('-t', action="store", dest="genotype_probability_threshold", type=float)


#test parameters
try:
    options=parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

vcf_input=options.vcf_input
vcf_output=options.vcf_output
threshold=options.genotype_probability_threshold
outfile=open(vcf_output,'w')



def genotype_prob_parser(snp, threshold):
	"""
	Filters genotypes with genotype probability lower than the threshold provided.
	"""
	changed_snps=0
	snps2=0
	empty_individual_snp="./."
	new_snp=[]
	for individual_snp in snp:
		#is it a phased genotype?
		if "|" not in individual_snp:
			new_snp.append(individual_snp)
		#if it is a phased genotype
		#if homoz reference
		elif (individual_snp.split(":")[0].startswith("0|0")):
			if (float(individual_snp.split(":")[2].split(",")[0]))>= threshold:
				new_snp.append(individual_snp)
			else:
				new_snp.append(empty_individual_snp)
				changed_snps += 1
		#if heterozygous
		elif (individual_snp.split(":")[0].startswith("0|1")):
			if (float(individual_snp.split(":")[2].split(",")[1]))>= threshold:
				new_snp.append(individual_snp)
			else:
				new_snp.append(empty_individual_snp)
				changed_snps += 1
		#if heterozygous
		elif (individual_snp.split(":")[0].startswith("1|0")):
			if (float(individual_snp.split(":")[2].split(",")[1]))>= threshold:
				new_snp.append(individual_snp)
			else:
				new_snp.append(empty_individual_snp)
				changed_snps += 1
		#if homoz alternative allele
		elif (individual_snp.split(":")[0].startswith("1|1")):
			if (float(individual_snp.split(":")[2].split(",")[2]))>= threshold:
				new_snp.append(individual_snp)
			else:
				new_snp.append(empty_individual_snp)
				changed_snps += 1
		#exclude triallelic snps2
		else:
			new_snp.append(empty_individual_snp)
	return(new_snp)



start = time.time()


#iterate through each line
counter=0
initial_vcf=[]
header=[]
with open(vcf_input,'r') as f:
	for line in f:
		#get header lines
		if line.startswith('#'):
			headline=line.strip('\n').split("\t")
			header.append(headline)
			outfile.write('\t'.join(headline) + '\n')
		else:
			counter += 1
			#process snp lines with the genotype_prob_parser function
			snp=line.strip('\n').split("\t")
			outfile.write('\t'.join(genotype_prob_parser(snp,threshold)) + '\n')
			sys.stdout.write("SNPs processed: %d   \r" % (counter) )
			sys.stdout.flush()



outfile.close()

end = time.time()
elapsed = end - start

print("\n" + str(round(elapsed,2)) + " sec.")
