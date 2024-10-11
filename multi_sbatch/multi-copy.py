#Author: Michael Elgin
#This script is to do a parallel re-copy of the grocery data
#Don't forget to create the softlinks in a grouped structure. This file is only for creating jobs for parallel copy
#   There is probably a script in utils/ to do this

import argparse
import os

parser = argparse.ArgumentParser(description="Create jobs to copy the grocery data to a new location")
parser.add_argument(
        "--data_src_path",
        type=str,
        default="/project/3dllms/DATASETS/PROCESSED/", #the original sheshapp data
        help="Path to the source directory containing all the scene folders at the same level"
    )
parser.add_argument(
        "--data_dest_path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED/NORMAL_COPY/UNGROUPED/",
        help="Path to the destination directory to contain all the scene folders at the same level"
    )
parser.add_argument(
        "--logs_dir_path",
        type=str,
        default=os.getenv("GROCERY_LOGS_DIR"),
        help="Path to put log files",
)
args = parser.parse_args()

#Arg checks
NERFBASELINES_HOME_DIR = os.getenv("NERFBASELINES_HOME_DIR")
assert NERFBASELINES_HOME_DIR != None, "must set env var NERFBASELINES_HOME_DIR to where nerfbaselines code is"
NERFBASELINES_HOME_DIR = NERFBASELINES_HOME_DIR.rstrip("/") + "/" #end in exactly 1 /

assert os.path.exists(args.data_src_path), f"data source path {args.data_src_path} must exist"
args.data_src_path = args.data_src_path.rstrip("/") + "/"

assert args.data_dest_path != None, "must set --data_dest_path so copying can be put there"
os.makedirs(args.data_dest_path, exist_ok=True) #Ensure destination is ready
args.data_dest_path = args.data_dest_path.rstrip("/") + "/"

assert args.logs_dir_path != None, "must set env var GROCERY_LOGS_DIR so the logs can be placed there"
os.makedirs(args.logs_dir_path, exist_ok=True)
args.logs_dir_path = args.logs_dir_path.rstrip("/") + "/"

#Copy in parallel
for scene_folder in os.listdir(args.data_src_path):
    #Command should match the args expected by the slurm script
    command = (
        f"sbatch -J copy_{scene_folder} {NERFBASELINES_HOME_DIR}slurm_scripts/copy.sh "
        f"{args.data_src_path} {args.data_dest_path} {args.logs_dir_path} {scene_folder}"
    )
    print(command)
#    os.system(command)
