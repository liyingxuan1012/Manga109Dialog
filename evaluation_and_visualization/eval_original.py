import torch
import json


# load detected results
detected_origin_path = '/home/ace14550vm/checkpoints/precls_motif_frame/inference/VG_stanford_filtered_with_attribute_test/'
detected_origin_result = torch.load(detected_origin_path + 'eval_results.pytorch')

vocab_file = json.load(open('/home/ace14550vm/Comic-SGG/datasets/vg/VG-SGG-dicts-with-attri.json'))

# get image info by index
def get_info_by_idx(idx, det_input, thres=0.5):
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

    # filter prediction results by score
    # mask = pred_rel_score > thres
    # pred_rel_score = pred_rel_score[mask]
    # pred_rel_label = pred_rel_label[mask]
    pred_rels = [(pred_labels[int(i[0])], idx2pred[str(j)], pred_labels[int(i[1])]) for i, j in zip(pred_rel_pair, pred_rel_label.tolist()) if j!=0]
    return labels, gt_rels, pred_rels, pred_rel_score


start_idx = 0
length = 2990    # length = old:2966 easy:2970 medium:2990 hard:2022

num_gt_rels = 0
num_pred_correct = 0

for cand_idx in range(start_idx, start_idx+length):
    labels, gt_rels, pred_rels, pred_rel_score = get_info_by_idx(cand_idx, detected_origin_result)
    
    # determine the range of pred_rels
    # method1
    # pred_rels = pred_rels[:len(gt_rels)]
    # method2
    # text_list = [label for label in labels if 'text' in label]
    text_list = [gt_rel[2] for gt_rel in gt_rels]   # multiple speakers
    pred_list = [pred_rel[2] for pred_rel in pred_rels]
    indices = []
    for text in text_list:
        try:
            if pred_list.index(text) in indices:
                # print(cand_idx)
                pred_list[pred_list.index(text)] = None
            indices.append(pred_list.index(text))
        except:
            pass
    pred_rels = [pred_rels[index] for index in indices]

    pred_correct = list(set(gt_rels).intersection(set(pred_rels)))
    
    num_gt_rels += len(gt_rels)
    num_pred_correct += len(pred_correct)
    
print('Recall: ' + str(num_pred_correct) + '/' + str(num_gt_rels) + ' = %.4f' %(num_pred_correct/num_gt_rels))
