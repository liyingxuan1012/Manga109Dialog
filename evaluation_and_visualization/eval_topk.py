import torch
import json


# load detected results
detected_origin_path = '/home/ace14550vm/checkpoints/precls_motif/inference/VG_stanford_filtered_with_attribute_test/'
detected_origin_result = torch.load(detected_origin_path + 'eval_results.pytorch')

vocab_file = json.load(open('/home/ace14550vm/Comic-SGG/datasets/vg/VG-SGG-dicts-with-attri.json'))

# get image info by index
def get_info_by_idx(idx, det_input):
    groundtruth = det_input['groundtruths'][idx]
    prediction = det_input['predictions'][idx]

    # object labels
    idx2label = vocab_file['idx_to_label']
    labels = ['{}-{}'.format(idx,idx2label[str(i)]) for idx, i in enumerate(groundtruth.get_field('labels').tolist())]
    pred_labels = ['{}-{}'.format(idx,idx2label[str(int(i))]) for idx, i in enumerate(prediction.get_field('pred_labels').tolist())]
    # groundtruth relation triplet
    idx2pred = vocab_file['idx_to_predicate']
    gt_rels = groundtruth.get_field('relation_tuple').tolist()
    gt_rels = [(labels[i[0]], idx2pred[str(i[2])], labels[i[1]]) for i in gt_rels]

    # prediction relation triplet
    pred_rel_pair = prediction.get_field('rel_pair_idxs').tolist()
    pred_rel_label = prediction.get_field('pred_rel_scores')
    pred_rel_label[:,0] = 0
    pred_rel_score, pred_rel_label = pred_rel_label.max(-1)

    pred_rels = [(pred_labels[int(i[0])], idx2pred[str(j)], pred_labels[int(i[1])]) for i, j in zip(pred_rel_pair, pred_rel_label.tolist()) if j!=0]
    return gt_rels, pred_rels, pred_rel_score


start_idx = 0
length = 2990   # length = 2966 for 109 books

for k in [20,50,100]:
    num_pred_correct = 0
    num_gt_rels = 0
    recall = 0

    for cand_idx in range(start_idx, start_idx+length):
        gt_rels, pred_rels, pred_rel_score = get_info_by_idx(cand_idx, detected_origin_result)
        pred_rels = pred_rels[:k]
        pred_correct = list(set(gt_rels).intersection(set(pred_rels)))
        
        num_gt_rels += len(gt_rels)
        num_pred_correct += len(pred_correct)
        recall += len(pred_correct)/len(gt_rels)

    print('recall@%d: %.4f' %(k,recall/length))
    print('Recall@%d: '%k + str(num_pred_correct) + '/' + str(num_gt_rels) + ' = %.4f' %(num_pred_correct/num_gt_rels))
