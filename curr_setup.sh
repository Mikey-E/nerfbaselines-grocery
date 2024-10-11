#nerfbaselines train --method gaussian-opacity-fields --data /cluster/medbow/home/melgin/tmp_candelete/04_19_2024_W_F_Sugar_P_2_changed_input --output /cluster/medbow/project/3dllms/melgin/nerfbaselines-grocery/results/poc_gof_sugar_changed_input1

#Setup for 2dgs
#conda remove --prefix /project/3dllms/melgin/conda/envs/conda-envs/2d-gaussian-splatting/6fddd194c2e0d4432a95071a67ac3f539cea8667abb76d609a0f0c2f1f7cfc24/2d-gaussian-splatting --all -y
#export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
#export CURR_DATA_DIR=$GROCERY_DATA_CONVERTED_DIR
#nerfbaselines train --method 2d-gaussian-splatting --data ${CURR_DATA_DIR}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR}poc_2dgs_${CURR_SCENE}

#Setup for zipnerf
export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
export CURR_DATA_DIR=$GROCERY_DATA_NORMAL_DIR
nerfbaselines train --method zipnerf --data ${CURR_DATA_DIR}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR}poc_zn_${CURR_SCENE}
