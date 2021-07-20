#!/usr/bin/env python

"""
Image processing and watermarking utility.
@author: Anatole Hernot
@version: 2.0.0
"""

import os

import preferences
import batch


if __name__ == '__main__':

    # Change path to ~/backend/processing/
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    batch.run(path=preferences.SOURCE_PATH)
