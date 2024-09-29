#Author: Michael Elgin
#Serial implementation, hopefully this only ever has to be run once

import sys
import os

grouped_path = "/project/3dllms/DATASETS/CONVERTED/GROUPED/"
ungrouped_path = "/project/3dllms/DATASETS/CONVERTED/UNGROUPED/"

for category in os.listdir(grouped_path):
    if category == "Random":
        command = "cp -r " + grouped_path + "/Random/* " + ungrouped_path
        print(command)
        os.system(command)
        continue
    for subcategory in os.listdir(grouped_path + category):
        command = "cp -r " + grouped_path + category + "/" + subcategory + "/* " + ungrouped_path
        print(command)
        os.system(command)
