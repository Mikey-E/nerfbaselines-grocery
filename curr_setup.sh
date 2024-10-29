#nerfbaselines train --method gaussian-opacity-fields --data /cluster/medbow/home/melgin/tmp_candelete/04_19_2024_W_F_Sugar_P_2_changed_input --output /cluster/medbow/project/3dllms/melgin/nerfbaselines-grocery/results/poc_gof_sugar_changed_input1

#Setup for 2dgs
#conda remove --prefix /project/3dllms/melgin/conda/envs/conda-envs/2d-gaussian-splatting/6fddd194c2e0d4432a95071a67ac3f539cea8667abb76d609a0f0c2f1f7cfc24/2d-gaussian-splatting --all -y
#export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
#export CURR_SCENE="04_19_2024_W_F_Spices_P_2/"
#export CURR_DATA_DIR_PATH=$GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH
#nerfbaselines train --method 2d-gaussian-splatting --data ${CURR_DATA_DIR_PATH}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR_PATH}poc_2dgs_${CURR_SCENE}

#Setup for zipnerf
#export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
#export CURR_DATA_DIR_PATH=$GROCERY_DATA_NORMAL_UNGROUPED_DIR_PATH
#nerfbaselines train --method zipnerf --data ${CURR_DATA_DIR_PATH}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR_PATH}poc_zn_${CURR_SCENE}

#Setup for instant-ngp ablation _2
#export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
#export CURR_DATA_DIR_PATH=$GROCERY_DATA_NORMAL_UNGROUPED_DIR_PATH
#nerfbaselines train --method instant-ngp --data ${CURR_DATA_DIR_PATH}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR_PATH}poc_ingp2_${CURR_SCENE}

#Setup for gaussian-splatting ablation new env
#export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
#export CURR_DATA_DIR_PATH=$GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH
#nerfbaselines train --method gaussian-splatting --data ${CURR_DATA_DIR_PATH}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR_PATH}poc_gs_${CURR_SCENE}

#Setup for mip-splatting ablation new env
#export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
#export CURR_DATA_DIR_PATH=$GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH
#nerfbaselines train --method mip-splatting --data ${CURR_DATA_DIR_PATH}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR_PATH}poc_ms_${CURR_SCENE}_8

#Setup for scaffold-gs model
export CURR_SCENE="04_19_2024_W_F_Sugar_P_2/"
export CURR_DATA_DIR_PATH=$GROCERY_DATA_CONVERTED_UNGROUPED_DIR_PATH
#export CURR_DATA_DIR_PATH=$GROCERY_DATA_NORMAL_UNGROUPED_DIR_PATH
nerfbaselines train --method scaffold-gs --data ${CURR_DATA_DIR_PATH}${CURR_SCENE} --output ${GROCERY_RESULTS_DIR_PATH}poc_sgs_${CURR_SCENE}
