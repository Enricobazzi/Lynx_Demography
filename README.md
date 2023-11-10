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

Full information can be found in the excel [table of all the samples](data/samples_table.xlsx).

Missing information:
- lp permit numbers
- lp tissues
- lc3, lc9999 location, tissue, permits
- lc permits
- lr5, lr6, lr7, lr8, lr9, lr10, lr18, lr19, lr21 tissues
- lr5, lr6, lr12, lr21 permits
- lr5, lr6, lr21 location

## Data Quality Control

### Run fastqc on raw reads
I run [fastqc](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) to check the quality of rawreads from sequencing. Scripts to be submitted to slurm queue in cesga ft3 were generated using the information contained in the [all_rawreads_fastqs configuration file](config/all_rawreads_fastqs.yml) with the [make_fastqc_scripts](scripts/make_fastqc_scripts.py) python script:
```
python scripts/make_fastqc_scripts.py config/all_rawreads_fastqs.yml
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
Then I can run [multiqc](https://multiqc.info/), [Ewels et al. (2016)](https://academic.oup.com/bioinformatics/article/32/19/3047/2196507) to check outputs:
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

Seeing the warnings I receive from fastqc reports I need to process the rawreads to try to remove them.

I use [fastp](https://github.com/OpenGene/fastp) from [Chen et al. (2018)](https://academic.oup.com/bioinformatics/article/34/17/i884/5093234?login=true) with default settings plus the following flags:
```
--dont_overwrite (protect the existing files not to be overwritten by fastp)
--trim_poly_g (detect the polyG in read tails and trim them)
--length_required 30 (reads shorter than length_required will be discarded)
--correction (enable base correction in overlapped regions)
--detect_adapter_for_pe (enable adapter sequence auto-detection)
--thread 6 (worker thread number)
```
Scripts that run fastp on each fastq pair separately were generated using the information contained in the [all_rawreads_fastqs configuration file](config/all_rawreads_fastqs.yml) with the [make_fastp_scripts](scripts/make_fastp_scripts.py) python script:
```
python scripts/make_fastp_scripts.py config/all_rawreads_fastqs.yml
```
The generated scripts were then submitted to the job queue on cesga ft3:
```
# sbatch ll samples:
for sh in $(ls scripts/fastp/*.sh | grep "_ll_")
 do
  echo "sbatch $sh"
  sbatch $sh
done

# sbatch lc and lr samples:
for sh in $(ls scripts/fastp/*.sh | grep -E "_lc_|_lr_")
 do
  echo "sbatch $sh"
  sbatch $sh
done
```

### Run fastqc on fastp trimmed reads

To check on how the fastp run went I run fastqc on the newly generated fastq pairs from fastp. This time I use a different [configuration file with the fastp folders and fastq files](config/all_fastp_fastqs.yml) using the [make_fastqc_scripts](scripts/make_fastqc_scripts.py) python script again:
```
python scripts/make_fastqc_scripts.py config/all_fastp_fastqs.yml
```
The generated scripts were then submitted to the job queue on cesga ft3:
```
# sbatch ll samples:
for sh in $(ls scripts/fastqc/*.sh | grep "_ll_")
 do
  echo "sbatch $sh"
  sbatch $sh
done

# sbatch lc and lr samples:
for sh in $(ls scripts/fastqc/*.sh | grep -E "_lc_|_lr_")
 do
  echo "sbatch $sh"
  sbatch $sh
done
```
Then I can run multiqc to check outputs:
```
module load cesga/2020 multiqc/1.14-python-3.9.9

cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LYNX_24/20200405/FASTQ/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LYNX_20/FASTQ/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LYNX_21/FASTQ/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LRU_30/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/MAGROGEN/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/Canada_data_CandadaLynxes/share/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/Bobcat1/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/USA_data_Bobcats/fastp/fastqc
multiqc .
cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/lynx_genome/lynx_data/FASTQ_files/LCA_3/fastp/fastqc
multiqc .
```

It seems that the only samples that after fastp could still be problematic are:
- c_lc_yu_0007, c_lr_vt_0014, c_lr_vt_0020 -> very odd Per Seqeunce GC Content

## Run alignments

I align the my samples to the [Lynx rufus reference genome](https://denovo.cnag.cat/lynx_rufus).

A script will be run for each sample that will use [bwa v0.7.17](https://bio-bwa.sourceforge.net/bwa.shtml), [samtools v1.9](https://www.htslib.org/doc/samtools.html), [picard v2.25.5](https://broadinstitute.github.io/picard/) and [gatk v3.7-0](https://gatk.broadinstitute.org/hc/en-us) that will do the following:
- Align each of the sample's R1-R2 fastq pairs to the reference genome using BWA-MEM and Samtools view
- samtools sort to sort the reads in the bam file
- picardtools AddOrReplaceReadGroups to add read groups to the reads in the bam file
- samtools merge to merge the bam files from the multiple R1-R2 pairs of the sample if necessary
- picardtools MarkDuplicates to mark duplicate reads in the bam
- realign indels with GATK which comprises:
    - gatk RealignerTargetCreator to identify realign targets
    - gatk IndelRealigner to realign the indels
- samtools index to index the indel realigned bam for downstream analyses

Scripts that will run the alignment pipeline [for each sample](scripts/print_samples_in_config.py) in the [alignment configuration file](config/all_fastp_alignment.yml) are generated using the [run_alignment](src/congenomics_fastq_align-main/run_alignment.py) python script with the flag `--test`:
```
cd scripts/alignment

for sample in $(python ../../scripts/print_samples_in_config.py ../../config/all_fastp_alignment.yml)
 do
  echo "generating alignment script of $sample"
  python ../../src/congenomics_fastq_align-main/run_alignment.py --sample $sample --config ../../config/all_fastp_alignment.yml --test
done
```
To prepare the reference genome for the alignment I run:
```
module load cesga/2020 gcccore/system 
module load bwa/0.7.17
module load samtools/1.9
module load gatk/3.7-0-gcfedb67

cd /mnt/lustre/hsm/nlsas/notape/home/csic/ebd/jgl/reference_genomes/lynx_rufus_mLynRuf2.2/

samtools faidx mLynRuf2.2.revcomp.scaffolds.fa
bwa index mLynRuf2.2.revcomp.scaffolds.fa
java -jar ${EBROOTGATK}/GenomeAnalysisTK.jar -T CreateSequenceDictionary -R mLynRuf2.2.revcomp.scaffolds.fa
```
The generated scripts were then submitted to the job queue on cesga ft3:
```
# sbatch all except lr
for sh in $(ls scripts/alignment/*.sh | grep -v "lr")
 do
  echo "sbatching $sh"
  sbatch $sh
done
```

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