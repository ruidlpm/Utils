#!/bin/bash
#############################################################
# Name:run_pileup.sh
# Version: 1.1
# Date:26/08/2015
# Author: Rui Martiniano
# Usage:
#	./run_pileup.sh <bam.list> <interval_list> <table> <out_folder>
#
#	where <bam.list> contains the name of bam files,
#	<interval_list> points to SNPs to be called and 
#	<table> to the table file which contains more info
#	about the markers.
#
# Function: 
#	takes indexed bam files, runs GATK's pileup
#
#	input: *bam
#   output: *.pileup
#
# Notes:
#	requires GATK and bam.list
#
#	bam list can be made by:
# for fastq_name in $(ls *.trimmed.fastq | cut -d'.' -f1);  do ls $fastq_name/bam_files_$fastq_name/$fastq_name.rescaled.1.bam; done | cut -f1 -d/ > bam.list
#
##############################################################

#get args
bam_list=$1
interval_list=$2
table=$3
out_folder=$4

#iterate through file list and run pileup
cat $bam_list | while read sample; do
  java -jar /home/rui/Rui/software/GenomeAnalysisTK-2.5-2-gf57256b/GenomeAnalysisTK.jar \
  -T Pileup \
  -I $sample/bam_files_$sample/$sample.rescaled.1.bam \
  -R ~/Rui/resources/hg19_clean_noM.fa \
  -o $out_folder/$sample.rescaled.pileup \
  -L  $interval_list \
  -nt 20 \
  --metadata:table $table
 done

