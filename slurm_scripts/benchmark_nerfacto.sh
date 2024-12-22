#!/bin/bash

#SBATCH --account=3dllms
#SBATCH --time=06:00:00 #max runtime

#Job names preferably are specified to sbatch with -J
##SBATCH --job-name=sbatch_test

#SBATCH --nodes=1

#may want to change to mb-h100 or inv-ssheshap
#SBATCH --partition=non-investor
##SBATCH --partition=mb-h100
##SBATCH --partition=inv-ssheshap
##SBATCH --partition=mb-l40s

#minimum memory directives (if necessary)
#above 128GB tends to choke out job scheduling (at least on h100s)
##SBATCH --mem-per-gpu=16G #(this is a minimum for scheduling on a node)
#SBATCH --mem=16G #proper directive?

#Probably don't want to limit gpu type unless it's necessary
##SBATCH --gres=gpu:h100:1 #Number of GPUs per node
#SBATCH --gres=gpu:1

#Specifying the logs programatically is better, and that can't be done by sbatch directive
#Preferably use -o in srun below
##SBATCH -o ./logs/$1.log #DO NOT USE, IT WON'T INTERPOLATE $1

#a30s seem to cause problems so those are disallowed
#SBATCH --constraint="l40s|h100"
##SBATCH --constraint="h100"

scene_folder=$1 #particular scene folder
data_path=$2 #where all scene folders live
results_path=$3 #where all results folders of this kind will go
logs_path=$4 #where the log files will go

#Add slashes to the paths if not present. No need for scene_folder
for var in data_path results_path logs_path; do
	if [[ "${!var}" != */ ]]; then  #Check if the value of the variable doesn't end with a slash
        eval "$var=\"${!var}/\""  #Add a slash to the end of the value and update the variable
    fi
done

cd $NERFBASELINES_HOME_DIR_PATH
srun -o $logs_path$scene_folder.log nerfbaselines train --method nerfacto --data $data_path$scene_folder --output $results_path$scene_folder
