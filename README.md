#Utils

###Scripts for processing vcf or pileup files


Rui Martiniano (2016)


 - **make_table_and_interval_list.sh** - *makes GATK .table and .interval_list files from .bim file*
 
```
Usage:
./make_table_and_interval_list.sh <dataset.bim>

Example:
./make_table_and_interval_list.sh ire_brit_nl_filt.bim 

```
 
  
 - **run_pileup.py** - *Takes indexed bam files, runs GATK's pileup*
```
Usage:
./run_pileup.sh <bam.list> <interval_list> <table> <output_folder>

Example:
./run_pileup.sh bam.list ~/Hellenthal_dataset/Hellenthal_b37.interval_list \
/home/rui//Hellenthal_dataset/hellenthal.table
```



- **pileup2plink.py** - *Filters input file (pileup format) and converts it to plink format files (ped and map)*

```
Usage:
pileup2plink.py [-h] [-i PILEUP_FILE] [-d BIMFILE] [-q QUALITY] [-o OUTPREFIX]

Example:
pileup2plink -i in.pileup -d genotype_dataset -q 30 -o out

```

