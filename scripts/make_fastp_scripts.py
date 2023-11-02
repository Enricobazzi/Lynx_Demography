import argparse
import yaml
import os
import textwrap

'''
This script generates bash scripts for running fastp on multiple sets of paired-end reads.

Usage:
python make_fastp_scripts.py <path/to/config_file.yaml>

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
#SBATCH --output=logs/fastp/sample1_fastq_pair_1.out
#SBATCH --error=logs/fastp/sample1_fastq_pair_1.err
#SBATCH --time=4:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=6

module load cesga/2020 gcccore/system fastp/0.22.0

fastp \
-i path/to/pair1/pair1_r1.fastq.gz -I path/to/pair1/pair1_r2.fastq.gz \
-o path/to/pair1/fastp/pair1_r1.fastp.fastq.gz -O path/to/pair1/fastp/pair1_r2.fastp.fastq.gz \
-h path/to/pair1/fastp/pair1_fastp.html -j path/to/pair1/fastp/pair1_fastp.json \
--unpaired1 path/to/pair1/fastp/pair1_unpaired.fastq.gz --unpaired2 path/to/pair1/fastp/pair1_unpaired.fastq.gz \
--failed_out path/to/pair1/fastp/pair1_failed.fastq.gz \
--dont_overwrite \
--trim_poly_g \
--length_required 30 \
--correction \
--detect_adapter_for_pe \
--thread 6

'''
# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('config_file', help='Path to YAML config file')
args = parser.parse_args()

# Create the output directories if they don't exist
os.makedirs('scripts/fastp', exist_ok=True)
os.makedirs('logs/fastp', exist_ok=True)

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
        
        # define the fastp output file names and create the output folder
        fastp_folder = os.path.join(containing_folder, 'fastp')
        # r1 and r2 fastp output files
        fastp_r1 = data['sample_dict'][sample][fastq_pair][1].replace('.fastq.gz', '.fastp.fastq.gz').replace('.fq.gz', '.fastp.fastq.gz')
        fastp_r2 = data['sample_dict'][sample][fastq_pair][2].replace('.fastq.gz', '.fastp.fastq.gz').replace('.fq.gz', '.fastp.fastq.gz')
        fastp_r1_out = os.path.join(fastp_folder, fastp_r1)
        fastp_r2_out = os.path.join(fastp_folder, fastp_r2)

        # fastp json and html output files
        fastp_html = f'{fastq_pair}_fastp.html'
        fastp_html_out = os.path.join(fastp_folder, fastp_html)
        fastp_json = f'{fastq_pair}_fastp.json'
        fastp_json_out = os.path.join(fastp_folder, fastp_json)
        
        # unpaired and failed output files
        unpaired = f'{fastq_pair}_unpaired.fastq.gz'
        unpaired_out = os.path.join(fastp_folder, unpaired)
        failed = f'{fastq_pair}_failed.fastq.gz'
        failed_out = os.path.join(fastp_folder, failed)

        # Generate the fastp command
        command = textwrap.dedent(
        f'''\
            fastp \
            -i {fastq_r1} -I {fastq_r2} \
            -o {fastp_r1_out} -O {fastp_r2_out} \
            -h {fastp_html_out} -j {fastp_json_out} \
            --unpaired1 {unpaired_out} --unpaired2 {unpaired_out} \
            --failed_out {failed_out} \
            --dont_overwrite \
            --trim_poly_g \
            --length_required 30 \
            --correction \
            --detect_adapter_for_pe \
            --thread 6
        '''
        )
        # Replace multiple spaces with a single space
        command = ' '.join(command.split())

        # Generate the bash script
        script = textwrap.dedent(
        f'''\
            #!/bin/bash
            #SBATCH --job-name={sample}_{fastq_pair}
            #SBATCH --output=logs/fastp/{sample}_{fastq_pair}.out
            #SBATCH --error=logs/fastp/{sample}_{fastq_pair}.err
            #SBATCH --time=4:00:00
            #SBATCH --mem=4G
            #SBATCH --cpus-per-task=6

            module load cesga/2020 gcccore/system fastp/0.22.0

            {command}
        '''
        )

        # Write the bash script to a file
        with open(f'scripts/fastp/{sample}_{fastq_pair}_fastp.sh', 'w') as f:
            f.write(script)
