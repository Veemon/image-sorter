#!/usr/bin/env python

import random
import string
import glob
import os
def randomise():
    directory = os.getcwd()
    pictures = glob.glob('./*jpg')

    for pic in pictures:
        current = directory+'/'+pic
        new = directory+'/'+randomString(7)+pic[-4:]
        os.rename(current, new)

def randomString(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def main():
    randomise()

if __name__ == '__main__':
    main()
