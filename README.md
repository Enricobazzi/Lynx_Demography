# Reconstructing the evolutionary history of Lynx species

## Selecting Samples

I will generate GVCFs of following samples:

 - 10 new Lynx pardinus - sierra morena : 211, 220, 225, 239, 278, 377, 390, 452, 474, 614
 - 5 Lynx lynx - east : 112, 114, 137, 141, 146
 - 5 Lynx lynx - west : 45, 90, 202, 211, 212
 - 3 Lynx lynx - lesser caucasus : 240, 242, 247
 - 5 Lynx lynx - dagestan : 241 (high ROH!), 243, 244, 259, 260
 - All (20) Lynx canadensis : 3 and 12 are differentiated in PC1 and PC2 respectively and 7 is shit
 - All (18) Lynx rufus (11 is a canada lynx)

*Build samples table*

## Data Quality Control

### Run fastqc on raw reads
Scripts to be submitted to slurm queue in cesga ft3 were generated using the information contained in the [all_rawreads_fastqc configuration file](config/all_rawreads_fastqc.yml) with the [make_fastqc_scripts](scripts/make_fastqc_scripts.py) python script:
```
python scripts/make_fastqc_scripts.py config/all_rawreads_fastqc.yml
```
The generated scripts were then submitted to the job queue on cesga ft3:
```
# sbatch ll samples:
for sh in $(ls scripts/rawreads_fastqc/*.sh | grep "_ll_")
 do
  echo "sbatch $sh"
  sbatch $sh
done

# sbatch lc and lr samples:
for sh in $(ls scripts/rawreads_fastqc/*.sh | grep -E "_lc_|_lr_")
 do
  echo "sbatch $sh"
  sbatch $sh
done
```
Then I can run multiqc to check outputs:
```
module load cesga/2020 multiqc/1.14-python-3.9.9

multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LYNX_24/20200405/FASTQ/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LYNX_20/FASTQ/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LYNX_21/FASTQ/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LRU_30/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/MAGROGEN/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/Canada_data_CandadaLynxes/share/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/Bobcat1/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/USA_data_Bobcats/fastqc
multiqc /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LCA_3/fastqc
```
Analyzing fastqc and multiqc reports we see that

LYNX_20, LYNX_21, LYNX_24 have very-low to fail levels of:
- Illumina universal adapter content
- Poly-G sequences

Bobcat1 have warning levels of:
- Nextera transposase adapters

Canada_data_CandadaLynxes have very-low to warning levels of:
- Illumina universal adapter content
- Poly-G sequences
and one failed GC-content

MAGROGEN LL212 has warnings for:
- Overrepresented TruSeq Adapter (ATCGGAAGAGCACACGTCTGAACTCCAGTCACGAATTCGTATCTCGTATG)
- Overrepresented Illumina Single End PCR Primer 1 (ATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTGCCTCTATGTGTAGATCTC)

USA_data_Bobcats have very-low to warning levels of:
- Nextera transposase adapters
- Poly-G sequences

### Run fastp on raw reads

### Run fastqc on fastp trimmed reads
### Run multiqc to check outputs

## two
Run alignment

## three
Run variant calling

## four
Filter variants

## five
Identify windows

## six
Run lynx_ea_abc - invasive weed

## seven
Run simulations of best models

## eight
Run ABC