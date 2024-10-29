#!/bin/bash

#This file is to print out all scene names in a results folder that are missing a results file.

#A (likely) example: from within a results folder:
#	nerfbaselines_grocery/results/model$ . ../../utils/<this_file> results-30000.json

#Do not do results-*.json; you want the explicit (full) name

#remember to redirect the output to some other location so as to not litter the results folder(s)
#	> ~/tmp_candelete/unsuccessful_scenes_in_model.txt

file_to_check="$1"
for dir in */; do
  if [[ ! -f "$dir/$file_to_check" ]]; then
    echo "$dir"
  fi
done
