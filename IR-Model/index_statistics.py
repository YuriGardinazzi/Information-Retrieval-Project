# -*- coding: utf-8 -*-
"""
This file is used to retrieve statistics from queries
"""
import simplejson as json
from os import listdir
from os.path import isfile, join
import os
import io
def get_google_ranking():
    """This function returns a dictionary where 
    key = Title
    value = List of the first 10 results"""
    res = {}
    path="google_results"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        filepath = os.path.join("google_results",f)
        #f[:-5] removes the .json extension
        res[f[:-5]] = []
        with io.open(filepath, 'r',encoding="utf-8") as file_json:
            c = 1
            rel = 7
            for line in file_json:
                try:
                    
                    if c >= 1 and c < 6:
                        rel -= 1
                    else:
                        rel = 1
                    data = json.loads(line)
                    titolo= data['title'].replace(" - Wikipedia","")             
                    res[f[:-5]].append((str(titolo),rel))               
                    c += 1
                except ValueError:
                    # Bad Json
                    continue
    
    return res
if __name__ == "__main__":
    print("Statistic:")
    res = get_google_ranking()
    for key in res.keys():
        print("Key: ", key,"\nnum_risultati: ",len(res[key]))
        print(res[key], "\n**********")