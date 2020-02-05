# -*- coding: utf-8 -*-
"""
From a *.bz2 file take a CHUNK of bytes starting from INDEX
decompress the chunk of bytes and save it in a *.xml file
______________________
Structure of Index file:
starting_byte_index: article_id: title_of_the_Article (or other stuff)

useful links:
bz2 module: https://docs.python.org/3.7/library/bz2.html

XML-Schema = https://www.mediawiki.org/xml/export-0.10/
Namespaces used = https://www.mediawiki.org/wiki/Help:Namespaces
https://www.mediawiki.org/wiki/Help:Export
https://pymotw.com/2/bz2/
https://en.wikipedia.org/wiki/Wikipedia:Database_download#Should_I_get_multistream?
"""

import bz2

INDEX = 47504145
CHUNK = 80000


file = b"enwikinews.xml.bz2" #take the file in binary

zipfile = bz2.BZ2File(file) # open the file

zipfile.seek(INDEX) #move forward to the INDEX byte
data = zipfile.read(CHUNK) # get the decompressed M bytes
newfile = "enwikinews.xml"
open(newfile,"wb").write(data) #create new file

zipfile.close()