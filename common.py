#!/usr/bin/python
# -*- coding: utf-8 -*-

import traceback
import sys
import argparse
import os
import re
import shutil
import errno

def rmdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def mkdir(src):
    try:
        os.makedirs(src)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise  # raises the error again

def get_curr_path():
    return os.path.dirname(os.path.realpath(__file__))

def file_exists(path):
    return os.path.isfile(path)

def file_read(path):
    # print "path: " + path
    with open(path, "r") as target_file:
        return target_file.read()

def file_write(path, data):
    with open(path, "w") as text_file:
        text_file.write(data)
