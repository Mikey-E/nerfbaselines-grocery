#Author: Michael Elgin

import os
import sys
import re
import json
import csv

model = sys.argv[1]

pattern = r"^results-.*\.json$"

data_for_csv = []

data_folders_path = "/project/3dllms/DATASETS/GROUPED/"
project_path = "/cluster/medbow/project/3dllms/melgin/nerfbaselines-grocery/"
results_path = project_path + "results/"
output_path = project_path + "csv/csv_results/"

#Prefixes for results folder
#Condiser registry.get_supported_methods() for the method names
prefixes = {
    "instant-ngp"   :   "ingp",
    "nerfacto"      :   "nerfacto",
    "gaussian-opacity-fields" : "gaussian-opacity-fields",
    "gaussian-splatting" : "gaussian-splatting",
    "mip-splatting" : "mip-splatting",
    "zipnerf" : "zipnerf",
}

for category in os.listdir(data_folders_path):
    if category == "Random":#is effectively a sub-category
        continue #until we decide what we want to do with this - right now it's not even part of the paper
    os.chdir(data_folders_path + category)
    for subcategory in os.listdir("."):
        psnr_sum = 0
        ssim_sum = 0
        lpips_sum = 0
        folder_count = 0
        os.chdir(data_folders_path + category + "/" + subcategory)
        for folder in os.listdir("."):
            try:
                #nerfacto special-case for where it (finally) writes results
                if model == "nerfacto":
                    os.chdir(results_path + prefixes[model] + "/" + folder + "/results/" + prefixes[model] + "_" + folder)
                else:
                    os.chdir(results_path + prefixes[model] + "/" + folder)
                found = False
                for item in os.listdir("."):
                    if bool(re.match(pattern, item)):
                        with open(item, 'r') as f:
                            data = json.load(f)
                            found = True
                        psnr_sum += data["metrics"]["psnr"]
                        ssim_sum += data["metrics"]["ssim"]
                        lpips_sum += data["metrics"]["lpips"]
                        folder_count += 1
                        #continue?
                if not found:
#                    raise Exception(os.getcwd() + " RESULTS EXPECTED BUT NOT FOUND")
                    print("Did not find data for " + folder + ", skipping")
            except FileNotFoundError as e:
                print(e)
            print(os.getcwd())
        data_for_csv.append({
            "subcategory": subcategory,
            "psnr":   psnr_sum / folder_count,
            "ssim":   ssim_sum / folder_count,
            "lpips":  lpips_sum / folder_count,
        })

with open(output_path + model + "_avgs.csv", mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["subcategory", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in data_for_csv:
        row["psnr"] = f"{row['psnr']:.3f}"#change to 3 decimal places for easy copy-paste
        row["ssim"] = f"{row['ssim']:.3f}"#change to 3 decimal places for easy copy-paste
        row["lpips"] = f"{row['lpips']:.3f}"#change to 3 decimal places for easy copy-paste
        writer.writerow(row)
