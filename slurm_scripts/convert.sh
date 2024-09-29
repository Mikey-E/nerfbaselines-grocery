#!/bin/bash

#SBATCH --account=3dllms
#SBATCH --time=24:00:00 # max runtime
#SBATCH --nodes=1
#SBATCH --partition=non-investor
#SBATCH --gres=gpu:1

#convert.py can have OOM errors, so have an sbatch directive for minimum memory
#128GB seems to be a good large amount, without being so large as to severely limit the amount of jobs that go thru
#SBATCH --mem=128GB #Total memory (this is a minimum for scheduling on a node)

#The a30 gpus tend to have issues finishing running convert.py, so I have disallowed them
#SBATCH --constraint="l40s|h100"

# Load modules required
ml gcc/13.2.0
ml cuda-toolkit/12.4.1

#@@@ these 2 commands don't seem to help and it looks like i have to activate the conda env in the current shell
conda init
conda activate convert_scenes

#@@@ probably don't want to use a relative path ../utils/convert.py, may lead to bugs
srun -o ../logs/convert_$1.log time python ../utils/convert.py --source_path $1
