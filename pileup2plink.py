#!/bin/python2.7

import argparse
import sys
import getopt
import random
import re
import time


"""
Author: Rui Martiniano
Date:25/08/2015
Description: converts GATK pileup to plink format

usage: pileup2plink.py [-i] <input.GATK.pileup> [-d] <dataset.bim> [-q] <quality> [-o] <prefix> [-h]

Filters input file (pileup format) and converts it to plink format files (ped and map)

input: 
1) pileup file for individual sample
2) bim file of desired dataset

filtration criteria:
1) checks if alleles are present in bimfile
2) checks if base qual is >= <qual>

output:
homozygous ped and map files




Note:

can be used as:
ls *rescaled.pileup | cut -f1 -d'.' | while read i; do python pileup2plink.py -i $i.rescaled.pileup -d /home/rui/Hellenthal_dataset/Hellenthal_b37.bim -q 30 -o $i & done
takes 5 sec. each file.
"""


parser = argparse.ArgumentParser(description='Converts pileup format files into homozygous plink format files for an individual sample.')

#add options to argparser
parser.add_argument('-i', action="store", dest="pileup_file", type=str)
parser.add_argument('-d', action="store", dest="bimfile", type=str)
parser.add_argument('-q', action="store", dest="quality", type=int)
parser.add_argument('-o', action="store", dest="outprefix", type=str)

#test parameters
try:
    options=parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

#parameters
args=options
pileup_file=options.pileup_file
bimfile=options.bimfile
outprefix=options.outprefix
quality=options.quality
outped=outprefix + '.final.ped'
outmap=outprefix + '.final.map'
triallelic_snps_outfile=outprefix + '.txt'
sample_name=outprefix


#read pileup into list
pileup = []
with open(pileup_file) as f:
    for line in f:
        #replace specific characters. [:-1] is used to remove last "]"
        l1=[line.replace('\t', ' ').replace("[ROD",'').strip('\n')[:-1].split(' ') for line in f]
        for unfilt in l1:
            #remove emtpy str
            str_list = filter(None, unfilt)
            pileup.append(str_list)


#filter pileup
def filter_pileup(pileup, quality):
    """
    filters pileup by removing:
        1) triallelic snps
        2) low quality bases
    returns filtered pileup  
    """
    triallelic_snps=set()
    #for each snp/line in pileup
    filtered_pileup=[]
    for snp in pileup[:-1]:
        #for each called base
        #check if not triallelic
        base_to_keep=[]
        for base in range(len(snp[3])):
            #check if if bases match colums 9 (known alleles, this means SNPs are not triallelic)
            if snp[3][base] not in snp[9]:
                #if triallelic, append rsID to triallelic_snps
                triallelic_snps.add(snp[8])
            else:
                #filter by quality
                if (ord(snp[4][base])-33) >= quality:
                    base_to_keep.append(snp[3][base])
                else:
                    pass
        if len(base_to_keep) > 0:
            filtered_snp = (snp[0], snp[1] , base_to_keep,snp[8])
            filtered_pileup.append(filtered_snp)
        else:
            pass
    return(filtered_pileup)

#run filter_pileup
filtered_pileup= filter_pileup(pileup,quality)

#calc number of removed SNPs
removed_snps = len(pileup) - len(filtered_pileup)
print("Sample " + sample_name + ": removed " + str(removed_snps) + " of " + str(len(pileup)) + " = " + str(len(filtered_pileup)) + " SNPs")


#make ped file
def make_ped(filtered_pileup):
    """
    input is filtered pileup, output is list of homozygous alleles
    """
    homoz_alleles=[]
    for snp in filtered_pileup:
        allele = random.choice(snp[2])
        alleles = str(allele + ' ' + allele)
        homoz_alleles.append(alleles)
    return homoz_alleles

#get homozygous alleles
ped=make_ped(filtered_pileup)

#make header
header=sample_name + ' ' + sample_name + ' 0 0 0 1 '

#write ped file
with open(outped,'w') as out:
    out.write(header)
    for line in ped:
        strs="".join(str(x) for x in line)
        out.write(strs + ' ')



#read in bim file
bim = []
with open(bimfile, 'r') as f:
    for snp_line in f:
        lin=snp_line.rstrip("\n").split('\t')
        bim.append(lin)

#convert to dict having rsID as key
d = {r[1] : r[0:4] for r in bim}

def make_map(filtered_pileup):
    """
    gets rsID from filtered pileup and outputs map file
    """
    maplist=[]
    for snp in filtered_pileup:
        maplist.append(d[snp[3]])
    return maplist

#make map file
mapfile = make_map(filtered_pileup)

#write map file
with open(outmap, 'w') as file:
    file.writelines('\t'.join(i) + '\n' for i in mapfile)
    file.writelines('\n')
