import yaml
import argparse

'''
This script reads a YAML configuration file and prints the unique folder names
contained in the file. The path to the YAML file is passed as a command-line argument.
'''

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('config_file', help='Path to YAML config file')
args = parser.parse_args()

# Load the YAML file
with open(args.config_file, 'r') as f:
    data = yaml.safe_load(f)

# Create a set to store unique folder names
folders = set()

# Loop through each sample in the YAML file
for sample in data['sample_dict']:
    # Loop through each fastq pair for the sample
    for fastq_pair in data['sample_dict'][sample]:
        # Get the containing folder and add it to the set
        folders.add(data['sample_dict'][sample][fastq_pair][0])

# Print all unique folder names
for folder in folders:
    print(folder)