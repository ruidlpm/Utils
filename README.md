#Utils

###Scripts for processing vcf or pileup files

 - **vcf2fasta.py** - *converts vcf to fasta*
 
```
Usage:
vcf2fasta.py [-h] [-i INPUT_VCF] [-o OUTPUT_FASTA]
```




 - **make_table_and_interval_list.sh** - *makes GATK .table and .interval_list files from .bim file*
 
```
Usage:
./make_table_and_interval_list.sh <dataset.bim>

Example:
./make_table_and_interval_list.sh 1KG.bim 

```
 

  
 - **run_pileup.py** - *Takes indexed bam files, runs GATK's pileup*
```
Usage:
./run_pileup.sh <bam.list> <interval_list> <table> <output_folder>

Example:
./run_pileup.sh bam.list 1KG.interval_list 1KG.table
```



- **pileup2plink.py** - *Filters input file (pileup format) and converts it to plink format files (ped and map)*

```
Usage:
pileup2plink.py [-h] [-i PILEUP_FILE] [-d BIMFILE] [-q QUALITY] [-o OUTPREFIX]

Example:
pileup2plink -i in.pileup -d genotype_dataset -q 30 -o out

```



- **filter_vcf_deamination.py** - *Removes potential deamination from vcf file*
```
Usage:

filter_vcf_deamination.py [-h] [-i VCF_INPUT] [-o VCF_OUTPUT]

Example:
python filter_vcf_deamination.py -i test.vcf -o test_out.vcf

```



- **filter_vcf_GP.py** - *Filters VCF by Genotype probability threshold*
```
Usage:
filter_vcf_GP.py [-h] [-i VCF_INPUT] [-o VCF_OUTPUT] [-t GENOTYPE_PROBABILITY_THRESHOLD]

Example:
python filter_vcf_GP.py -i chr1.1.out.vcf -o test.out -t 0.90

```
