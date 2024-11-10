#Author: Michael Elgin

import os
import sys
import re
import json
import csv
import argparse

parser = argparse.ArgumentParser(description="Create a csv file of scene names and their metrics from training.")
parser.add_argument(
    "--training_scene_folders_dir_path_ungrouped",
    type=str,
    required=True,
    help="Path to the directory containing all scene folders (ungrouped) used in training.",
)
parser.add_argument(
    "--training_scene_folders_dir_path_grouped",
    type=str,
    required=True,
    help="Path to the directory containing all scene folders (grouped) used in training.",
)
parser.add_argument(
    "--results_scene_folders_dir_path",
    type=str,
    required=True,
    help="Path to the directory containing all scene folders (ungrouped) of the training results.",
)
parser.add_argument(
    "--filter_list_file_path",
    type=str,
    help="File path to a .txt list of scenes to gather results for, skipping all other scenes",
    default=None,
)
parser.add_argument(
    "--csv_dir_path",
    type=str,
    help="Path to the directory where the output CSV should be saved.",
    default=os.getenv("GROCERY_CSVS_DIR_PATH"),
)
args = parser.parse_args()

#arg checking
args.training_scene_folders_dir_path_ungrouped = args.training_scene_folders_dir_path_ungrouped.rstrip('/') + '/'
args.training_scene_folders_dir_path_grouped = args.training_scene_folders_dir_path_grouped.rstrip('/') + '/'
args.results_scene_folders_dir_path = args.results_scene_folders_dir_path.rstrip('/') + '/'
if args.csv_dir_path == None:
    raise argparse.ArgumentTypeError("--csv_dir_path is None. It must be set to a location to place the output")
args.csv_dir_path = args.csv_dir_path.rstrip('/') + '/'
if args.filter_list_file_path:
    args.filter_list_file_path = args.filter_list_file_path.rstrip('/') #Shouldn't have trailing '/'
    #Creating filter for the best scenes
    with open(args.filter_list_file_path, 'r') as file:
        lines = file.readlines()
    best_scenes = [line.strip() for line in lines]

#determine what the name of the output file should be. This will match the name of the particular results folder
results_name = args.results_scene_folders_dir_path.rstrip('/').split('/')[-1]

#Create regex for finding the results files
pattern = r"^results-.*\.json$"

data_for_csv = []

for folder in os.listdir(args.training_scene_folders_dir_path_ungrouped):
    #Skipping unless in best scenes, if set
    if args.filter_list_file_path:
        if folder not in best_scenes:
            continue
    try:
        #nerfacto special-case for where it (finally) writes results
        if os.path.exists(args.results_scene_folders_dir_path + folder + "/results/nerfacto_" + folder):
            path = args.results_scene_folders_dir_path + folder + "/results/nerfacto_" + folder
        else:
            path = args.results_scene_folders_dir_path + folder
        print(f"path: {path}")#Show what folder on
        found = False
        for item in os.listdir(path):
            if bool(re.match(pattern, item)):
                with open(path + '/' + item, 'r') as f:
                    data = json.load(f)
                    found = True
                data_for_csv.append({
                    "folder": folder,
                    "psnr":   data["metrics"]["psnr"],
                    "ssim":   data["metrics"]["ssim"],
                    "lpips":  data["metrics"]["lpips"],
                })
                break #No need to iterate further
        if not found:
#            raise Exception(os.getcwd() + " RESULTS EXPECTED BUT NOT FOUND")
            data_for_csv.append({
                "folder": folder,
                "psnr":   "null",
                "ssim":   "null",
                "lpips":  "null",
            })
    except FileNotFoundError as e:
        print(e)

#Write flat results file
with open(args.csv_dir_path + results_name + ".csv", mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["folder", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in data_for_csv:
        writer.writerow(row)

#Subcategories
data_for_csv = []
for category in os.listdir(args.training_scene_folders_dir_path_grouped):
    if category == "Random":#is effectively a sub-category
        continue #until we decide what we want to do with this - right now it's not even part of the paper
    for subcategory in os.listdir(args.training_scene_folders_dir_path_grouped + category):
        psnr_sum = 0
        ssim_sum = 0
        lpips_sum = 0
        folder_count = 0
        for folder in os.listdir(args.training_scene_folders_dir_path_grouped + category + '/' + subcategory):
            try:
                #nerfacto special-case for where it (finally) writes results
                if os.path.exists(args.results_scene_folders_dir_path + folder + "/results/nerfacto_" + folder):
                    path = args.results_scene_folders_dir_path + folder + "/results/nerfacto_" + folder
                else:
                    path = args.results_scene_folders_dir_path + folder
                print(f"subcategory path: {path}")#Show what folder on
                found = False
                for item in os.listdir(path):
                    if bool(re.match(pattern, item)):
                        with open(path + '/' + item, 'r') as f:
                            data = json.load(f)
                            found = True
                        psnr_sum += data["metrics"]["psnr"]
                        ssim_sum += data["metrics"]["ssim"]
                        lpips_sum += data["metrics"]["lpips"]
                        folder_count += 1
                        break #No need to iterate further
                if not found:
#                    raise Exception(os.getcwd() + " RESULTS EXPECTED BUT NOT FOUND")
                    print("Did not find data for " + folder + ", skipping")
            except FileNotFoundError as e:
                print(e)
        data_for_csv.append({
            "subcategory": subcategory,
            "folder_count": folder_count,
            "psnr":   psnr_sum / folder_count,
            "ssim":   ssim_sum / folder_count,
            "lpips":  lpips_sum / folder_count,
        })

#Write subcategories results file
with open(args.csv_dir_path + results_name + "_subcat_avgs.csv", mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["subcategory", "folder_count", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in data_for_csv:
        row["folder_count"] = f"{row['folder_count']}"#Should stay int
        row["psnr"] = f"{row['psnr']:.3f}"#change to 3 decimal places for easy copy-paste
        row["ssim"] = f"{row['ssim']:.3f}"#change to 3 decimal places for easy copy-paste
        row["lpips"] = f"{row['lpips']:.3f}"#change to 3 decimal places for easy copy-paste
        writer.writerow(row)
