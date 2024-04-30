#!/bin/bash
source .bashrc
conda activate scene_graph_benchmark
CUDA_VISIBLE_DEVICES=0 python speaker_prediction/tools/relation_train_net.py --config-file "speaker_prediction/configs/e2e_relation_X_101_32_8_FPN_1x.yaml" MODEL.ROI_RELATION_HEAD.USE_GT_BOX True MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False MODEL.ATTRIBUTE_ON False MODEL.ROI_RELATION_HEAD.PREDICTOR MotifPredictor SOLVER.IMS_PER_BATCH 4 TEST.IMS_PER_BATCH 1 SOLVER.MAX_ITER 50000 SOLVER.VAL_PERIOD 2000 SOLVER.CHECKPOINT_PERIOD 2000 GLOVE_DIR glove MODEL.PRETRAINED_DETECTOR_CKPT pretrained_model/pretrained_faster_rcnn_test/model_final.pth OUTPUT_DIR checkpoints/sgcls_motif_frame_detection
