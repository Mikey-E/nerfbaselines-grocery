#Author: Michael Elgin
#This file should generate a list of all nerfbaselines training commands to be run, for a specific model
#Keep it by redirect ie '>'
#Example run: python multi-train.py mip-splatting --triage > commands_to_run.sh
#And then you could keep it running w/ nohup: nohup ./commands_to_run.sh &

import os
import sys
import argparse
from utils.allowed_models import allowed_models

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
parser.add_argument(
    "--logs_path",
    default=os.getenv("GROCERY_LOGS_DIR_PATH") + model + "/",
    help="Logs directory: where to put the log folders for each scene",
)
args = parser.parse_args(sys.argv[2:])#Requires model as first argument before options

#Ask whether logs should be cleared
if (os.path.isdir(args.logs_path) and len(os.listdir(args.logs_path)) != 0):#if logs are already there
    print(f"#WARNING: logs already present at {args.logs_path}")

#Confirm settings are as user wants
print("#------- Settings for this run --------")
print("#model: " + model)
print("#data path: " + args.data_path)
print("#results path: " + args.results_path)
print("#logs path: " + args.logs_path)
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
    command = f"nerfbaselines train --method {model} --data {args.data_path} --output {args.results_path}"
    print(command)
