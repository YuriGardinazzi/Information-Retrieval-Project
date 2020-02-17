#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to start the IR-engine
"""

import os, sys
import main as fx
import test_engine_bar as GUI

if __name__ == "__main__":
    if not (os.path.exists('pages')):
        print("Creating pages")
        fx.split_files()
        fx.remove_duplicate_files()
    else:
        print("Pages already created")
    if not (os.path.exists('index_dir')):
        print("Creating index")
        fx.create_index()
    else:
        print("Index already created")
    try: 
        print("Using " + sys.argv[1] + " model")
        GUI.start(sys.argv[1])
    except IndexError:
        print("Using default model")
        GUI.start("default")
   
    