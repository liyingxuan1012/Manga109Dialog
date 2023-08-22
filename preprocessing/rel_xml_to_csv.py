import argparse
import manga109api
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--manga109_root_dir', type=str, default='./manga109/', help='root dir for manga109api')
args = parser.parse_args()

# use manga109api parser
manga109_parser = manga109api.Parser(root_dir=args.manga109_root_dir)
manga_list = manga109_parser.books

with open('./relationship.csv', 'w') as csvfile:
    fileheader = ["title","index","text_id","speaker_id"]
    writer = csv.DictWriter(csvfile, fileheader)
    writer.writeheader()
        
    for manga_name in manga_list:
        # get page index
        relationships = manga109_parser.get_annotation(book=manga_name, annotation_type="relationships")['page']
        for relationship in relationships:
            page_index = relationship['@index']
            
            # get relationships
            try:
                rels = relationships[page_index]['speaker_to_text']
                if isinstance(rels, dict):
                    rels = [rels]  # for one instance case.
            except:
                continue

            for rel in rels:
                writer.writerow({"title":manga_name,"index":page_index,"text_id":rel['@text_id'],"speaker_id":rel['@speaker_id']})


with open('./annotations.csv', 'w') as csvfile:
    fileheader = ["title","index","text_id","character_id"]
    writer = csv.DictWriter(csvfile, fileheader)
    writer.writeheader()
        
    for manga_name in manga_list:
        annotations = manga109_parser.get_annotation(book=manga_name, annotation_type="annotations")['page']
        relationships = manga109_parser.get_annotation(book=manga_name, annotation_type="relationships")['page']

        for annotation in annotations:
            page_index = annotation['@index']
 
            # body_id_to_char
            body_id_to_char = {}
            rois = annotation['body']
            if isinstance(rois, dict):
                rois = [rois]  # for one instance case.
            for roi in rois:
                body_id_to_char[roi['@id']] = roi['@character']

            # get relationships
            try:
                rels = relationships[page_index]['speaker_to_text']
                if isinstance(rels, dict):
                    rels = [rels]  # for one instance case.
            except:
                continue

            for rel in rels:
                writer.writerow({"title":manga_name,"index":page_index,"text_id":rel['@text_id'],"character_id":body_id_to_char[rel['@speaker_id']]})
