#Author: Michael Elgin
#Example run: python multi-benchmark.py mip-splatting --triage

import os
import sys
import argparse
from allowed_models import allowed_models

#Model to benchmark
model = sys.argv[1]
assert model in allowed_models, "Must pass a valid model name as first arg"

#Begin building parser
parser = argparse.ArgumentParser(description="Create jobs to benchmark grocery scenes")
parser.add_argument(
    "--triage",
    action='store_true',
    help="Only run jobs on previously failed scenes"
)
parser.add_argument(
    "--data_path",
    default =
        os.getenv("GROCERY_DATA_CONVERTED_DIR")
        if model in ["gaussian-opacity-fields", "gaussian-splatting", "mip-splatting"] else
        os.getenv("GROCERY_DATA_NORMAL_DIR"),
    help="Data directory: where the properly formatted scene folders are",
)
parser.add_argument(
    "--results_path",
    default=os.getenv("GROCERY_RESULTS_DIR") + model + "/",
    help="Results directory: where to put the results folders for each scene",
)
parser.add_argument(
    "--logs_path",
    default=os.getenv("GROCERY_LOGS_DIR") + model + "/",
    help="Logs directory: where to put the log folders for each scene",
)
args = parser.parse_args(sys.argv[2:])#Requires model as first argument before options

#Ask whether logs should be cleared
if (os.path.isdir(args.logs_path) and len(os.listdir(args.logs_path)) != 0):#if logs are already there
    if (input("clear logs? y/[n]: ") == 'y'):
        os.system("rm -rf " + args.logs_path)

#Confirm settings are as user wants
print("------- Settings for this run --------")
print("data path: " + args.data_path)
print("results path: " + args.results_path)
print("model: " + model)
print("--------------------------------------")
if (input("Continue? y/[n]: ") != 'y'): exit(0)

if args.triage:
    import re
    pattern = r"^results-.*\.json$"
else:#Warn
    if (input("triage flag not set, this will re-run any previous successful runs. Continue? y/[n]: ") != 'y'): exit(0)

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
    #Trailing arguments of the command should match what is expected by the benchmarking script
    command =\
        "sbatch -J " + model + "_" + scene_folder + " "\
        + os.getenv("NERFBASELINES_HOME_DIR") + "slurm_scripts/benchmark_" + model + ".sh "\
        + scene_folder + " " + args.data_path + " " + args.results_path
    os.system("echo command is: " + command)
    os.system(command)
