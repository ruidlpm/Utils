#!/usr/bin/python
# 
# filter_vcf_deamination.py
# version: 1.1
# Removes potential deamination from vcf file
# optional arguments:
#   -h, --help     show this help message and exit
#   -i VCF_INPUT
#   -o VCF_OUTPUT
# usage: filter_vcf_deamination.py [-h] [-i VCF_INPUT] [-o VCF_OUTPUT]
# 
# Date: 12/11/2015 
# Author: Rui Martiniano
#
# Note: included test
# run this:
# python filter_vcf_deamination.py -i test.vcf -o test_out.vcf

from __future__ import print_function
import argparse
import sys
import time



parser = argparse.ArgumentParser(description="Removes potential deamination from vcf file")

#add options to argparser
parser.add_argument('-i', action="store", dest="vcf_input", type=str)
parser.add_argument('-o', action="store", dest="vcf_output", type=str)

#test parameters
try:
    options=parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

vcf_input=options.vcf_input
vcf_output=options.vcf_output

outfile=open(vcf_output,'w')



def parser(i):
	"""
	Removes potential deamination from vcf file
	takes a snp (or line) in vcf file and when encountering
	potential deamination, replaces its genotype with './.'
	(missing).
	"""
	changed_snps=0
	if (i[3]=='C' and i[4]=='T'):
		newline=[]
		for item in i:
			if (item.startswith('0/1') or item.startswith('1/1')):
				changed_item=item.replace(item, './.')
				newline.append(changed_item)
				changed_snps += 1
			else:
				newline.append(item)
		# print(changed_snps)
		return(newline)
	elif (i[3]=='G' and i[4]=='A'):
		newline=[]
		for item in i:
			if (item.startswith('0/1') or item.startswith('1/1')):
				changed_item=item.replace(item, './.')
				newline.append(changed_item)
				changed_snps += 1
			else:
				newline.append(item)
		# print(changed_snps)
		return(newline)
	elif (i[3]=='T' and i[4]=='C'):
		newline=[]
		for item in i:
			if (item.startswith('0/1') or item.startswith('0/0')):
				changed_item=item.replace(item, './.')
				newline.append(changed_item)
				changed_snps += 1
			else:
				newline.append(item)
		# print(changed_snps)
		return(newline)
	elif (i[3]=='A' and i[4]=='G'):
		newline=[]
		for item in i:
			if (item.startswith('0/1') or item.startswith('0/0')):
				changed_item=item.replace(item, './.')
				newline.append(changed_item)
				changed_snps += 1
			else:
				newline.append(item)
		# print(changed_snps)
		return(newline)
	else: #if none of the above, just return the unchanged line
		return(i)



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
			#process snp lines with the parser function
			snp=line.strip('\n').split("\t")
			outfile.write('\t'.join(parser(snp)) + '\n')

			sys.stdout.write("SNPs processed: %d   \r" % (counter) )
			sys.stdout.flush()
outfile.close()

end = time.time()
elapsed = end - start

print("\n" + str(round(elapsed,2)) + " sec.")
