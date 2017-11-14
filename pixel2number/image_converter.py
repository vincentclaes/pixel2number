import argparse
import collections
import os
from collections import OrderedDict
from collections import defaultdict

from PIL import ImageOps, Image
from pandas import DataFrame


def get_image(input_file):
    im = Image.open(input_file).convert('RGB')  # Can be many different formats.
    im = ImageOps.mirror(im)
    im = im.transpose(Image.ROTATE_90)
    return im


def convert(input_file):
    file_name, ext = os.path.splitext(input_file)

    im = get_image(input_file)

    pix = im.load()
    color_dict = OrderedDict()
    color_counter = defaultdict(int)
    dataframe = DataFrame(index=range(im.size[0]), columns=range(im.size[1]))
    counter = 0
    print('printing image : ')
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pix[i, j] not in color_dict.keys():
                counter += 1
                color_dict[pix[i, j]] = counter
            color_counter[pix[i, j]] += 1
            print(color_dict[pix[i, j]],)
            dataframe.loc[i, j] = color_dict[pix[i, j]]
        print('')

    print('legende')
    print('---------')
    print('dimensions : {}'.format(im.size))
    print('')
    print('{: >20} {: >20} {: >20} {: >20} {: >20}'.format('R', 'G', 'B', 'number', 'count'))
    for k, v in color_dict.items():
        print('{: >20} {: >20} {: >20} {: >20} {: >20}'.format(k[0], k[1], k[2], v, color_counter[k]))

    # color_dict = sorted(color_dict)
    sorted_color_dict = collections.OrderedDict(sorted(color_dict.items(), reverse=True))

    dataframe = dataframe.applymap(lambda x: x * -1)
    color_dict = {}
    # the index of the color defines the "luminostory" *ahum*.
    # so if the first element was nr 5 -> it will become now nr 1 in the df and the color dict
    for i, colour in enumerate(sorted_color_dict.items(), start=1):
        dataframe = dataframe.applymap(lambda x: i if x * -1 == colour[1] else x)
        # create a new color dict with the sorted colour ranging from 1 to x
        color_dict[colour[0]] = i

    color_dict = collections.OrderedDict(sorted(color_dict.items(), reverse=True))

    file_name_csv = file_name + '.csv'
    dataframe.to_csv(file_name_csv, index=False, header=False,
                     sep=';')

    fd = open(file_name_csv, 'a')
    fd.write('legende \n')
    fd.write('--------- \n')
    fd.write('dimensions : {} \n'.format(im.size))
    fd.write('')
    fd.write('{: >20} {: >20} {: >20} {: >20} {: >20} \n'.format('R', 'G', 'B', 'number', 'count'))
    for k, v in color_dict.items():
        fd.write('{: >20} {: >20} {: >20} {: >20} {: >20} \n'.format(k[0], k[1], k[2], v, color_counter[k]))

    fd.close()
    number_of_colours = len(color_dict)
    LENGTH_SQUARE_SIDE = 50
    TOTAL_WIDTH = number_of_colours * LENGTH_SQUARE_SIDE
    TOTAL_HEIGHT = LENGTH_SQUARE_SIDE
    x_y = (TOTAL_WIDTH, TOTAL_HEIGHT)
    im = Image.new("RGB", (x_y[0], x_y[1]))
    pix = im.load()
    for y in range(x_y[1]):
        counter = 0
        for i, x in enumerate(range(x_y[0])):
            pix[x, y] = list(color_dict.keys())[counter]
            if i != 0 and i % LENGTH_SQUARE_SIDE == 0:
                counter += 1
    file_name_png = file_name + '_sorted_colours' + '.png'
    im.save(file_name_png, "PNG")
    return file_name_csv, file_name_png
