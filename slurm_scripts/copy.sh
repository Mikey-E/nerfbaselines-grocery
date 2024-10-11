#!/bin/bash

#For copying grocery dataset in parallel

#SBATCH --account=3dllms
#SBATCH --time=24:00:00 # max runtime
#SBATCH --nodes=1
#SBATCH --partition=non-investor
#SBATCH --mem=16G
#SBATCH --gres=none

#Example run: sbatch -J jobname copy.sh arg1 arg2...
DATA_SRC=$1
DATA_DEST=$2
LOGS_DIR_PATH=$3
SCENE_FOLDER=$4

srun -o $LOGS_DIR_PATH/copy_$SCENE_FOLDER.log time cp -r $DATA_SRC/$SCENE_FOLDER $DATA_DEST/
