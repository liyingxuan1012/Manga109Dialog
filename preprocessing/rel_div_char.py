import argparse
import manga109api
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--manga109_root_dir', type=str, default='./manga109/', help='root dir for manga109api')
args = parser.parse_args()

# use manga109api parser
manga109_parser = manga109api.Parser(root_dir=args.manga109_root_dir)
manga_list = manga109_parser.books

data = pd.read_csv('./relationship.csv')
chars = []
char_0 = 0
char_1 = 0
char_2 = 0

for manga_name in manga_list:
    annotation_type_list = ['body', 'text']
    annotations = manga109_parser.get_annotation(manga_name)['page']

    for annotation in annotations:
        page_index = annotation['@index']
        data_temp = data.loc[data['title']==str(manga_name)]
        data_new = data_temp.loc[data_temp['index']==page_index]

        if len(data_new) == 0:
            continue
        else:
            char_to_frame = {}
            text_to_frame = {}

            # find frame
            frame_coords = {}
            rois = annotations[page_index]['frame']
            if isinstance(rois, dict):
                rois = [rois]  # for one instance case.
            for roi in rois:
                frame_coords[roi['@id']] = {'xmin':roi['@xmin'],'ymin':roi['@ymin'],'xmax':roi['@xmax'],'ymax':roi['@ymax']}

            for annotation_type in annotation_type_list:
                rois = annotations[page_index][annotation_type]
                if isinstance(rois, dict):
                    rois = [rois]  # for one instance case.

                for roi in rois:
                    x_center = (roi['@xmin']+roi['@xmax'])/2
                    y_center = (roi['@ymin']+roi['@ymax'])/2

                    if annotation_type in {'body'}:
                        for frame_coord in frame_coords:
                            if frame_coords[frame_coord]['xmin']<x_center<frame_coords[frame_coord]['xmax'] and frame_coords[frame_coord]['ymin']<y_center<frame_coords[frame_coord]['ymax']:
                                char_to_frame[roi['@id']] = frame_coord

                    if annotation_type in {'text'}:
                        for frame_coord in frame_coords:
                            if frame_coords[frame_coord]['xmin']<x_center<frame_coords[frame_coord]['xmax'] and frame_coords[frame_coord]['ymin']<y_center<frame_coords[frame_coord]['ymax']:
                                text_to_frame[roi['@id']] = frame_coord
            
            for text_id in data_new['text_id']:
                if text_id in text_to_frame:
                    chars = [char for char in char_to_frame if char_to_frame[char]==text_to_frame[text_id]]
                if len(chars)==1:
                    char_1 += 1
                elif len(chars) > 1:
                    char_2 += 1
                else:
                    char_0 += 1

print(char_0)
print(char_1)
print(char_2)
