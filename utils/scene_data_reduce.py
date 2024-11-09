#Author: Michael Elgin
#This file is to create the modified datasets containing 90%, 50%, and 10% of the data for ablation studies.
#This file will probably only need to be run once.
#A converted version for gaussian models should be created from a dataset that has ALREADY had its images reduced.
#DO NOT simply reduce data on a converted version because then there is a mismatch between the data and the conversion output(s)

import argparse
import os

parser = argparse.ArgumentParser(description="reduce data in all scene folders (for ablation studies)")
parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to the directory containing scene folders"
    )
parser.add_argument(
        "--percent",
        type=float,
        required=True,
        help="Percent of the data to KEEP."
    )
args = parser.parse_args()

#Arg checks
assert os.path.exists(args.path), f"{args.path} does not exist on the file system"
args.path = args.path.rstrip("/") + "/"
assert args.percent >= 0 and args.percent <= 100

for scene_folder in os.listdir(args.path):
	images_in_scene = os.listdir(args.path + scene_folder + "/images")
	total_images_in_scene = len(images_in_scene)
	threshold = (args.percent/100) * total_images_in_scene
	images_to_remove = [image for image in images_in_scene if int(image.split(".")[0]) > threshold]
	for images_folder in ["images", "images_2", "images_4", "images_8"]:
		for image in images_to_remove:
			os.system("rm " + args.path + scene_folder + "/" + images_folder + "/" + image)
