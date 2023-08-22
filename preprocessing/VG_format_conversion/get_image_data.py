import argparse
import manga109api
import json


parser = argparse.ArgumentParser()
parser.add_argument('--manga109_root_dir', type=str, default='./manga109/', help='root dir for manga109api')
args = parser.parse_args()

# use manga109api parser
manga109_parser = manga109api.Parser(root_dir=args.manga109_root_dir)
manga_list = manga109_parser.books

image_list = []

for i, manga_name in enumerate(manga_list):
    annotations = manga109_parser.get_annotation(manga_name)['page']

    for annotation in annotations:
        page_index = annotation['@index']
        images = {}
        images['image_id'] = "%03d" %i + "%03d" %page_index

        images['width'] = annotation['@width']
        images['height'] = annotation['@height']
        image_list.append(images)

output = json.dumps(image_list, ensure_ascii=False)
with open('./VG/image_data.json', 'w') as f:
        f.write(output)
