"""
In this script I want to parse the config file and check if all the files are present in the directory they are supposed to be.

The config file is a yaml file with the following structure:
sample_dict:
  sample1:
    fastq_pair_1:
      ['path/to/pair1', 'pair1_r1.fastq.gz', 'pair1_r2.fastq.gz']
    fastq_pair_2:
      ['path/to/pair2', 'pair2_r1.fastq.gz', 'pair2_r2.fastq.gz']
    sample2:
      fastq_pair_1:
        ['path/to/pair3', 'pair3_r1.fastq.gz', 'pair3_r2.fastq.gz']

This script will print out the files that are not present in the directory they are supposed to be.
"""
import os
import sys
import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='Path to YAML config file')
    return parser.parse_args()

def main():
    # Load the YAML file
    args = parse_args()
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
            # Check if the files are present
            if not os.path.isdir(containing_folder):
                print(f'{containing_folder} does not exist')
            else:
                if not os.path.isfile(fastq_r1):
                    print(f'{fastq_r1} is not present in {containing_folder}')
                if not os.path.isfile(fastq_r2):
                    print(f'{fastq_r2} is not present in {containing_folder}')
    
if __name__ == '__main__':
    main()
