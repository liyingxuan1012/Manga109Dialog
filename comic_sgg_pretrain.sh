#!/bin/bash
source .bashrc
conda activate scene_graph_benchmark
CUDA_VISIBLE_DEVICES=0 python speaker_prediction/tools/detector_pretrain_net.py --config-file "speaker_prediction/configs/e2e_relation_detector_X_101_32_8_FPN_1x.yaml" SOLVER.IMS_PER_BATCH 4 TEST.IMS_PER_BATCH 1 SOLVER.MAX_ITER 50000 SOLVER.STEPS "(30000, 45000)" SOLVER.VAL_PERIOD 2000 SOLVER.CHECKPOINT_PERIOD 2000 MODEL.RELATION_ON False MODEL.ATTRIBUTE_ON False OUTPUT_DIR pretrained_model/pretrained_faster_rcnn_ebd SOLVER.PRE_VAL False
