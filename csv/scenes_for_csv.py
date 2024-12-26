#Author: Michael Elgin

import os
import sys
import re
import json
import csv
import argparse
from pathlib import Path

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
            print("Ungrouped: Did not find results for " + folder + ", skipping")
            data_for_csv.append({
                "folder": folder,
                "psnr":   "null",
                "ssim":   "null",
                "lpips":  "null",
            })
    except FileNotFoundError as e:
        print(e)

#Write flat results file
flat_file = args.csv_dir_path + results_name + ".csv"
with open(flat_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["folder", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in data_for_csv:
        writer.writerow(row)
    print(f"Created: {flat_file}")

#Subcategories and categories
subcat_for_csv = []
cat_for_csv = []
for category in os.listdir(args.training_scene_folders_dir_path_grouped):
    if category == "Random":#is effectively a sub-category
        continue #until we decide what we want to do with this - right now it's not even part of the paper
    psnr_sum_cat = 0
    ssim_sum_cat = 0
    lpips_sum_cat = 0
    folder_count_cat = 0
    for subcategory in os.listdir(args.training_scene_folders_dir_path_grouped + category):
        psnr_sum_subcat = 0
        ssim_sum_subcat = 0
        lpips_sum_subcat = 0
        folder_count_subcat = 0
        for folder in os.listdir(args.training_scene_folders_dir_path_grouped + category + '/' + subcategory):
            try:
                #nerfacto special-case for where it (finally) writes results
                if os.path.exists(args.results_scene_folders_dir_path + folder + "/results/nerfacto_" + folder):
                    path = args.results_scene_folders_dir_path + folder + "/results/nerfacto_" + folder
                else:
                    path = args.results_scene_folders_dir_path + folder
                found = False
                for item in os.listdir(path):
                    if bool(re.match(pattern, item)):
                        with open(path + '/' + item, 'r') as f:
                            data = json.load(f)
                            found = True
                        psnr = data["metrics"]["psnr"]
                        ssim = data["metrics"]["ssim"]
                        lpips = data["metrics"]["lpips"]
                        psnr_sum_subcat += psnr
                        ssim_sum_subcat += ssim
                        lpips_sum_subcat += lpips
                        folder_count_subcat += 1
                        psnr_sum_cat += psnr
                        ssim_sum_cat += ssim
                        lpips_sum_cat += lpips
                        folder_count_cat += 1
                        break #No need to iterate further
                if not found:
#                    raise Exception(os.getcwd() + " RESULTS EXPECTED BUT NOT FOUND")
                    print("Grouped: Did not find results for " + folder + ", skipping")
            except FileNotFoundError as e:
                print(e)
        subcat_for_csv.append({
            "subcategory": subcategory,
            "folder_count_subcat": folder_count_subcat,
            "psnr":   (psnr_sum_subcat / folder_count_subcat) if folder_count_subcat != 0 else "null",
            "ssim":   (ssim_sum_subcat / folder_count_subcat) if folder_count_subcat != 0 else "null",
            "lpips":  (lpips_sum_subcat / folder_count_subcat) if folder_count_subcat != 0 else "null",
        })
    cat_for_csv.append({
        "category": category,
        "folder_count_cat": folder_count_cat,
        "psnr":   (psnr_sum_cat / folder_count_cat) if folder_count_cat != 0 else "null",
        "ssim":   (ssim_sum_cat / folder_count_cat) if folder_count_cat != 0 else "null",
        "lpips":  (lpips_sum_cat / folder_count_cat) if folder_count_cat != 0 else "null",
    })

#Write subcategories results file
subcat_file = args.csv_dir_path + results_name + "_subcat_avgs.csv"
with open(subcat_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["subcategory", "folder_count_subcat", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in subcat_for_csv:
        row["folder_count_subcat"] = f"{row['folder_count_subcat']}"#Should stay int
        row["psnr"] = (f"{row['psnr']:.3f}") if row['psnr'] != "null" else "null"
        row["ssim"] = (f"{row['ssim']:.3f}") if row['ssim'] != "null" else "null"
        row["lpips"] = (f"{row['lpips']:.3f}") if row['lpips'] != "null" else "null"
        writer.writerow(row)
    print(f"Created: {subcat_file}")

#Write categories results file
cat_file = args.csv_dir_path + results_name + "_cat_avgs.csv"
with open(cat_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["category", "folder_count_cat", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in cat_for_csv:
        row["folder_count_cat"] = f"{row['folder_count_cat']}"#Should stay int
        row["psnr"] = (f"{row['psnr']:.3f}") if row['psnr'] != "null" else "null"
        row["ssim"] = (f"{row['ssim']:.3f}") if row['ssim'] != "null" else "null"
        row["lpips"] = (f"{row['lpips']:.3f}") if row['lpips'] != "null" else "null"
        writer.writerow(row)
    print(f"Created: {cat_file}")
