import torch
import json


# load detected results
detected_origin_path = 'checkpoints/sgcls_motif/inference/VG_stanford_filtered_with_attribute_test/'
detected_origin_result = torch.load(detected_origin_path + 'eval_results.pytorch')
vocab_file = json.load(open('speaker_prediction/datasets/vg/VG-SGG-dicts-with-attri.json'))

start_idx = 0
length = 2990   # length = old:2966 easy:2970 medium:2990 hard:2022

num_labels = 0
num_labels_error = 0
num_page_error = 0

for idx in range(start_idx, start_idx+length):
    det_input = detected_origin_result
    groundtruth = det_input['groundtruths'][idx]
    prediction = det_input['predictions'][idx]

    # object labels
    idx2label = vocab_file['idx_to_label']
    labels = ['{}-{}'.format(idx,idx2label[str(i)]) for idx, i in enumerate(groundtruth.get_field('labels').tolist())]
    pred_labels = ['{}-{}'.format(idx,idx2label[str(int(i))]) for idx, i in enumerate(prediction.get_field('pred_labels').tolist())]
    pred_scores = prediction.get_field('pred_scores')
    pred_labels_error = list(set(pred_labels).difference(set(labels)))

    num_labels += len(labels)
    if len(pred_labels_error)!=0:
        print(idx)
        num_labels_error += len(pred_labels_error)
        num_page_error += 1

print(str(num_labels_error) + '/' + str(num_labels) + ' = %.4f' %(num_labels_error/num_labels))
print(str(num_page_error) + '/' + str(length) + ' = %.4f' %(num_page_error/length))