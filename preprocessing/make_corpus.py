import argparse
import manga109api
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--manga109_root_dir', type=str, default='./manga109/', help='root dir for manga109api')
parser.add_argument('--max_page_number', type=int, default=184,
                    help='the maximum page number of manga109 datasets is 184 from the manga "hamlet".')
args = parser.parse_args()

# use manga109api parser
manga109_parser = manga109api.Parser(root_dir=args.manga109_root_dir)
manga_list = manga109_parser.books

for manga_name in manga_list:
    annotations = manga109_parser.get_annotation(manga_name)['page']
    
    for annotation in annotations:
        page_index = annotation['@index']
        
        # # char_id_to_name
        # try:
        #     char_dict = annotation['character']
        #     char_id_to_name = {}
        #     for char in char_dict:
        #         char_id_to_name[char['@id']] = char['@name']
        # except:
        #     pass

        try:
            rois = annotation['body']
            if isinstance(rois, dict):
                rois = [rois]  # for one instance case.
        except:
            continue

        for roi in rois:
            # names = char_id_to_name[roi['@character']]
            names = 'character'
            with open('words.txt', 'a') as f:
                f.write(names+" ")
        with open('words.txt', 'a') as f:
                f.write("\n")

        with open('./relationship.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for rows in csv_reader:
                if rows['title'] == str(manga_name) and rows['index'] == str(page_index):
                    row = dict(rows)
                    for roi in rois:
                        if roi['@id']==row['speaker_id']:
                            # name = char_id_to_name[roi['@character']]
                            name = 'character'
                            with open('words.txt', 'a') as f:
                                f.write(name+" says text\n")
        

# filename = "words.txt"
# myfile = open(filename) 
# lines = len(myfile.readlines()) 
# print (lines) 
