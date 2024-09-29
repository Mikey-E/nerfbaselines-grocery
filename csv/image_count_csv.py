#Author: Michael Elgin

import os

#Where are the images to count
GROCERY_DATA_CONVERTED_DIR = os.getenv("GROCERY_DATA_CONVERTED_DIR")
GROCERY_CSVS_DIR = os.getenv("GROCERY_CSVS_DIR")

#Confirm these are set
assert(GROCERY_DATA_CONVERTED_DIR != None)
assert(GROCERY_CSVS_DIR != None)

OUTPUT_FILENAME = "scene_image_count.csv"

with open(GROCERY_CSVS_DIR + OUTPUT_FILENAME, "w") as f:
    f.write("scene_folder_name, images_count\n")
    for scene_folder in os.listdir(GROCERY_DATA_CONVERTED_DIR):
        f.write(scene_folder + ","\
        + str(len(os.listdir(GROCERY_DATA_CONVERTED_DIR + "/" + scene_folder + "/images"))) + "\n")

print("Read scenes from " + GROCERY_DATA_CONVERTED_DIR)
print("Created output file: " + GROCERY_CSVS_DIR + OUTPUT_FILENAME)
