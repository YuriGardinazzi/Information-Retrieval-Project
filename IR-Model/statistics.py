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
    table = []
    path="google_results"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        filepath = os.path.join("google_results",f)
        #f[:-5] removes the .json extension
        res[f[:-5]] = []
        with io.open(filepath, 'r',encoding="utf-8") as file_json:
            for line in file_json:
                try:
                    data = json.loads(line)
                    titolo= data['title'].replace(" - Wikipedia","")             
                    res[f[:-5]].append(str(titolo))
                   
                    table.append(data)
                except ValueError:
                    # You probably have bad JSON
                    continue
    
    #for row in table:
     #   print(row['title'].replace(" - Wikipedia",""))
    return res
if __name__ == "__main__":
    print("Statistic:")
    res = get_google_ranking()
    for key in res.keys():
        print("Key: ", key,"num_risultati: ",len(res[key]))

   # get_google_ranking()