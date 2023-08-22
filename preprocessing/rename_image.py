import os, shutil


srcDirName = '/Users/liyingxuan/Desktop/speaker_pred_and_vis/manga109/images'
destDirName = './VG/images'

with open('./manga109/books.txt', 'r') as book_list:
    manga_list = book_list.readlines()

for i, manga_name in enumerate(manga_list):
    manga_name = manga_name.strip()
    fileList = os.listdir(srcDirName + '/' + manga_name)
    for file in fileList[::]:
        shutil.copy(srcDirName + '/' + manga_name + '/' + file, destDirName + '/' + "%03d"%i + file)
