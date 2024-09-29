#!/bin/bash

#For copying grocery dataset in parallel
#Example run: sbatch -J Fruits copy.sh Fruits
#And then you'll want to do the other categories

#SBATCH --account=3dllms
#SBATCH --time=24:00:00 # max runtime
#SBATCH --nodes=1
#SBATCH --partition=non-investor
#SBATCH --gres=gpu:1

DATA_SRC=/project/3dllms/DATASETS/GROUPED
DATA_DEST=/project/3dllms/DATASETS/CONVERTED
srun -o ../logs/copy_$1.log time cp -r $DATA_SRC/$1 $DATA_DEST/$1
