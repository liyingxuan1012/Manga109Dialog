# Speaker prediction

This repository contains the source code for our speaker prediction model. The scene graph generation (SGG) component of our model is primarily based on the[Scene-Graph-Benchmark](https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch). For a deeper understanding of the SGG component, please consult the detailed documentation available at [Scene Graph Benchmark in Pytorch](https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch/blob/master/README.md).

## Pre-training
```
mkdir pretrained_model
bash comic_sgg_pretrain.sh
```

## How to run
### Three protocols
There are three standard protocols for SGG tasks: 

(1) Predicate Classification (PredCls): taking ground truth bounding boxes and labels as inputs, 

(2) Scene Graph Classification (SGCls) : using ground truth bounding boxes without labels, 

(3) Scene Graph Detection (SGDet): detecting SGs from scratch. 

We use two switches `MODEL.ROI_RELATION_HEAD.USE_GT_BOX` and `MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL` to select the protocols.

For **Predicate Classification (PredCls)**, we need to set:
```
MODEL.ROI_RELATION_HEAD.USE_GT_BOX True MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL True
```
For **Scene Graph Classification (SGCls)**:
```
MODEL.ROI_RELATION_HEAD.USE_GT_BOX True MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False
```
For **Scene Graph Detection (SGDet)**:
```
MODEL.ROI_RELATION_HEAD.USE_GT_BOX False MODEL.ROI_RELATION_HEAD.USE_GT_OBJECT_LABEL False
```

### Training
```
mkdir checkpoints
bash comic_sgg.sh
```

### Test
```
bash comic_sgg_test.sh
```
