# -*- coding: utf-8 -*-
"""
Remove duplicates line from a text file
"""
import io

def remove_equal_entries():
        
    lines_seen = set() # holds lines already seen
    with io.open("list_without_duplicates.txt", "w", encoding="utf-8") as output_file:
    	for each_line in io.open("list_for_exportpages.txt", "r",encoding ="utf-8"):
    	    if each_line not in lines_seen: # check if line is not duplicate
    	        output_file.write(each_line)
    	        lines_seen.add(each_line)
def remove_duplicate_files():
    import sys
    import os
    import hashlib

    def chunk_reader(fobj, chunk_size=1024):
            """Generator that reads a file in chunks of bytes"""
            while True:
                chunk = fobj.read(chunk_size)
                if not chunk:
                    return
                yield chunk
        
    def check_for_duplicates(path="pages", hash=hashlib.sha1):
        print("Start file removal")
        hashes = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                hashobj = hash()
                for chunk in chunk_reader(open(full_path, 'rb')):
                       hashobj.update(chunk)
                       file_id = (hashobj.digest(), os.path.getsize(full_path))
                       duplicate = hashes.get(file_id, None)
                       if duplicate:
                           #print ("Duplicate found: %s and %s" % (full_path, duplicate))
                           try:
                               os.remove(duplicate)
                               print("removed duplicate ", duplicate)
                           except:
                               continue
                       else:
                           hashes[file_id] = full_path
        
        if sys.argv[1:]:
            check_for_duplicates(sys.argv[1:])
        else:
            print ("Please pass the paths to check as parameters to the script")
    check_for_duplicates()
if __name__ == "__main__":
    remove_duplicate_files()
            