#!/bin/bash

#$-l rt_AG.small=1
#$-l h_rt=12:00:00
#$-j y
#$-cwd

source .bashrc
module load gcc/9.3.0 cuda/11.3/11.3.1 cudnn/8.2/8.2.4
conda activate scene_graph_benchmark
cd speaker_prediction
CUDA_VISIBLE_DEVICES=0 python tools/detector_pretrain_net.py --config-file "configs/e2e_relation_detector_X_101_32_8_FPN_1x.yaml" SOLVER.IMS_PER_BATCH 4 TEST.IMS_PER_BATCH 1 SOLVER.MAX_ITER 50000 SOLVER.STEPS "(30000, 45000)" SOLVER.VAL_PERIOD 2000 SOLVER.CHECKPOINT_PERIOD 2000 MODEL.RELATION_ON False MODEL.ATTRIBUTE_ON False OUTPUT_DIR pretrained_model/pretrained_faster_rcnn_ebd SOLVER.PRE_VAL False