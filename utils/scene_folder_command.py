#Author: Michael Elgin
#This is a preprocessing step before running convert.py on all scene folders

import argparse
import os

parser = argparse.ArgumentParser(description="command to execute within all scene folders")
parser.add_argument(
        "--path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED",
        help="Path to the directory containing top level categories e.g. Fruits, Packages, etc"
    )
parser.add_argument(
        "--command",
        type=str,
        default="mv images input",
        help="Command to execute within each scene folder."
    )
args = parser.parse_args()

os.chdir(args.path)
for category in os.listdir(args.path):
    if category == "Random":#is effectively a sub-category
        os.chdir("Random")
        for scene_folder in os.listdir("."):
            os.chdir(scene_folder)
            os.system(args.command)
            os.chdir("..")
        os.chdir("..")
        continue
    os.chdir(category)
    for subcategory in os.listdir("."):
        os.chdir(subcategory)
        for scene_folder in os.listdir("."):
            os.chdir(scene_folder)
            os.system(args.command)
            os.chdir("..")
        os.chdir("..")
    os.chdir("..")
