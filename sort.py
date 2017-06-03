#!/usr/bin/env python

import sys
import glob
import os
import cv2
import gc
from os import rename, listdir
from tqdm import tqdm
from multiprocessing import Pool, freeze_support

# Locals
from color_histogram.io_util.image import loadRGB, luminance
from color_histogram.core.hist_1d import Hist1D

# Pictures
def getPictures():
    pictures = glob.glob('./*jpg')
    parent = pictures[0]
    pictures.pop(0)
    return parent, pictures
def renamePictures(sortedPictures):
    directory = os.getcwd()
    for i, picture in enumerate(sortedPictures):
        current = directory+'/'+picture[2:len(picture)]
        new = directory+'/'+str(i)+'_'+picture[2:len(picture)]
        os.rename(current, new)

# Luminance
def getLum(pic):
    img = loadRGB(pic)
    lum = luminance(img)
    del img
    gc.collect()
    return ((lum_average(lum), pic))
def lum_average(array):
    result = 0
    length = 0
    for row in array:
        for element in row:
            result += element
            length += 1
    return result / length
def sortLum(parent, this_pictures):
    pictures = this_pictures[:]
    pictures.insert(0, parent)

    pool = Pool(4)
    lums = pool.map(getLum, pictures)
    pool.close()
    pool.join()

    lums.sort(key=lambda x: x[0])

    pictureNames = []
    for pic in lums:
        pictureNames.append(pic[1])
    renamePictures(pictureNames)

# Color
def compare(image_file1, image_file2):
    def histogram(image_file):
        image = loadRGB(image_file)
        hist1D = Hist1D(image, num_bins=12)
        densities = hist1D.colorDensities()
        rgbColors = hist1D.rgbColors()
        colors = map(lambda x: x*255, rgbColors)
        return list(zip(densities, colors))

    def difference(a,b):
        length = min(len(a), len(b))
        c = []
        for i in range(length):
            vec = []
            for j in range(len(a[i])):
                vec.append(abs(a[i][j] - b[i][j]))
            c.append(vec)
        return c

    def average(diff):
        avg_den = 0
        avg_rgb = 0
        for el in diff:
            avg_den += el[0]
            avg_rgb += ( sum(el[1]) / len(el[1]) )
        avg_den /= len(diff)
        avg_rgb /= len(diff)
        return avg_den, avg_rgb

    im1 = histogram(image_file1)
    im2 = histogram(image_file2)

    diff = difference(im1, im2)
    avg_den, avg_rgb = average(diff)

    del im1
    del im2
    gc.collect()

    return avg_den, avg_rgb, image_file2
def clusterPictures(parent, pictures):
    clusters = []
    for pic in tqdm(pictures, desc='Color'):
        clusters.append(compare(parent, pic))
    clusters.sort(key=lambda x: x[1])
    clusters.insert(0, [0,0,parent])
    return clusters
def sortColor(parent, pictures):
    def getNames(clusters):
        result = []
        for cluster in clusters:
            try:
                result.append(cluster[2])
            except:
                pass
        return result

    clusters = clusterPictures(parent, pictures)
    names = getNames(clusters)
    renamePictures(names)

# Entry
def main():
    def print_help():
        print('-d\t--debug: Enables debug for when this thing does a thing that gives you a spook.')
        print('-h\t--help: The thing you just done diddly did.')
        print('-l\t--luminance: Enables sorting by luminance.')
        print('-c\t--color: Enables sorting by color.')
        print('\nNotes:')
        print('If luminance and color are both set, luminance will occur before color.')
        print('Doing so tends to produce better results.')

    # Sys Args
    sort_lum = False
    sort_col = False

    for i in range(len(sys.argv)):
        if sys.argv[i] == '-d' or sys.argv[i] == '--debug':
            print('Debug Mode')
            import better_exceptions

        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            print_help()

        if sys.argv[i] == '-l' or sys.argv[i] == '--luminance':
            print('Luminance: Enabled')
            sort_lum = True

        if sys.argv[i] == '-c' or sys.argv[i] == '--color':
            print('Color: Enabled')
            sort_col = True

    if sort_lum:
        sortLum(*getPictures())
    if sort_col:
        sortColor(*getPictures())

if __name__ == '__main__':
    freeze_support()
    main()
