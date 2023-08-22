import argparse
import manga109api
import json
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--manga109_root_dir', type=str, default='./manga109/', help='root dir for manga109api')
args = parser.parse_args()

# use manga109api parser
manga109_parser = manga109api.Parser(root_dir=args.manga109_root_dir)
manga_list = manga109_parser.books

image_list = []

with open('./relationship.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    column = [row['text_id'] for row in csv_reader]

for i, manga_name in enumerate(manga_list):
    annotations = manga109_parser.get_annotation(manga_name)['page']    
    annotation_type_list = ['body','text']

    for annotation in annotations:
        page_index = annotation['@index']
        images = {}
        object_list = []
        images['image_id'] = "%03d" %i + "%03d" %page_index

        # find frame
        frame_coords = {}
        rois = annotations[page_index]['frame']
        if isinstance(rois, dict):
            rois = [rois]  # for one instance case.
        for roi in rois:
            frame_coords[roi['@id']] = {'xmin':roi['@xmin'],'ymin':roi['@ymin'],'xmax':roi['@xmax'],'ymax':roi['@ymax']}

        for annotation_type in annotation_type_list:
            try:
                rois = annotation[annotation_type]
                if isinstance(rois, dict):
                    rois = [rois]  # for one instance case.
            except:
                continue

            for roi in rois:
                x_center = (roi['@xmin']+roi['@xmax'])/2
                y_center = (roi['@ymin']+roi['@ymax'])/2

                objects = {}
                if annotation_type in {'body'}:
                    objects['object_id'] = roi['@id']
                    objects['x'] = roi['@xmin']
                    objects['y'] = roi['@ymin']
                    objects['w'] = roi['@xmax'] - roi['@xmin']
                    objects['h'] = roi['@ymax'] - roi['@ymin']
                    for frame_coord in frame_coords:
                        if frame_coords[frame_coord]['xmin']<x_center<frame_coords[frame_coord]['xmax'] and frame_coords[frame_coord]['ymin']<y_center<frame_coords[frame_coord]['ymax']:
                            objects['x'] = frame_coords[frame_coord]['xmin']
                            objects['y'] = frame_coords[frame_coord]['ymin']
                            objects['w'] = frame_coords[frame_coord]['xmax'] - frame_coords[frame_coord]['xmin']
                            objects['h'] = frame_coords[frame_coord]['ymax'] - frame_coords[frame_coord]['ymin']
                    objects['names'] = 'character'
                    object_list.append(objects)

                if annotation_type in {'text'} and roi['@id']in column:
                    objects['object_id'] = roi['@id']
                    objects['x'] = roi['@xmin']
                    objects['y'] = roi['@ymin']
                    objects['w'] = roi['@xmax'] - roi['@xmin']
                    objects['h'] = roi['@ymax'] - roi['@ymin']
                    for frame_coord in frame_coords:
                        if frame_coords[frame_coord]['xmin']<x_center<frame_coords[frame_coord]['xmax'] and frame_coords[frame_coord]['ymin']<y_center<frame_coords[frame_coord]['ymax']:
                            objects['x'] = frame_coords[frame_coord]['xmin']
                            objects['y'] = frame_coords[frame_coord]['ymin']
                            objects['w'] = frame_coords[frame_coord]['xmax'] - frame_coords[frame_coord]['xmin']
                            objects['h'] = frame_coords[frame_coord]['ymax'] - frame_coords[frame_coord]['ymin']
                    objects['names'] = 'text'
                    object_list.append(objects)

        images['objects'] = object_list
        image_list.append(images)
        
output = json.dumps(image_list, ensure_ascii=False)
with open('./VG/frames.json', 'w') as f:
        f.write(output)
        