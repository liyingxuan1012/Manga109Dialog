import torch
import json
import numpy as np
from functools import reduce
from maskrcnn_benchmark.data.datasets.evaluation.vg.sgg_eval import _compute_pred_matches


# load detected results
detected_origin_path = '/home/ubuntu/checkpoints/sgdet_motif/inference/VG_stanford_filtered_with_attribute_test/'
detected_origin_result = torch.load(detected_origin_path + 'eval_results.pytorch')
detected_info = json.load(open(detected_origin_path + 'visual_info.json'))

vocab_file = json.load(open('/home/ubuntu/Comic-SGG/datasets/vg/VG-SGG-dicts-with-attri.json'))

# get image info by index
def get_info(idx, det_input):
    groundtruth = det_input['groundtruths'][idx]
    prediction = det_input['predictions'][idx]
    # boxes
    boxes = groundtruth.bbox
    boxes = np.array(boxes)
    pred_boxes = prediction.bbox
    pred_boxes = np.array(pred_boxes)

    # object labels
    idx2label = {"0": "_background_"}
    idx2label.update(vocab_file['idx_to_label'])
    labels = [idx2label[str(i)] for i in groundtruth.get_field('labels').tolist()]
    pred_labels = [idx2label[str(int(i))] for i in prediction.get_field('pred_labels').tolist()]

    # groundtruth relation triplet
    idx2pred = vocab_file['idx_to_predicate']
    gt_rels = groundtruth.get_field('relation_tuple').tolist()
    gt_boxes_pairs = [np.hstack((boxes[i[0]], boxes[i[1]])) for i in gt_rels]
    gt_boxes_pairs = np.array(gt_boxes_pairs)
    gt_rels = [(labels[i[0]], idx2pred[str(i[2])], labels[i[1]]) for i in gt_rels]
    gt_rels = np.array(gt_rels)

    # prediction relation triplet
    pred_rel_pair = prediction.get_field('rel_pair_idxs').tolist()
    pred_rel_label = prediction.get_field('pred_rel_scores')
    pred_rel_label[:,0] = 0
    pred_rel_score, pred_rel_label = pred_rel_label.max(-1)

    pred_boxes_pairs = [np.hstack((pred_boxes[int(i[0])], pred_boxes[int(i[1])])) for i in pred_rel_pair]
    pred_boxes_pairs = np.array(pred_boxes_pairs)
    pred_rels = [(pred_labels[int(i[0])], idx2pred[str(j)], pred_labels[int(i[1])]) for i, j in zip(pred_rel_pair, pred_rel_label.tolist()) if j!=0]
    pred_rels = np.array(pred_rels)

    return gt_rels, pred_rels, gt_boxes_pairs, pred_boxes_pairs

start_idx = 0
length = 2990   # length = 2966 for 109 books

for k in [20]:
    num_pred_correct = 0
    num_gt_rels = 0
    recall = 0

    for cand_idx in range(start_idx, start_idx+length):
        gt_rels, pred_rels, gt_boxes_pairs, pred_boxes_pairs = get_info(cand_idx, detected_origin_result)
        pred_to_gt = _compute_pred_matches(
                        gt_rels,
                        pred_rels,
                        gt_boxes_pairs,
                        pred_boxes_pairs,
                        iou_thres=0.65,
                        phrdet=False,
                    )
        pred_correct = reduce(np.union1d, pred_to_gt[:k])

        num_gt_rels += len(gt_rels)
        num_pred_correct += len(pred_correct)
        recall += len(pred_correct)/len(gt_rels)

    print('recall@%d: %.4f' %(k,recall/length))
    print('Recall@%d: '%k + str(num_pred_correct) + '/' + str(num_gt_rels) + ' = %.4f' %(num_pred_correct/num_gt_rels))
