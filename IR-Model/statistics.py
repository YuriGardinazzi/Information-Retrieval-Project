# -*- coding: utf-8 -*-
"""
This file is used to retrieve statistics from queries
"""
import simplejson as json
from os import listdir
from os.path import isfile, join
import os
def get_google_ranking():
    
    path = "google_results"
    
    #struttura {()}
    res = {}
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        title_list = []
        filepath = os.path.join(path, f)
        with open(filepath,"r") as jsonFile:
            data = json.load(jsonFile)
            print (data['link'])
        
def try_read():
    table = []
    path="google_results"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        filepath = os.path.join("google_results",f)
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    j = line.split('|')[-1]
                    table.append(json.loads(j))
                except ValueError:
                    # You probably have bad JSON
                    continue
    
    for row in table:
        print(row['title'])
    
if __name__ == "__main__":
    print("Statistic:")
    try_read()
   # get_google_ranking()