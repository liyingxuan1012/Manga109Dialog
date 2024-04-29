#!/bin/bash

#$-l rt_AG.small=1
#$-l h_rt=01:00:00
#$-j y
#$-cwd

source .bashrc
module load gcc/9.3.0 cuda/11.3/11.3.1 cudnn/8.2/8.2.4
conda activate scene_graph_benchmark
cd speaker_prediction
CUDA_VISIBLE_DEVICES=0 python tools/relation_test_net.py --config-file "configs/e2e_relation_X_101_32_8_FPN_1x.yaml" MODEL.ROI_RELATION_HEAD.USE_GT_BOX True MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False MODEL.ATTRIBUTE_ON False MODEL.ROI_RELATION_HEAD.PREDICTOR MotifPredictor TEST.IMS_PER_BATCH 1 GLOVE_DIR glove MODEL.PRETRAINED_DETECTOR_CKPT checkpoints/sgcls_motif_frame_detection OUTPUT_DIR checkpoints/sgcls_motif_frame_detection

# CUDA_VISIBLE_DEVICES=0 python tools/relation_test_net.py --config-file "configs/e2e_relation_X_101_32_8_FPN_1x_transformer.yaml" MODEL.ROI_RELATION_HEAD.USE_GT_BOX True MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL True MODEL.ATTRIBUTE_ON False MODEL.ROI_RELATION_HEAD.PREDICTOR TransformerPredictor TEST.IMS_PER_BATCH 1 GLOVE_DIR glove MODEL.PRETRAINED_DETECTOR_CKPT checkpoints/precls_trans OUTPUT_DIR checkpoints/precls_trans
# CUDA_VISIBLE_DEVICES=0 python tools/relation_test_net.py --config-file "configs/e2e_relation_X_101_32_8_FPN_1x.yaml" MODEL.ROI_RELATION_HEAD.USE_GT_BOX False MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False MODEL.ROI_RELATION_HEAD.PREDICTOR MotifPredictor TEST.IMS_PER_BATCH 1 GLOVE_DIR glove MODEL.PRETRAINED_DETECTOR_CKPT checkpoints/sgdet_motif OUTPUT_DIR checkpoints/sgdet_motif TEST.CUSTUM_EVAL True TEST.CUSTUM_PATH checkpoints/custom_images DETECTED_SGG_DIR checkpoints/custom_images_output
