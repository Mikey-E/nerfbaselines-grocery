#Author: Michael Elgin
#This file should generate a list of all nerfbaselines training commands to be run, for a specific model
#Keep it by redirect ie '>'
#Example run: python multi-train.py mip-splatting --triage > commands_to_run.sh
#And then you could keep it running w/ nohup: nohup ./commands_to_run.sh &

import os
import sys
import argparse
from utils.allowed_models import allowed_models

from pathlib import Path

def get_images_symlink_target(base_dir):
    """
    Pass the data path and this should return the ablation setting
    """
    images_link = Path(base_dir) / "images"
    if images_link.is_symlink():
        target = images_link.resolve()
        # Check which images_X folder it points to
        for suffix in ["images_1", "images_2", "images_4", "images_8"]:
            if target.name == suffix:
                print(f'"images" symlink points to: {suffix}')
                return suffix
        print(f'"images" symlink points to: {target} (not a known images_X folder)')
        return target
    else:
        print('"images" is not a symlink.')
        return None

#Model to benchmark
model = sys.argv[1]
assert model in allowed_models, "Must pass a valid model name as first arg"

#Begin building parser
parser = argparse.ArgumentParser(description="Create commands to benchmark grocery scenes")
parser.add_argument(
    "--triage",
    action='store_true',
    help="Only create commands for previously failed scenes"
)
parser.add_argument(
    "--data_path",
    default =
        os.getenv("GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH")
        if model in ["gaussian-opacity-fields", "gaussian-splatting", "mip-splatting", "scaffold-gs"] else
        os.getenv("GROCERY_DATA_NORMAL_UNGROUPED_DIR_PATH"),
    help="Data directory: where the properly formatted scene folders are",
)
parser.add_argument(
    "--results_path",
    default=os.getenv("GROCERY_RESULTS_DIR_PATH") + model + "/",
    help="Results directory: where to put the results folders for each scene",
)
args = parser.parse_args(sys.argv[2:])#Requires model as first argument before options

#Confirm settings are as user wants
print("#------- Settings for this run --------")
print("#model: " + model)
print("#data path: " + args.data_path)
print("#results path: " + args.results_path)
print("#folder size setting: " + get_images_symlink_target(os.path.join(args.data_path, 04_19_2024_W_F_Dressings_P_2)))#arbitrary folder from ungrouped
print("#--------------------------------------")

if args.triage:
    import re
    pattern = r"^results-.*\.json$"
elif (os.path.isdir(args.results_path) and len(os.listdir(args.results_path)) != 0):#if results are already there
    print(f"#WARNING: triage flag not set, this will re-run any previous successful runs at {args.results_path}")

for scene_folder in os.listdir(args.data_path):
    if args.triage:
        is_results_found=False
        try:
            for item in os.listdir(args.results_path + scene_folder):
                if bool(re.match(pattern, item)):
                    is_results_found=True
                    break
            if is_results_found:
                continue
        except FileNotFoundError:
            pass #ie this one needs to run, go forth and make the command
    command = \
        f"nerfbaselines train --method {model} --data {args.data_path}{scene_folder} --output {args.results_path}{scene_folder}"
    print(command)
