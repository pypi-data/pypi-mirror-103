# -*- coding: utf-8 -*-
# ***********************************************************
# aitk.utils: Python AI utils
#
# Copyright (c) 2020 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.utils
#
# ***********************************************************

import os
import numpy as np
from PIL import Image

from .utils import get_file

_filename = get_file(
    "dogs-vs-cats.tar.gz",
    "https://media.githubusercontent.com/media/Calysto/conx-data/master/dogs-vs-cats/dogs-vs-cats.tar.gz",
    extract=True,
)

# Strip off gz, then tar:
DATA_DIR = os.path.splitext(os.path.splitext(_filename)[0])[0]

def onehot(num):
    retval = [0] * 10
    retval[num] = 1
    return retval

def get():
    """
    """
    dogs_filename = os.path.join(DATA_DIR, "dogs.npy")
    if not os.path.exists(dogs_filename):
        print("Creating dogs.npy...")
        # create dogs array
        dogs = []
        for i in range(10000):
            filename = os.path.join(DATA_DIR, "dog.%i.jpg" % i)
            if os.path.exists(filename):
                image = Image.open(filename)
                array = np.array(image)
                dogs.append(array)
        dogs = np.array(dogs)
        np.save(dogs_filename, dogs)
    else:
        dogs = np.load(dogs_filename)

    cats_filename = os.path.join(DATA_DIR, "cats.npy")
    if not os.path.exists(cats_filename):
        print("Creating cats.npy...")
        # create cats array
        cats = []
        for i in range(10000):
            filename = os.path.join(DATA_DIR, "cat.%i.jpg" % i)
            if os.path.exists(filename):
                image = Image.open(filename)
                array = np.array(image)
                cats.append(array)
        cats = np.array(cats)
        np.save(cats_filename, cats)
    else:
        cats = np.load(cats_filename)
    return cats, dogs
