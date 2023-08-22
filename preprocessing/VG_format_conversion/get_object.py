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

    # # char_id_to_name
    # try:
    #     char_dict = annotations['character']
    #     char_id_to_name = {}
    #     for char in char_dict:
    #         char_id_to_name[char['@id']] = char['@name']
    # except:
    #     pass

    for annotation in annotations:
        page_index = annotation['@index']
        images = {}
        object_list = []
        images['image_id'] = "%03d" %i + "%03d" %page_index

        for annotation_type in annotation_type_list:
            try:
                rois = annotation[annotation_type]
                if isinstance(rois, dict):
                    rois = [rois]  # for one instance case.
            except:
                continue

            for roi in rois:
                objects = {}
                if annotation_type in {'body'}:
                    objects['object_id'] = roi['@id']
                    objects['x'] = roi['@xmin']
                    objects['y'] = roi['@ymin']
                    objects['w'] = roi['@xmax'] - roi['@xmin']
                    objects['h'] = roi['@ymax'] - roi['@ymin']
                    # objects['names'] = char_id_to_name[roi['@character']]
                    objects['names'] = 'character'
                    object_list.append(objects)

                if annotation_type in {'text'} and roi['@id']in column:
                    objects['object_id'] = roi['@id']
                    objects['x'] = roi['@xmin']
                    objects['y'] = roi['@ymin']
                    objects['w'] = roi['@xmax'] - roi['@xmin']
                    objects['h'] = roi['@ymax'] - roi['@ymin']
                    objects['names'] = 'text'
                    object_list.append(objects)

        images['objects'] = object_list
        image_list.append(images)
        
output = json.dumps(image_list, ensure_ascii=False)
with open('./VG/objects.json', 'w') as f:
        f.write(output)
