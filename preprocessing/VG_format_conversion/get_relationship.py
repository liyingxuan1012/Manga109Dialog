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

for i, manga_name in enumerate(manga_list):
    annotations = manga109_parser.get_annotation(manga_name)['page']
    annotation_type_list = ['body','text']

    for annotation in annotations:
        page_index = annotation['@index']
        images = {}
        relation_list = []
        images['image_id'] = "%03d" %i + "%03d" %page_index

        with open('./relationship.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for rows in csv_reader:
                if rows['title'] == str(manga_name) and rows['index'] == str(page_index):
                    row = dict(rows)
                    relationship_id = row['speaker_id'][3:]+row['text_id'][3:]
                    relationships = {'relationship_id':relationship_id,'predicate':'says','subject':{},'object':{}}

                    for annotation_type in annotation_type_list:
                        try:
                            rois = annotation[annotation_type]
                            if isinstance(rois, dict):
                                rois = [rois]  # for one instance case.
                        except:
                            continue

                        for roi in rois:
                            objects = {}
                            if annotation_type in {'body'} and roi['@id']==row['speaker_id']:
                                objects['object_id'] = roi['@id']
                                objects['x'] = roi['@xmin']
                                objects['y'] = roi['@ymin']
                                objects['w'] = roi['@xmax'] - roi['@xmin']
                                objects['h'] = roi['@ymax'] - roi['@ymin']
                                objects['name'] = 'character'
                                relationships['subject'] = objects

                            if annotation_type in {'text'} and roi['@id']==row['text_id']:
                                objects['object_id'] = roi['@id']
                                objects['x'] = roi['@xmin']
                                objects['y'] = roi['@ymin']
                                objects['w'] = roi['@xmax'] - roi['@xmin']
                                objects['h'] = roi['@ymax'] - roi['@ymin']
                                objects['name'] = 'text'
                                relationships['object'] = objects
                    relation_list.append(relationships)

            images['relationships'] = relation_list
            image_list.append(images)

output = json.dumps(image_list, ensure_ascii=False)
with open('./VG/relationships.json', 'w') as f:
    f.write(output)
