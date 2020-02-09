# -*- coding: utf-8 -*-
"""
This file tests the index created by the file "indexed_test_1.py"
"""

from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

def searchQuery(self, string):
    ix = open_dir("indexdir")
    
    searcher = ix.searcher()
    #print(list(searcher.lexicon("content")))
    parser = QueryParser("content", schema=ix.schema)
    query = parser.parse(string)  
    results = searcher.search(query)
    
    if len(results) == 0:
        print("Empty Result")
    else:
        print("Query: ", query)
        print("Number of results: ", len(results))
        print("**********")
        for x in results:
            print("PATH:", x['path'])
            print("TITLE:", x['title'])
            print("TEXTDATA:", x['textdata'][:300])
            print("************")
            



