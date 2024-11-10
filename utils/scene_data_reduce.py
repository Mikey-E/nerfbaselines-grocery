#Author: Michael Elgin
#This file is to create the modified datasets containing 90%, 50%, and 10% of the data for ablation studies.
#This file will probably only need to be run once.

#A converted version for gaussian models should be created from a dataset that has ALREADY had its images reduced.
#DO NOT simply reduce data on a converted version because then there is a mismatch between the data and the conversion output(s).

#After the filtered_transforms.json files have been created, they will need to become transforms.json,
#so "mv filtered_transforms.json transforms.json", perhaps making a backup of the old transforms first as
#"mv transforms.json transforms.bak" if you want.
#Remember scene_folder_command can do this for all scene folders at once.

import argparse
import os
import json

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
#	threshold = (args.percent/100) * total_images_in_scene
#	images_to_remove = [image for image in images_in_scene if int(image.split(".")[0]) > threshold]
#	for images_folder in ["images", "images_2", "images_4", "images_8"]:
#		for image in images_to_remove:
#			os.system("rm " + args.path + scene_folder + "/" + images_folder + "/" + image)

	#Now update the transforms.json - leaving unmatched frames will cause errors,
	#that means having a transform for an image that no longer exists will cause errors.
	with open(args.path + scene_folder + "/transforms.json", 'r') as file:
		data=json.load(file)

	threshold=total_images_in_scene#@@@

	#Filter frames based on the image number in the file path
	filtered_frames=[
		frame for frame in data['frames']
		if int(frame['file_path'].split('/')[-1].split('.')[0])<=threshold
	]

	#Update the data with filtered frames
	data['frames']=filtered_frames

	#Save the filtered data back to JSON
	with open(args.path + scene_folder + "/filtered_transforms.json", 'w') as file:
		json.dump(data, file, indent=4)
