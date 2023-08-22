import torch
import h5py
import json
import csv
import numpy as np


roidb_file = "/home/ace14550vm/Comic-SGG/datasets/vg/VG-SGG-with-attri-frame.h5"
image_file = "/home/ace14550vm/Comic-SGG/datasets/vg/image_data.json"
det_input = torch.load("/groups/gcc50494/home/li/pretrained_faster_rcnn_frame/inference/VG_stanford_filtered_with_attribute_test/eval_results.pytorch")

roi_h5 = h5py.File(roidb_file, 'r')
data_split = roi_h5['split'][:]
split_mask = data_split == 2

# Filter out images without bounding boxes
split_mask &= roi_h5['img_to_first_box'][:] >= 0
split_mask &= roi_h5['img_to_first_rel'][:] >= 0

image_index = np.where(split_mask)[0]
split_mask = np.zeros_like(data_split).astype(bool)
split_mask[image_index] = True

# Get filename
with open(image_file, 'r') as f:
    im_data = json.load(f)

filenames = []
for i, img in enumerate(im_data):
    filenames.append(img['image_id'])
filenames = [filenames[i] for i in np.where(split_mask)[0]]

with open('./frame_detection.csv', 'w') as csvfile:
    fileheader = ["index","xmin","ymin","xmax","ymax"]
    writer = csv.DictWriter(csvfile, fileheader)
    writer.writeheader()

    for index in range(len(image_index)):
        prediction = det_input['predictions'][index]
        for box in prediction.bbox:
            box = box.tolist()
            writer.writerow({"index":filenames[index],"xmin":round(box[0],2),"ymin":round(box[1],2),"xmax":round(box[2],2),"ymax":round(box[3],2)})

        