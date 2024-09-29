#Author: Michael Elgin
#To check whether or not all the "input" folders have the same amt of contents as "images"

import argparse
import os

parser = argparse.ArgumentParser(description="command to execute within all scene folders")
parser.add_argument(
        "--path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED/",
        help="Path to the directory containing top level categories e.g. Fruits, Packages, etc"
    )
args = parser.parse_args()

for category in os.listdir(args.path):
    if category == "Random":#is effectively a sub-category
        for scene_folder in os.listdir(args.path + "Random/"):
            if len(os.listdir(args.path + "Random/" + scene_folder + "/input/"))\
                    == len(os.listdir(args.path + "Random/" + scene_folder + "/images/")):
                print("Random/" + scene_folder + ":True")
            else:
                print("Random/" + scene_folder + ":False")
        continue
    for subcategory in os.listdir(args.path + category):
        for scene_folder in os.listdir(args.path + category + "/" + subcategory):
            if len(os.listdir(args.path + category + "/" + subcategory + "/"\
                    + scene_folder + "/input/"))\
                    ==\
                    len(os.listdir(args.path + category + "/" + subcategory + "/"\
                    + scene_folder + "/images/")):
                print(category + "/" + subcategory + "/" + scene_folder + ":True")
            else:
                print(category + "/" + subcategory + "/" + scene_folder + ":False")
