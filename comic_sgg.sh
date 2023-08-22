#!/bin/bash

#$-l rt_AG.small=1
#$-l h_rt=2:00:00
#$-j y
#$-cwd

source /home/ace14550vm/.bashrc
module load gcc/9.3.0 cuda/11.3/11.3.1 cudnn/8.2/8.2.4
conda activate scene_graph_benchmark
cd Comic-SGG
CUDA_VISIBLE_DEVICES=0 python tools/relation_train_net.py --config-file "configs/e2e_relation_X_101_32_8_FPN_1x.yaml" MODEL.ROI_RELATION_HEAD.USE_GT_BOX True MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False MODEL.ATTRIBUTE_ON False MODEL.ROI_RELATION_HEAD.PREDICTOR MotifPredictor SOLVER.IMS_PER_BATCH 4 TEST.IMS_PER_BATCH 1 SOLVER.MAX_ITER 50000 SOLVER.VAL_PERIOD 2000 SOLVER.CHECKPOINT_PERIOD 2000 GLOVE_DIR /home/ace14550vm/glove MODEL.PRETRAINED_DETECTOR_CKPT /groups/gcc50494/home/li/pretrained_faster_rcnn_test/model_final.pth OUTPUT_DIR /home/ace14550vm/checkpoints/sgcls_motif_frame_detection
