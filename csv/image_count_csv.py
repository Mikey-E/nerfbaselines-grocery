#Author: Michael Elgin
#File to make a simple csv file of the counts of images per scene

import os
import argparse

#Set up argparse to handle directory paths as arguments
parser = argparse.ArgumentParser(description="Count images in scenes and write to CSV")
parser.add_argument(
    "--data_dir_path",
    type=str,
    required=True,
    help="Path to the directory containing all scene folders (ungrouped).",
)
parser.add_argument(
    "--csv_dir_path",
    type=str,
    help="Path to the directory where the output CSV should be saved.",
    default=os.getenv("GROCERY_CSVS_DIR_PATH"),
)
parser.add_argument(
    "--output_filename",
    type=str,
    help="Name of the output CSV file.",
    default="scene_image_count.csv",
)
args = parser.parse_args()

#Confirm these are set correctly
assert(args.data_dir_path != None)
assert(args.csv_dir_path != None)
if args.output_filename[-4:] != ".csv":
    args.output_filename += ".csv"
args.data_dir_path = args.data_dir_path.rstrip("/") + "/"
args.csv_dir_path = args.csv_dir_path.rstrip("/") + "/"

with open(args.csv_dir_path + args.output_filename, "w") as f:
    f.write("scene_folder_name, images_count\n")
    for scene_folder in os.listdir(args.data_dir_path):
        f.write(scene_folder + ","\
        + str(len(os.listdir(args.data_dir_path + scene_folder + "/images"))) + "\n")

print("Read scenes from " + args.data_dir_path)
print("Created output file: " + args.csv_dir_path + args.output_filename)
