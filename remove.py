#!/usr/bin/env python

import random
import string
import glob
import os
def remove():
    directory = os.getcwd()
    pictures = glob.glob('./*jpg')

    for pic in pictures:
        current = directory+'/'+pic
        pic = pic.split('_')
        new = directory+'/'+pic[-1]
        os.rename(current, new)

def main():
    remove()

if __name__ == '__main__':
    main()
