#Author: Michael Elgin
#This file will split commands created from the output of multi-train.py
#For example: if you have created a file from running something like:
#	python multi-train.py nerfacto --data_path /home2/grocery/data/normal/100percent/ungrouped/ --results_path /home2/grocery/results/nerfbaselines-grocery/nerfacto_4/ > nerfacto_4_commands.sh
#Then this file can take nerfacto_4_commands.sh and split it into n chunks for n gpus
#This will then allow setting each split to its own gpu:
#	CUDA_VISIBLE_DEVICES=[0|1|2...] nohup ./nerfacto_4_commands_split[0|1|2...].sh > /home2/grocery/logs/nerfbaselines-grocery/nerfacto_4_split[0|1|2...].log &

import argparse
import os

def split_list(lst, n):
    length = len(lst)
    result = []
    for i in range(n):
        start = i * length // n
        end = (i + 1) * length // n
        result.append(lst[start:end])
    return result

def main():
    parser = argparse.ArgumentParser(description='Split commands in a .sh file into n chunks.')
    parser.add_argument('-n', type=int, required=True, help='Number of splits (GPUs)')
    parser.add_argument('--file', type=str, required=True, help='Path to the .sh file to split')
    args = parser.parse_args()

    num_splits = args.n
    input_file = args.file

    #Read input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    #Separate header and commands
    header_lines = []
    command_lines = []

    for line in lines:
        if line.strip().startswith('#'):
            header_lines.append(line)
        elif line.strip():
            command_lines.append(line)

    #Split commands into n chunks
    chunks = split_list(command_lines, num_splits)

    #Prepare output filenames
    base_name = os.path.splitext(input_file)[0]
    extension = os.path.splitext(input_file)[1]

    for i, chunk in enumerate(chunks):
        output_filename = f"{base_name}_split{i}{extension}"
        with open(output_filename, 'w') as f:
            f.writelines(header_lines)
            f.writelines(chunk)

if __name__ == '__main__':
    main()
