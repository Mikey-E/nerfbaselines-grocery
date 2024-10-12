#This file contains important env vars to be activated whenever the nerfbaselines conda env is activated.
#Hence in the etc/conda/activate.d directory for that conda env, soft-link to this file so that it is
#run upon activation

#Nerfbaselines creates new conda environments for each model it will train. This var says where to put these.
#At this location it will create a new directory "conda-envs" and place them within
export NERFBASELINES_PREFIX=/project/3dllms/melgin/conda/envs/

#Where the nerfbaselines sourcecode has been cloned
export NERFBASELINES_HOME_DIR_PATH=/project/3dllms/melgin/nerfbaselines-grocery/

#Location of data for models that require converted data according to convert.py, flat (ungrouped)
export GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH=/project/3dllms/DATASETS/CONVERTED/CONVERTED/UNGROUPED/

#Location of data for models that require converted data according to convert.py, hierarchical grouped
export GROCERY_DATA_CONVERTED_GROUPED_DIR_PATH=/project/3dllms/DATASETS/CONVERTED/CONVERTED/GROUPED/

#Location of data for models that work with our normal format, flat (ungrouped)
export GROCERY_DATA_NORMAL_UNGROUPED_DIR_PATH=/project/3dllms/DATASETS/CONVERTED/NORMAL/UNGROUPED/

#Location of data for models that work with our normal format, hierarchical grouped
export GROCERY_DATA_NORMAL_GROUPED_DIR_PATH=/project/3dllms/DATASETS/CONVERTED/NORMAL/GROUPED/

#Location of where to place results from training runs
export GROCERY_RESULTS_DIR_PATH=${NERFBASELINES_HOME_DIR_PATH}results/

#Location of where to place log files from training runs
export GROCERY_LOGS_DIR_PATH=${NERFBASELINES_HOME_DIR_PATH}logs/

#Location of where to place csv files generated from results
export GROCERY_CSVS_DIR_PATH=${NERFBASELINES_HOME_DIR_PATH}csv/csv_results/

#Ensure that the location of the cloned nerfbaselines code is part of where to look for imports.
#This is necessary for utils etc
export PYTHONPATH=${NERFBASELINES_HOME_DIR_PATH}:${PYTHONPATH}
