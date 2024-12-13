#Author: Michael Elgin
#Remember that every scene folder within converted should have its "images" renamed to "input".
#There is a utils/ python script for this.

import argparse
import os

parser = argparse.ArgumentParser(description="Create jobs to convert all grocery scenes")
parser.add_argument(
        "--scene_path",
        type=str,
        default="/project/3dllms/DATASETS/CONVERTED",
        help="Path to the directory containing top level categories e.g. Fruits, Packages, etc"
    )
parser.add_argument(
        "--nerfbaselines_path",
        type=str,
        default="/cluster/medbow/project/3dllms/melgin/nerfbaselines-grocery",
        help="Path to the directory containing top level nerfbaselines code"
    )
args = parser.parse_args()

for scene_folder in os.listdir(args.scene_path):
    path = args.scene_path.rstrip("/") + "/" + scene_folder
    command = "sbatch -J convert_" + scene_folder + " " + args.nerfbaselines_path + "/slurm_scripts/convert.sh " + path
    print(command)
    os.system(command)
