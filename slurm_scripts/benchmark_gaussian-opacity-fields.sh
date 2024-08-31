#!/bin/bash

#@@@NEEDS TO BE DONE BY actual live shell 1st - unless you investigate and find out why this is necessary and do otherwise
#conda activate /project/3dllms/melgin/conda/envs/conda-envs/instant-ngp/7ad00635e316fd20e609aafee828b33c8039fa9952b0a1784e172b350746bb9c/instant-ngp
#conda deactivate

#SBATCH --account=3dllms
#SBATCH --time=6-23:59:59 #max runtime

#Job names preferably are specified to sbatch with -J
##SBATCH --job-name=sbatch_test

#SBATCH --nodes=1

#may want to change to mb-h100 or inv-ssheshap
#SBATCH --partition=non-investor
##SBATCH --partition=mb-h100
##SBATCH --partition=inv-ssheshap
##SBATCH --partition=mb-l40s

#gaussian-opacity-fields has oom hazard, so minimum memory is a good idea
#above 128GB tends to choke out job scheduling (at least on h100s)
#SBATCH --mem=16GB #Total memory (this is a minimum for scheduling on a node)

#Probably don't want to limit gpu type unless it's necessary
##SBATCH --gres=gpu:h100:1 #Number of GPUs per node
#SBATCH --gres=gpu:1

#Specifying the logs programatically is better, and that can't be done by sbatch directive
#Preferably use -o in srun below
##SBATCH -o ./logs/$1.log #DO NOT USE, IT WON'T INTERPOLATE $1

scene_folder=$1 #particular scene folder
data_path=$2 #data path (where all scene folders live)
results_path=$3 #results path (where all scene folders of this kind are stored)

#Add slashes to the paths if not present. No need for scene_folder
for var in data_path results_path; do
	if [[ "${!var}" != */ ]]; then  #Check if the value of the variable doesn't end with a slash
        eval "$var=\"${!var}/\""  #Add a slash to the end of the value and update the variable
    fi
done

# Load modules required
ml arcc/1.0
ml gcc/13.2.0
ml cuda-toolkit/12.4.1

cd $NERFBASELINES_HOME_DIR
srun -o ./logs/gaussian-opacity-fields/$1.log nerfbaselines train --method gaussian-opacity-fields --data $data_path$scene_folder --output $results_path$scene_folder
