#Author: Michael Elgin
#This is a preprocessing step before running convert.py on all scene folders

import argparse
import os

parser = argparse.ArgumentParser(description="command to execute within all scene folders")
parser.add_argument(
        "--path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED",
        help="Path to the directory containing scene folders"
    )
parser.add_argument(
        "--command",
        type=str,
        default="mv images input",
        help="Command to execute within each scene folder."
    )
args = parser.parse_args()

#Arg checks
assert os.path.exists(args.path), f"{args.path} does not exist on the file system"
args.path = args.path.rstrip("/") + "/"

for scene_folder in os.listdir(args.path):
    os.chdir(args.path + scene_folder)
    os.system(args.command)
