#!/bin/python

import argparse
import sys

parser = argparse.ArgumentParser(description="converts biallelic haploid vcf to fasta")
parser.add_argument('-i', action="store", dest="input_vcf", type=str)
parser.add_argument('-o', action="store", dest="output_fasta", type=str)

try:
    options=parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

if options.input_vcf is None or options.output_fasta is None:
    raise Exception('please provide input and output files')


vcf=options.input_vcf
out_fasta=options.output_fasta


def get_vcf_header(vcf):
    '''reads VCF until it finds the header line and returns it'''
    with open(vcf, 'r') as f:
        vcf_header=[]
        for line in f:
            if line.startswith('#CHROM'):
                vcf_header=line.strip().split()
                break

    if len(vcf_header)>0:
        return(vcf_header)
    else:
        raise Exception("VCF has no header")


def make_ind_dict(ind_list):
    '''keeps an index of the individuals present in the VCF file'''
    counter=8
    ind_dict={}
    for ind in ind_list:
        counter=counter+1
        ind_dict[str(ind)]=int(counter)
    return ind_dict


def get_bases_from_ind(vcf_row, indiv_index):
    '''converts the genotype to the corresponding allele'''
    base=''    
    REF=vcf_row[3]
    ALT=vcf_row[4]
    geno=str(vcf_row[indiv_index])

    
    if len(str(REF))==1 and len(str(ALT))==1:
        if len(str(geno))>1:
            raise Exception("this program only handles haploid VCFs")
        else:
            if geno=='0':
                base=REF
            elif geno=='1':
                base=ALT
            elif geno=='.' or geno=='N':
                base='N'
            else:
                base='N'
                print('fix ' + geno)
    else:
        pass
    return(base)


open(out_fasta, 'w').close()

nucleotides=['A','T','C','G','N']

vcf_header=get_vcf_header(vcf)

inds=vcf_header[9:]

ind_dict=make_ind_dict(inds)

for ind in inds:
    print(ind)
    with open(vcf, 'r') as f:
        sequence=''
        for line in f:
            if not line.startswith('#'):
                line=line.strip().split()
                sequence+=get_bases_from_ind(line, ind_dict[ind])
        with open(out_fasta, 'a') as out:
            out.write('>' + ind + '\n')
            out.write(sequence + '\n')


