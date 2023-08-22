#!/bin/bash

source activate scene_graph_benchmark
cd /home/ace14550vm/Comic-SGG

python tools/relation_test_net.py --config-file "configs/e2e_relation_X_101_32_8_FPN_1x.yaml" MODEL.ROI_RELATION_HEAD.USE_GT_BOX False MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False MODEL.ROI_RELATION_HEAD.PREDICTOR MotifPredictor TEST.IMS_PER_BATCH 1 GLOVE_DIR /home/ace14550vm/glove MODEL.PRETRAINED_DETECTOR_CKPT /home/ace14550vm/checkpoints/sgdet_motif OUTPUT_DIR /home/ace14550vm/checkpoints/sgdet_motif TEST.CUSTUM_EVAL True TEST.CUSTUM_PATH /home/ace14550vm/demo/custom_images DETECTED_SGG_DIR /home/ace14550vm/demo/custom_images_output MODEL.DEVICE cpu
