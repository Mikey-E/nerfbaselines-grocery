#Author: Michael Elgin
#This script is to do a parallel re-copy of the grocery data
#Don't forget to create the softlinks in a grouped structure. This file is only for creating jobs for parallel copy
#   There is probably a script in utils/ to do this

import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(description="Create jobs to copy the grocery data to a new location")
parser.add_argument(
        "--data_src_dir_path",
        type=str,
        default="/project/3dllms/DATASETS/PROCESSED/", #the original sheshapp data
        help="Path to the source directory containing all the scene folders at the same level"
    )
parser.add_argument(
        "--data_dest_dir_path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED/NORMAL/UNGROUPED/",
        help="Path to the destination directory to contain all the scene folders at the same level"
    )
parser.add_argument(
        "--logs_dir_path",
        type=str,
        default=os.getenv("GROCERY_LOGS_DIR_PATH"),
        help="Path to put log files",
)
parser.add_argument('-y', '--yes', action='store_true', help='Automatically confirm and bypass settings confirmation')
args = parser.parse_args()

#Arg checks
NERFBASELINES_HOME_DIR_PATH = os.getenv("NERFBASELINES_HOME_DIR_PATH")
assert NERFBASELINES_HOME_DIR_PATH != None, "must set env var NERFBASELINES_HOME_DIR_PATH to where nerfbaselines code is"
NERFBASELINES_HOME_DIR_PATH = NERFBASELINES_HOME_DIR_PATH.rstrip("/") + "/" #end in exactly 1 /

assert os.path.exists(args.data_src_dir_path), f"data source path {args.data_src_dir_path} must exist"
args.data_src_dir_path = args.data_src_dir_path.rstrip("/") + "/"

assert args.data_dest_dir_path != None, "must set --data_dest_dir_path so copying can be put there"
os.makedirs(args.data_dest_dir_path, exist_ok=True) #Ensure destination is ready
args.data_dest_dir_path = args.data_dest_dir_path.rstrip("/") + "/"

assert args.logs_dir_path != None, "must set env var GROCERY_LOGS_DIR_PATH so the logs can be placed there"
os.makedirs(args.logs_dir_path, exist_ok=True)
args.logs_dir_path = args.logs_dir_path.rstrip("/") + "/"

#Within the log path given, make sure everything in this run goes in <filename>_yyyy_mm_dd_hh_mm_ss/
#No extension of the filename when used as part of this directory to put the logs in
args.logs_dir_path += os.path.splitext(os.path.basename(__file__))[0] + "_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

#Confirm settings are as user wants
print("------- Settings for this run --------")
print("nerfbaselines path: " + NERFBASELINES_HOME_DIR_PATH)
print("data source path: " + args.data_src_dir_path)
print("data destination path: " + args.data_dest_dir_path)
print("logs path: " + args.logs_dir_path)
print("--------------------------------------")
if not args.yes:
    if (input("Continue? y/[n]: ") != 'y'):
        exit(0)

#Copy in parallel
for scene_folder in os.listdir(args.data_src_dir_path):
    #Command should match the args expected by the slurm script
    command = (
        f"sbatch -J copy_{scene_folder} {NERFBASELINES_HOME_DIR_PATH}slurm_scripts/copy.sh "
        f"{args.data_src_dir_path} {args.data_dest_dir_path} {args.logs_dir_path} {scene_folder}"
    )
    print(command)
    os.system(command)
