#Author: Michael Elgin

import os

#Where are the images to count
GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH = os.getenv("GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH")
GROCERY_CSVS_DIR_PATH = os.getenv("GROCERY_CSVS_DIR_PATH")

#Confirm these are set
assert(GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH != None)
assert(GROCERY_CSVS_DIR_PATH != None)

OUTPUT_FILENAME = "scene_image_count.csv"

with open(GROCERY_CSVS_DIR_PATH + OUTPUT_FILENAME, "w") as f:
    f.write("scene_folder_name, images_count\n")
    for scene_folder in os.listdir(GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH):
        f.write(scene_folder + ","\
        + str(len(os.listdir(GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH + "/" + scene_folder + "/images"))) + "\n")

print("Read scenes from " + GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH)
print("Created output file: " + GROCERY_CSVS_DIR_PATH + OUTPUT_FILENAME)
