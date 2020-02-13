# -*- coding: utf-8 -*-
"""
Remove duplicates line from a text file
"""
import io
lines_seen = set() # holds lines already seen
with io.open("list_without_duplicates.txt", "w", encoding="utf-8") as output_file:
	for each_line in io.open("list_for_exportpages.txt", "r",encoding ="utf-8"):
	    if each_line not in lines_seen: # check if line is not duplicate
	        output_file.write(each_line)
	        lines_seen.add(each_line)