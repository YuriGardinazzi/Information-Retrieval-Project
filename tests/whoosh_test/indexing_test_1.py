# -*- coding: utf-8 -*-
"""
Test of Whoosh library

To use whoosh an Index object is needed.
To have an Index a schema is needed
A field is a piece of information for each document in the index, such as Title or Text
A field can be Indexed = searchable  and/or Stored
"""

from whoosh.index import create_in
from whoosh.fields import *
import os, os.path, io


directory = 'doc'
doc1= os.path.join(directory, "61.txt")
doc2= os.path.join(directory, "141.txt")
doc3= os.path.join(directory, "148.txt")

#creation of the schema
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    
#creation of the index
ix = create_in("indexdir", schema)

writer = ix.writer()


writer.add_document(title=u"First document", path=doc1, content=io.open(doc3,"r", encoding="utf-8").readlines())
writer.add_document(title=u"Second document", path=doc2, content=io.open(doc2,"r", encoding="utf-8").readlines())
writer.add_document(title=u"Second document", path=doc2, content=io.open(doc1,"r",encoding="utf-8").readlines())
writer.commit()

ix.close()