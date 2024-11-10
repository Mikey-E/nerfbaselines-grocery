#Author: Michael Elgin

import os
import sys
import re
import json
import csv
import argparse

parser = argparse.ArgumentParser(description="Create a csv file of scene names and their metrics from training.")
parser.add_argument(
    "--training_scene_folders_dir_path",
    type=str,
    required=True,
    help="Path to the directory containing all scene folders (ungrouped) used in training.",
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
args.training_scene_folders_dir_path = args.training_scene_folders_dir_path.rstrip('/') + '/'
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

for folder in os.listdir(args.training_scene_folders_dir_path):
    #Skipping unless in best scenes, if set
    if args.filter_list_file_path:
        if folder not in best_scenes:
            continue
    try:
        #nerfacto special-case for where it (finally) writes results
        if "nerfacto" in results_name:
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

with open(args.csv_dir_path + results_name + ".csv", mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["folder", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in data_for_csv:
        writer.writerow(row)
