# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 17:14:49 2020

@author: Yuri
"""

from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

ix = open_dir("indexdir")

searcher = ix.searcher()
print(list(searcher.lexicon("content")))
parser = QueryParser("content", schema=ix.schema)
query = parser.parse(u"Japan")
results = searcher.search(query)
if len(results) == 0:
    print("Empty result!!")
else:
    for x in results:
        print(x.encode("utf-8"))
ix.close()


