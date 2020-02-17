#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to start the IR-engine
"""

import os 
import main as fx
import test_engine_bar as GUI

if __name__ == "__main__":
    if not (os.path.exists('pages')):
        print("Creating pages")
        fx.split_files()
    else:
        print("Pages already created")
    if not (os.path.exists('index_dir')):
        print("Creating index")
        fx.create_index()
    else:
        print("Index already created")
    GUI.start()
    