# Manga109Dialog: A Large-scale Dialogue Dataset for Comics Speaker Detection

Official repository of Manga109Dialog (ICME 2024) |
[Paper](https://arxiv.org/abs/2306.17469) | [Dataset](https://github.com/manga109/public-annotations?tab=readme-ov-file#manga109dialog)
### Prerequisites
- **Manga109 dataset**
    - Download from http://www.manga109.org/en/download.html
- **Manga109 Dialog annotation**
    - Download from https://github.com/manga109/public-annotations

### Data preprocessing
Check [README.md](preprocessing/README.md).

### Environment setup
Check [INSTALL.md](speaker_prediction/INSTALL.md) for installation instructions.

### How to run
```
# Training
bash comic_sgg.sh

# Test
bash comic_sgg_test.sh
```

### Evaluation
```
# PredCls / SGCls
python evaluation_and_visualization/eval_original.py

# SGDet
python evaluation_and_visualization/eval_original_sgdet.py
```

### Visualization
The visualization tools for predictions can be found in ``evaluation_and_visualization/``.
- 1.visualize_PredCls_and_SGCls.ipynb
- 2.visualize_SGDet.ipynb
- 3.visualize_SGDet.ipynb
- 4.visualize_custom_SGDet.ipynb

### Citation
When using annotations of Manga109Dialog, please cite our paper.
```
@misc{li2023manga109dialog,
      title={Manga109Dialog A Large-scale Dialogue Dataset for Comics Speaker Detection}, 
      author={Yingxuan Li and Kiyoharu Aizawa and Yusuke Matsui},
      year={2023},
      eprint={2306.17469},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
