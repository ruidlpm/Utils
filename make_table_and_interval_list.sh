#!/bin/bash

#this script makes a .table and .interval_list for using with GATK
#Usage:
#	./make_table_and_interval_list.sh <dataset.bim>
#
#date:31/08/2015
#author: Rui Martiniano

dataset=$1
outprefix=$(echo $dataset| cut -f1 -d.)

#1 - Make table

#table format is:
#HEADER	POS	RSid	Alleles
#chr1:752566-752566	rs3094315	G:A
#chr1:768448-768448	rs12562034	A:G
#chr1:1030565-1030565	rs6687776	T:C

echo "HEADER POS RSid Alleles" | tr ' ' '\t' > $outprefix.table
cat $dataset | awk '{print "chr"$1":"$4"-"$4" "$2" "$5":"$6}' | tr ' ' '\t' >> $outprefix.table

#1 - Make table

#Format is:
#chr2:78906926-78906926
#chr2:78914837-78914837
#chr2:78927328-78927328

cat $dataset | awk '{print "chr"$1":"$4"-"$4}' > $outprefix.interval_list
