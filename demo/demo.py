import os
import shutil
import time
import subprocess
import json
import streamlit as st
from PIL import Image, ImageDraw, ImageFont


def load_image(image_folder_path):
    uploaded_file = st.file_uploader(label='Pick an image to test', type='jpg')
    
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)

        # download images to local
        image_path = image_folder_path + uploaded_file.name
        with open(image_path,'wb') as f:
            f.write(image_data)
 

def load_pred(pred_path, data_info_path):
    custom_prediction = json.load(open(pred_path))
    custom_data_info = json.load(open(data_info_path))

    image_idx = 0
    ind_to_classes = custom_data_info['ind_to_classes']
    ind_to_predicates = custom_data_info['ind_to_predicates']

    image_path = custom_data_info['idx_to_files'][image_idx]
    boxes = custom_prediction[str(image_idx)]['bbox']
    box_labels = custom_prediction[str(image_idx)]['bbox_labels']
    box_scores = custom_prediction[str(image_idx)]['bbox_scores']
    all_rel_labels = custom_prediction[str(image_idx)]['rel_labels']
    all_rel_scores = custom_prediction[str(image_idx)]['rel_scores']
    all_rel_pairs = custom_prediction[str(image_idx)]['rel_pairs']

    for i in range(len(box_labels)):
        box_labels[i] = str(i) + '_' + ind_to_classes[box_labels[i]]

    rel_labels = []
    rel_scores = []
    indices = []
    for i in range(len(all_rel_pairs)):
        # select prediction that can cover all texts
        if 'text' in box_labels[all_rel_pairs[i][1]] and all_rel_pairs[i][1] not in indices:
            indices.append(all_rel_pairs[i][1])
            rel_scores.append(all_rel_scores[i])
            label = (box_labels[all_rel_pairs[i][0]], ind_to_predicates[all_rel_labels[i]], box_labels[all_rel_pairs[i][1]])
            rel_labels.append(label)
        else:
            continue

    draw_image(image_path, boxes, box_labels, rel_labels, box_scores=box_scores, rel_scores=rel_scores)
    st.text('*' * 50)
    print_list('box_labels', box_labels, box_scores)
    st.text('*' * 50)
    print_list('rel_labels', rel_labels, rel_scores)
    st.text('*' * 50)


def print_list(name, input_list, scores=None):
    for i, item in enumerate(input_list):
        text = name + ' ' + str(i) + ': ' + str(item) + '; score: %.4f' %scores[i]
        st.markdown('<p style="font-size: 14pt; line-height: 6pt">%s</p>'% text, unsafe_allow_html=True)
    

def draw_image(img_path, boxes, box_labels, rel_labels, box_scores=None, rel_scores=None):
    size = get_size(Image.open(img_path).size)
    pic = Image.open(img_path).resize(size)
    font = ImageFont.truetype('/home/ace14550vm/Comic-SGG/visualization/NotoSansJP-Bold.otf', 15)
    draw = ImageDraw.Draw(pic)
    
    num_obj = len(boxes)
    for i in range(num_obj):
        info = box_labels[i]
        if 'text' in info:
            color = '#31a9b8'
        else:
            color = '#258039'

        box = boxes[i]
        x1,y1,x2,y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        draw.rectangle(((x1, y1), (x2, y2)), outline=color)
        text_width, text_height = font.getsize(info)
        draw.rectangle(((x1, y1-text_height), (x1+text_width, y1)), fill=color)
        draw.text((x1, y1-text_height), info, font=font)
    
    for item in rel_labels:
        sub_idx = box_labels.index(item[0])
        sub_box = boxes[sub_idx]
        x1,y1,x2,y2 = int(sub_box[0]), int(sub_box[1]), int(sub_box[2]), int(sub_box[3])
        sub_x = (x1 + x2) / 2
        sub_y = (y1 + y2) / 2
        obj_idx = box_labels.index(item[2])
        obj_box = boxes[obj_idx]
        x1,y1,x2,y2 = int(obj_box[0]), int(obj_box[1]), int(obj_box[2]), int(obj_box[3])
        obj_x = (x1 + x2) / 2
        obj_y = (y1 + y2) / 2
        shape = [(sub_x,sub_y),(obj_x,obj_y)]
        draw.line(shape, fill='#ffa500', width=3)
    st.image(pic)
    
    return None


def get_size(image_size):
    min_size = 600
    max_size = 1000
    w, h = image_size
    size = min_size
    if max_size is not None:
        min_original_size = float(min((w, h)))
        max_original_size = float(max((w, h)))
        if max_original_size / min_original_size * size > max_size:
            size = int(round(max_size * min_original_size / max_original_size))
    if (w <= h and w == size) or (h <= w and h == size):
        return (w, h)
    if w < h:
        ow = size
        oh = int(size * h / w)
    else:
        oh = size
        ow = int(size * w / h)
    return (ow, oh)


def main():
    st.title('Comic Speaker Detection')

    image_folder_path = './custom_images/'
    if os.path.exists(image_folder_path):
        shutil.rmtree(image_folder_path)
    os.makedirs(image_folder_path)
    load_image(image_folder_path)

    if st.button('Start testing'):
        my_bar = st.progress(20)
        subprocess.run(['bash', f"{'./demo.sh'}"])
        for percent_complete in range(20, 100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)

        # load the prediction results
        pred_path = './custom_images_output/custom_prediction.json'
        data_info_path = './custom_images_output/custom_data_info.json'
        load_pred(pred_path, data_info_path)


if __name__ == '__main__':
    main()
