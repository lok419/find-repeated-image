import numpy as np
from PIL import Image
import os

path = 'C:\\Users\\Cheung\\Google 雲端硬碟\\Doujin'
format = ['.jpg','.png','.bmp']

def read_image(path, format):
    # return name of all files with defined format
    filelist = []
    for filename in os.listdir(path):
        for i in format:
            if i in filename:
                filelist.append(filename)
    return filelist

def image_to_array(im, size):
    # convert an image object to array
    return np.array(im.resize(size,Image.BILINEAR).convert("L"))

def build_array(path, format, resize):
    # convert all image objects to arrays

    image_list = read_image(path, format)
    array_list = []
    total_image = len(image_list)
    print('Start building array with size',resize)
    for ix, name in enumerate(image_list):
        im = Image.open('{}\\{}'.format(path,name))
        array_list.append(image_to_array(im,resize))
        print('Progress: {}/{}'.format(ix+1,total_image))

    return array_list, image_list

def show_image(filename):
    Image.open(filename).show()
    return

def compare_array(path, format, resize):
    print('Now comparing all array')
    array_list, image_list = build_array(path, format, resize)
    all_pairs = []
    repeated = []

    for i in range(len(array_list)):
        print('Progress: {}/{}'.format(i+1, len(array_list)))
        if i in repeated:
            continue

        pairs = [image_list[i]]
        for j in range(i+1, len(array_list)):
            if np.array_equal(array_list[i],array_list[j]):
                pairs.append(image_list[j])
                repeated.append(j)
        if len(pairs) > 1:
            all_pairs.append(pairs)
            print('found repeated photos {}'.format(pairs))

    print('Comparsion completed, found {} set of repeated photo '.format(len(all_pairs)))
    for i, pairs in enumerate(all_pairs):
        print(pairs)

    return all_pairs

def del_photo(path, format, resize = (10,10)):
    all_pairs = compare_array(path, format, resize)
    if len(all_pairs) == 0:
        exit()
    r = input('Delete all repeated photos ? [Y/N]')
    if r == 'Y' or r == 'y':
        count = 0
        for pairs in all_pairs:
            for name in pairs[:-1]:
                os.remove('{}\\{}'.format(path,name))
                print('Deleted {}'.format(name))
                count += 1
        print('Deleted {} images'.format(count))

if __name__ == '__main__':
    del_photo(path, format)




