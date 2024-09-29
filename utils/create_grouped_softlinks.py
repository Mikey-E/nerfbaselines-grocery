#Author: Michael Elgin
#File to make softlinks for the converted dataset in its grouped folder

import os

#Necessary environment variables
GROCERY_DATA_CONVERTED_DIR = os.getenv("GROCERY_DATA_CONVERTED_DIR")
GROCERY_DATA_CONVERTED_GROUPED_DIR = os.getenv("GROCERY_DATA_CONVERTED_GROUPED_DIR")
GROCERY_DATA_NORMAL_GROUPED_DIR = os.getenv("GROCERY_DATA_NORMAL_GROUPED_DIR")

#Ensure they are set
assert(GROCERY_DATA_CONVERTED_DIR != None)
assert(GROCERY_DATA_CONVERTED_GROUPED_DIR != None)
assert(GROCERY_DATA_NORMAL_GROUPED_DIR != None)

for category in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR):
    os.makedirs(GROCERY_DATA_CONVERTED_GROUPED_DIR + category, exist_ok=True)
    if category == "Random": #is effectively a sub-category
        for scene_folder in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR + category):
            command = "ln -s " + GROCERY_DATA_CONVERTED_DIR + scene_folder + " "\
            + GROCERY_DATA_CONVERTED_GROUPED_DIR + category + "/" + scene_folder
            print(command)
            os.system(command)
        continue
    for subcategory in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR + category):
        os.makedirs(GROCERY_DATA_CONVERTED_GROUPED_DIR + category + "/" + subcategory, exist_ok=True)
        for scene_folder in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR + category + "/" + subcategory):
            command = "ln -s " + GROCERY_DATA_CONVERTED_DIR + scene_folder + " "\
            + GROCERY_DATA_CONVERTED_GROUPED_DIR + category + "/" + subcategory + "/" + scene_folder
            print(command)
            os.system(command)
