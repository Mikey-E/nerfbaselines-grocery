#Author: Michael Elgin

import os
import sys
import re
import json
import csv

model = sys.argv[1]

pattern = r"^results-.*\.json$"

data_for_csv = []

#This is using non-grouped dataset
data_folders_path = "/project/3dllms/DATASETS/PROCESSED/"
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
    "zipnerf" : "zipnerf"
}

for folder in os.listdir(data_folders_path):
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
                data_for_csv.append({
                    "folder": folder,
                    "psnr":   data["metrics"]["psnr"],
                    "ssim":   data["metrics"]["ssim"],
                    "lpips":  data["metrics"]["lpips"],
                })
                print(data["metrics"]["psnr"])
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
    print(os.getcwd())

with open(output_path + model + ".csv", mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["folder", "psnr", "ssim", "lpips"])
    writer.writeheader()
    for row in data_for_csv:
        writer.writerow(row)
