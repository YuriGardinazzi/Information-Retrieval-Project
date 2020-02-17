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
    import os
    import hashlib
    def read_chunk(fobj, chunk_size = 2048):
        """ Files can be huge so read them in chunks of bytes. """
        while True:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def remove_duplicates(dir, hashfun = hashlib.sha512):
        unique = set()
        for filename in os.listdir(dir):
            filepath = os.path.join(dir, filename)
            if os.path.isfile(filepath):
                hashobj = hashfun()
                for chunk in read_chunk(open(filepath,'rb')):
                    hashobj.update(chunk)
                    # the size of the hashobj is constant
                    # print "hashfun: ", hashfun.__sizeof__()
                hashfile = hashobj.hexdigest()
                if hashfile not in unique:
                    unique.add(hashfile)
                else: 
                    os.remove(filepath)

    try:
        hashfun = hashlib.sha256
        remove_duplicates("pages", hashfun)

    except IndexError:
        print ("Please pass a path to a directory with duplicate files as a parameter to the script.")
    
if __name__ == "__main__":
    remove_duplicate_files()
            