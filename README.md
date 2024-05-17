# Manga109Dialog: A Large-scale Dialogue Dataset for Comics Speaker Detection

Official repository of Manga109Dialog (ICME 2024) |
[Paper](https://arxiv.org/abs/2306.17469) | [Dataset](https://github.com/manga109/public-annotations?tab=readme-ov-file#manga109dialog)

## Overview
To enhance the machine’s understanding of comics, we developed Manga109Dialog, which is the world’s largest speaker-to-text annotation dataset for comics. 
We proposed a novel deep learning-based method using scene graph generation (SGG) models, providing a challenging yet realistic benchmark for comics speaker detection.
The contributions of our work are summarized as follows.
- We constructed Manga109Dialog, an annotation dataset of associations between speakers and texts. This is the largest comics dialogue dataset in the world.
- We proposed a deep learning-based approach for comics speaker detection using SGG models. We enhance the performance by introducing frame information in the relationship prediction stage.
- We established a new benchmark for evaluation, setting a standard for future research in this domain.

<img width="919" alt="introduction" src="https://github.com/liyingxuan1012/Manga109Dialog/assets/81853956/0d7704ac-cd48-4eb3-b273-4cc794667f96">

## Prerequisites
- **Manga109 dataset**
    - Download from http://www.manga109.org/en/download.html
- **Manga109Dialog annotation**
    - Download from https://github.com/manga109/public-annotations

## Environment setup
Check [INSTALL.md](speaker_prediction/INSTALL.md) for installation instructions.

## Data preprocessing
Convert the annotations from Manga109 into a format suitable for the scene graph generation (SGG) models. 
For more details, check [README.md](preprocessing/README.md).

## Speaker prediction
This is the core part of our model. 
For details on how to detect characters and texts in comics and predict the speaker based on visual information, check  [README.md](speaker_prediction/README.md).

## Evaluation
In addition to conventional metrics for evaluating SGG models, we have introduced a new metric tailored for comics: **Recall@(#text)**.
```
# PredCls / SGCls
python eval_and_vis/eval_original.py

# SGDet
python eval_and_vis/eval_original_sgdet.py
```
You can find details on conventional evaluation metrics in [METRICS.md](https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch/blob/master/METRICS.md).

## Visualization
The visualization tools for predictions can be found in ``eval_and_vis/``.
- 1.visualize_PredCls_and_SGCls.ipynb
- 2.visualize_SGDet.ipynb
- 3.visualize_SGDet.ipynb
- 4.visualize_custom_SGDet.ipynb

## Citation
When using annotations of Manga109Dialog, please cite our paper.
```
@inproceedings{li2024manga109dialog,
  title={Manga109Dialog: A Large-scale Dialogue Dataset for Comics Speaker Detection},
  author={Li, Yingxuan and Aizawa, Kiyoharu and Matsui, Yusuke},
  booktitle={2024 IEEE International Conference on Multimedia and Expo (ICME)},
  year={2024},
  organization={IEEE}
}
```
