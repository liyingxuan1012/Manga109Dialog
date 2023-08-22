import torch
import json


# load detected results
detected_origin_path = '/home/ace14550vm/checkpoints/test/inference/VG_stanford_filtered_with_attribute_test/'
detected_origin_result = torch.load(detected_origin_path + 'eval_results.pytorch')
detected_info = json.load(open(detected_origin_path + 'visual_info.json'))

vocab_file = json.load(open('/home/ace14550vm/Comic-SGG/datasets/vg/VG-SGG-dicts-with-attri.json'))

# get image info by index
def get_info_by_idx(idx, det_input, thres=0.5):
    groundtruth = det_input['groundtruths'][idx]
    prediction = det_input['predictions'][idx]
    # boxes
    boxes = groundtruth.bbox

    # object labels
    idx2label = vocab_file['idx_to_label']
    labels = ['{}-{}'.format(idx,idx2label[str(i)]) for idx, i in enumerate(groundtruth.get_field('labels').tolist())]
    pred_labels = ['{}-{}'.format(idx,idx2label[str(int(i))]) for idx, i in enumerate(prediction.get_field('pred_labels').tolist())]
    pred_scores = prediction.get_field('pred_scores')

    # groundtruth relation triplet
    idx2pred = vocab_file['idx_to_predicate']
    gt_rels = groundtruth.get_field('relation_tuple').tolist()
    gt_rels = [(labels[i[0]], idx2pred[str(i[2])], labels[i[1]]) for i in gt_rels]

    # prediction relation triplet
    pred_rel_pair = prediction.get_field('rel_pair_idxs').tolist()
    pred_rel_label = prediction.get_field('pred_rel_scores')
    pred_rel_label[:,0] = 0
    pred_rel_score, pred_rel_label = pred_rel_label.max(-1)

    # mask = pred_rel_score > thres
    # pred_rel_score = pred_rel_score[mask]
    # pred_rel_label = pred_rel_label[mask]

    pred_rels = [(pred_labels[int(i[0])], idx2pred[str(j)], pred_labels[int(i[1])]) for i, j in zip(pred_rel_pair, pred_rel_label.tolist()) if j!=0]
    return labels, pred_labels, pred_scores, gt_rels, pred_rels, pred_rel_score

def print_list(name, input_list, scores):
    for i, item in enumerate(input_list):
        if scores == None:
            print(name + ' ' + str(i) + ': ' + str(item))
        else:
            print(name + ' ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()))

def print_pred(name, pred, scores, pred_correct):
    for i, item in enumerate(pred):
        if item in pred_correct:
            print(str(name) + ' ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()))
        else:
            print('\033[31m' + str(name) + ' ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()) + '\033[0m')
    
def show_gt(labels, pred_labels, pred_scores, gt_rels, pred_rels, pred_rel_score):
    print('*' * 50)
    print_list('gt_boxes', labels, None)
    print('*' * 50)
    print_list('gt_rels', gt_rels, None)
    print('*' * 50)
    
def show_pred(labels, pred_labels, pred_scores, gt_rels, pred_rels, pred_rel_score):
    pred_labels_correct = list(set(labels).intersection(set(pred_labels)))
    print('*' * 50)
    print_pred('pred_labels', pred_labels, pred_scores, pred_labels_correct)
    print('*' * 50)
    print_list('gt_rels', gt_rels, None)
    print('*' * 50)
    # print_list('pred_rels', pred_rels[:20], pred_rel_score)
    # print('*' * 50)

    # select prediction that can cover all texts
    # text_list = [label for label in labels if 'text' in label]
    text_list = [gt_rel[2] for gt_rel in gt_rels]   # multiple speakers
    pred_list = [pred_rel[2] for pred_rel in pred_rels]
    indices = []
    for text in text_list:
        try:
            if pred_list.index(text) in indices:
                pred_list[pred_list.index(text)] = None
            indices.append(pred_list.index(text))
        except:
            pass
    pred_rels = [pred_rels[index] for index in indices]
    pred_correct = list(set(gt_rels).intersection(set(pred_rels)))  
    print_pred('pred_rels', pred_rels, pred_rel_score[indices], pred_correct)
    print('*' * 50)  

def show_selected(idx_list):
    for select_idx in idx_list:
        print(select_idx)
        # show_gt(*get_info_by_idx(select_idx, detected_origin_result))
        show_pred(*get_info_by_idx(select_idx, detected_origin_result))
        
def show_all(start_idx, length):
    for cand_idx in range(start_idx, start_idx+length):
        print(cand_idx)
        # show_gt(*get_info_by_idx(cand_idx, detected_origin_result))
        show_pred(*get_info_by_idx(cand_idx, detected_origin_result))

# show_all(start_idx=0, length=282)
show_selected([0])