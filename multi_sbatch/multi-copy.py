#Author: Michael Elgin
#Remember that every scene folder within converted should have its "images" renamed to "input",
#there is a utils/ python script for this.
#This script is to do a parallel re-copy of the grocery data, mostly by subcategory since
#doing it by category takes 1.3 hours

import argparse
import os

parser = argparse.ArgumentParser(description="Create jobs to copy the grocery data to a new location")
parser.add_argument(
        "--data_src_path",
        type=str,
        default="/project/3dllms/DATASETS/GROUPED",
        help="Path to the source directory containing top level categories e.g. Fruits, Packages, etc"
    )
parser.add_argument(
        "--data_dest_path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED",
        help="Path to the destination directories to contain top level categories e.g. Fruits, Packages, etc"
    )
parser.add_argument(
        "--nerfbaselines_path",
        type=str,
        default="/cluster/medbow/project/3dllms/melgin/nerfbaselines-grocery",
        help="Path to the directory containing top level nerfbaselines code"
    )
args = parser.parse_args()

#Create the category folders
for category in os.listdir(args.data_src_path):
    os.system("mkdir " + args.data_dest_path + "/" + category)

#Copy in parallel by subcategory
for category in os.listdir(args.data_src_path):
    for subcategory in os.listdir(args.data_src_path + "/" + category):
        command = "sbatch "\
                    + "-J " + subcategory + " "\
                    + args.nerfbaselines_path + "/slurm_scripts/copy.sh "\
                    + category + "/" + subcategory
        print(command)
        os.system(command)
