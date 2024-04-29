# Manga109Dialog: A Large-scale Dialogue Dataset for Comics Speaker Detection

Official repository of Manga109Dialog (ICME 2024) |
[Paper](https://arxiv.org/abs/2306.17469) | [Dataset](https://github.com/manga109/public-annotations?tab=readme-ov-file#manga109dialog)
## Prerequisites
- **Manga109 dataset**
    - Download from http://www.manga109.org/en/download.html
- **Manga109Dialog annotation**
    - Download from https://github.com/manga109/public-annotations

## Environment setup
Check [INSTALL.md](speaker_prediction/INSTALL.md) for installation instructions.

## Data preprocessing
Check [README.md](preprocessing/README.md).

## Speaker prediction
```
Check [README.md](speaker_prediction/README.md).
```

## Evaluation
```
# PredCls / SGCls
python eval_and_vis/eval_original.py

# SGDet
python eval_and_vis/eval_original_sgdet.py
```

## Visualization
The visualization tools for predictions can be found in ``eval_and_vis/``.
- 1.visualize_PredCls_and_SGCls.ipynb
- 2.visualize_SGDet.ipynb
- 3.visualize_SGDet.ipynb
- 4.visualize_custom_SGDet.ipynb

### Citation
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
