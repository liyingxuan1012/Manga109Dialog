import torch
import json
import numpy as np
from scipy.spatial import distance


# load detected results
detected_origin_path = '/home/ace14550vm/checkpoints/precls_motif/inference/VG_stanford_filtered_with_attribute_test/'
detected_origin_result = torch.load(detected_origin_path + 'eval_results.pytorch')
detected_attri_path = '/home/ace14550vm/checkpoints/precls_motif_frame/inference/VG_stanford_filtered_with_attribute_test/'
detected_attri_result = torch.load(detected_attri_path + 'eval_results.pytorch')

vocab_file = json.load(open('/home/ace14550vm/Comic-SGG/datasets/vg/VG-SGG-dicts-with-attri.json'))

# get image info by index
def get_info_by_idx(idx, det_input, thres=0.5):
    groundtruth = det_input['groundtruths'][idx]
    prediction = det_input['predictions'][idx]
    # boxes
    boxes = prediction.bbox
    # attributes
    attributes = prediction.get_field('attributes')[:,0].tolist()
    
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
    return boxes, attributes, labels, pred_labels, gt_rels, pred_rels, pred_rel_score

def print_list(name, input_list, scores):
    for i, item in enumerate(input_list):
        if scores == None:
            print(name + ' ' + str(i) + ': ' + str(item))
        else:
            print(name + ' ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()))

def print_pred(pred_rels, scores, pred_correct,pred_different):
    for i, item in enumerate(pred_rels):
        if item in pred_correct:
            if item in pred_different:
                print('\033[32mpred_rels ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()) + '\033[0m')
            else:
                print('pred_rels ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()))
        else:
            print('\033[31mpred_rels ' + str(i) + ': ' + str(item) + '; score: ' + str(scores[i].item()) + '\033[0m')

def show_gt(boxes, labels, gt_rels, pred_rels, pred_rel_score):
    print('*' * 50)
    print_list('gt_boxes', labels, None)
    print('*' * 50)
    print_list('gt_rels', gt_rels, None)
    print('*' * 50)

def rule_based(boxes, attributes, pred_labels, text_list, frame_dis=True):
    char_coords = np.array([])
    text_coords = np.array([])
    dis_rels = []

    num_obj = boxes.shape[0]
    for i in range(num_obj):
        box = boxes[i]
        pred_label = pred_labels[i]
        attribute = attributes[i]

        x1,y1,x2,y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])

        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2

        if 'character' in pred_label:
            char_coords = np.append(char_coords,[x_center,y_center,attribute,pred_label])
        if 'text' in pred_label and pred_label in text_list:
            text_coords = np.append(text_coords,[x_center,y_center,attribute,pred_label])

    char_coords = char_coords.reshape(-1,4)
    text_coords = text_coords.reshape(-1,4)

    for text in text_coords:
        frame_order = text[2]
        # find charactor in the same frame
        if frame_dis and frame_order != 0:
            char_tmp = char_coords[char_coords[:,2]==frame_order,:]
            if len(char_tmp) == 0:
                char_tmp = char_coords
        else:
            char_tmp = char_coords

        char_coord = char_tmp[:,:-2].astype(float)
        text_coord = text[np.newaxis,:-2].astype(float)

        # speaker prediction
        char = char_tmp[np.argmin(distance.cdist(text_coord, char_coord),axis=1)][0,:]
        dis_rels.append((char[-1], 'says', text[-1]))
    return dis_rels

start_idx = 0
length = 2990    # length = old:2966 easy:2970 medium:2990 hard:2022

num_gt_rels = 0
num_pred_correct = 0
num_pred_different = 0

for cand_idx in range(start_idx, start_idx+length):
    # # show_gt(*get_info_by_idx(cand_idx, detected_origin_result))
    # boxes, attributes, labels, pred_labels, gt_rels, pred_rels, pred_rel_score = get_info_by_idx(cand_idx, detected_origin_result) 
    # # select prediction that can cover all texts
    # text_list = [gt_rel[2] for gt_rel in gt_rels]   # multiple speakers
    # pred_list = [pred_rel[2] for pred_rel in pred_rels]
    # indices = []
    # for text in text_list:
    #     try:
    #         if pred_list.index(text) in indices:
    #             pred_list[pred_list.index(text)] = None
    #         indices.append(pred_list.index(text))
    #     except:
    #         pass
    # pred_rels = [pred_rels[index] for index in indices]
    # pred_correct = list(set(gt_rels).intersection(set(pred_rels)))  

    # results using attritubes
    boxes, attributes, labels, pred_labels, gt_rels, pred_rels, pred_rel_score = get_info_by_idx(cand_idx, detected_attri_result)  
    # select prediction that can cover all texts
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
    pred_correct_attri = list(set(gt_rels).intersection(set(pred_rels)))  

    # make prediction by distance
    dis_rels = rule_based(boxes, attributes, pred_labels, text_list, frame_dis=True)
    pred_correct_dis = list(set(gt_rels).intersection(set(dis_rels)))

    # pred_different = list(set(pred_correct_attri).difference(set(pred_correct)))
    
    num_gt_rels += len(gt_rels)
    num_pred_correct += len(pred_correct_attri)
    num_pred_different += len(pred_correct_dis)
    # num_pred_different += len(pred_different)

    # if len(pred_correct_attri) == len(gt_rels) and len(pred_correct_attri) > len(pred_correct) > len(pred_correct_dis):
    #     print(cand_idx)
    #     print(len(gt_rels), len(pred_correct_attri), len(pred_correct), len(pred_correct_dis))

print(str(num_pred_correct) + '/' + str(num_gt_rels) + ' = %.4f' %(num_pred_correct/num_gt_rels))
# print(str(num_pred_different) + '/' + str(num_pred_correct) + ' = %.4f' %(num_pred_different/num_pred_correct))
print(str(num_pred_different) + '/' + str(num_gt_rels) + ' = %.4f' %(num_pred_different/num_gt_rels))