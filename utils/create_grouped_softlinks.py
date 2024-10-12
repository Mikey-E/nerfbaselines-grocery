#Author: Michael Elgin
#File to make softlinks for an ungrouped dataset in its corresponding grouped folder.
#This assumes the actual data is stored in an ungrouped folder, and grouped soft-links should point to it based on
#the original grouping hierarchy of categories and subcategories

import os
import argparse

parser = argparse.ArgumentParser(description="create grouped soft-links for a copy of the dataset")
parser.add_argument(
    "--new_ungrouped_dir_path",
    type=str,
    required=True,
    help="Flat location of scene folders where the grouped soft-links will point to"
)
parser.add_argument(
    "--new_grouped_dir_path",
    type=str,
    required=True,
    help="Location of where to place the grouped soft-links"
)
parser.add_argument(
    "--old_grouped_dir_path",
    type=str,
    default="/project/3dllms/DATASETS/GROUPED/",
    help="Location of where current grouped data folders exist, to model after"
)
args = parser.parse_args()

#Ensure the provided paths exist
if not os.path.exists(args.new_ungrouped_dir_path):
    raise FileNotFoundError(f"Path '{args.new_ungrouped_dir_path}' doesn't exist. Provide a valid path.")
if not os.path.exists(args.new_grouped_dir_path):
    raise FileNotFoundError(f"Path '{args.new_grouped_dir_path}' doesn't exist. Provide a valid path.")
if not os.path.exists(args.old_grouped_dir_path):
    raise FileNotFoundError(f"Path '{args.old_grouped_dir_path}' doesn't exist. Provide a valid path.")

#paths should end in a '/' for subsequent code
args.new_ungrouped_dir_path = args.new_ungrouped_dir_path.rstrip("/") + "/"
args.new_grouped_dir_path = args.new_grouped_dir_path.rstrip("/") + "/"
args.old_grouped_dir_path = args.old_grouped_dir_path.rstrip("/") + "/"

for category in os.listdir(args.old_grouped_dir_path):
    os.makedirs(args.new_grouped_dir_path + category, exist_ok=True)
    if category == "Random": #is effectively a sub-category
        for scene_folder in os.listdir(args.old_grouped_dir_path + category):
            command = "ln -s " + args.new_ungrouped_dir_path + scene_folder + " "\
            + args.new_grouped_dir_path + category + "/" + scene_folder
            print(command)
            os.system(command)
        continue
    for subcategory in os.listdir(args.old_grouped_dir_path + category):
        os.makedirs(args.new_grouped_dir_path + category + "/" + subcategory, exist_ok=True)
        for scene_folder in os.listdir(args.old_grouped_dir_path + category + "/" + subcategory):
            command = "ln -s " + args.new_ungrouped_dir_path + scene_folder + " "\
            + args.new_grouped_dir_path + category + "/" + subcategory + "/" + scene_folder
            print(command)
            os.system(command)
