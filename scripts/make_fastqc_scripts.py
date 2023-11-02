import argparse
import yaml
import os

'''
This script generates bash scripts for running FastQC on multiple sets of paired-end reads.

Usage:
python make_fastqc_scripts.py <path/to/config_file.yaml>

The config file should be a YAML file with the following structure:
 - The 'sample_dict' key should be a dictionary of dictionaries.
   - The first level of keys should be the sample names.
     - The second level of keys should be the fastq pair names.
     - The values for the second level of keys should be a list of three strings:
       the path to the folder containing the fastq files, the name of the first fastq file, 
       and the name of the second fastq file

Here's an example of what the YAML file should look like:
sample_dict:
  sample1:
    fastq_pair_1:
      ['path/to/pair1', 'pair1_r1.fastq.gz', 'pair1_r2.fastq.gz']
    fastq_pair_2:
      ['path/to/pair2', 'pair2_r1.fastq.gz', 'pair2_r2.fastq.gz']
  sample2:
    fastq_pair_1:
      ['path/to/pair3', 'pair3_r1.fastq.gz', 'pair3_r2.fastq.gz']

The script will generate a bash script for each fastq pair in the sample_dict.
Here's an example of the bash script that would be generated for sample1, fastq_pair_1:

#!/bin/bash
#SBATCH --job-name=sample1_fastq_pair_1
#SBATCH --output=logs/fastqc/sample1_fastq_pair_1.out
#SBATCH --error=logs/fastqc/sample1_fastq_pair_1.err
#SBATCH --time=3:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=6

module load cesga/2020 fastqc/0.11.9

fastqc -o path/to/pair1/fastqc -t 6 path/to/pair1/pair1_r1.fastq.gz path/to/pair1/pair1_r2.fastq.gz
'''

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('config_file', help='Path to YAML config file')
args = parser.parse_args()

# Load the YAML file
with open(args.config_file, 'r') as f:
    data = yaml.safe_load(f)

# Loop through each sample in the YAML file
for sample in data['sample_dict']:
    # Loop through each fastq pair for the sample
    for fastq_pair in data['sample_dict'][sample]:
        # Get the containing folder and fastq file names
        containing_folder = data['sample_dict'][sample][fastq_pair][0]
        fastq_r1 = os.path.join(containing_folder, data['sample_dict'][sample][fastq_pair][1])
        fastq_r2 = os.path.join(containing_folder, data['sample_dict'][sample][fastq_pair][2])
        
        # Generate the fastqc command
        command = f'fastqc -o {os.path.join(containing_folder, "fastqc")} -t 6 {fastq_r1} {fastq_r2}'
        
        # Generate the bash script
        script = f'''\
#!/bin/bash
#SBATCH --job-name={sample}_{fastq_pair}
#SBATCH --output=logs/fastqc/{sample}_{fastq_pair}.out
#SBATCH --error=logs/fastqc/{sample}_{fastq_pair}.err
#SBATCH --time=3:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=6

module load cesga/2020 fastqc/0.11.9

{command}
'''
        
        # Write the bash script to a file
        script_file = f'scripts/fastqc/{sample}_{fastq_pair}.sh'
        with open(script_file, 'w') as f:
            f.write(script)
