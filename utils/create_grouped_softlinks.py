#Author: Michael Elgin
#File to make softlinks for the converted dataset in its grouped folder

import os

#Necessary environment variables
GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH = os.getenv("GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH")
GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH = os.getenv("GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH")
GROCERY_DATA_NORMAL_GROUPED_DIR_PATH = os.getenv("GROCERY_DATA_NORMAL_GROUPED_DIR_PATH")

#Ensure they are set
assert(GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH != None)
assert(GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH != None)
assert(GROCERY_DATA_NORMAL_GROUPED_DIR_PATH != None)

for category in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR_PATH):
    os.makedirs(GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH + category, exist_ok=True)
    if category == "Random": #is effectively a sub-category
        for scene_folder in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR_PATH + category):
            command = "ln -s " + GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH + scene_folder + " "\
            + GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH + category + "/" + scene_folder
            print(command)
            os.system(command)
        continue
    for subcategory in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR_PATH + category):
        os.makedirs(GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH + category + "/" + subcategory, exist_ok=True)
        for scene_folder in os.listdir(GROCERY_DATA_NORMAL_GROUPED_DIR_PATH + category + "/" + subcategory):
            command = "ln -s " + GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH + scene_folder + " "\
            + GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH + category + "/" + subcategory + "/" + scene_folder
            print(command)
            os.system(command)
