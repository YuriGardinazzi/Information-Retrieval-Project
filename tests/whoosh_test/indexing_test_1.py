# -*- coding: utf-8 -*-
"""
Test of Whoosh library

This file creates a simple index based on text files inside the directory  docs
schema is the  structure of the indexed file, stored = searchable and indexed

useful links: 
https://appliedmachinelearning.blog/2018/07/31/developing-a-fast-indexing-and-full-text-search-engine-with-whoosh-a-pure-python-library/
https://whoosh.readthedocs.io/en/latest/quickstart.html
"""

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
import os, os.path, io, shutil


<<<<<<< HEAD
def createIndex():
    #creation of the schema
=======
#creation of the schema
def createIndex():
>>>>>>> master
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    else:
        shutil.rmtree("indexdir")
        print("Eliminated old indexes")
        os.mkdir("indexdir")
        
    #creation of the index
    ix = create_in("indexdir", schema)
    print("Created index")
    
    writer = ix.writer()
    
    #adding entries to the index
    directory = 'doc'
    filepaths = [os.path.join(directory,i) for i in os.listdir(directory)]
    print("Documents read: ")
    for path in filepaths:
            fp = io.open(path,'r',encoding="utf-8")
            print(path)
            text = fp.read()
            #title it's not the real title of the document but just the filename
            writer.add_document(title=(os.path.split(path))[1], path=path, content=text,textdata=text)
            fp.close()
    writer.commit()

