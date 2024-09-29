#Author: Michael Elgin
#POC file for multiple training runs

import os
import sys

#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Avacados"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Coconuts"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/GrapeFruits"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Bananas"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Apples"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Lemons"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Plums" #only 2 subfolders
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Mangoes"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/MultiFruits"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Nectarines"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Orange"
#base_path = "/project/3dllms/DATASETS/GROUPED/Fruits/Pears"

#base_path = "/project/3dllms/DATASETS/GROUPED/"
base_path = "/project/3dllms/DATASETS/CONVERTED/"
base_path += sys.argv[1]

#resume = "04_04_2024_W_C_Melons2_F_1"
#found = False

for folder in os.listdir(base_path):
#    if folder != resume and found == False:
#        continue
#    else:
#        found = True
#    command = "nerfbaselines train --method nerfacto --data " + base_path + "/" + folder + \
#        " --output results/nerfacto_" + folder
#    command = "nerfbaselines train --method gaussian-opacity-fields --data " + base_path + "/" + folder + \
#        " --output results/gof_" + folder
#    command = "nerfbaselines train --method gaussian-splatting --data " + base_path + "/" + folder + \
#        " --output results/gs_" + folder
    command = "nerfbaselines train --method mip-splatting --data " + base_path + "/" + folder + \
        " --output results/ms_" + folder
    print("Starting: " + command)
    os.system(command)
