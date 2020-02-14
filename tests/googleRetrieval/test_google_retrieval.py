# -*- coding: utf-8 -*-
"""
This file does a google query for each term in the list passed, and it creates
a json file with the results

useful resource:
https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
"""

import sys, getopt
import urllib
import simplejson as json
import requests
import io
from googleapiclient.discovery import build
import pprint

my_api_key=""
my_cse_id=""


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


print("my_api_key: ", my_api_key)
print("my_cse_id: ", my_cse_id)


def save_data_to_JSON(query_list):
    for query in query_list:
        results = google_search(query, my_api_key, my_cse_id, num=10)
        file_name = query+".json"
        with io.open(file_name,"w") as f:
            for result in results:
              #  pprint.pprint(result)
                json.dump(result,f)
                f.write("\n")
def read_line(list):
    table = []
    for l in list:  
        with open(l+".json", 'r') as f:
            for line in f:
                try:
                    j = line.split('|')[-1]
                    table.append(json.loads(j))
                except ValueError:
                    # You probably have bad JSON
                    continue
    c = 1
    for row in table:
        print(c, " ",row['link'])
        c+=1
    print(len(table))
    
if __name__ == "__main__":
    
    list = ["DNA","Hollywood","Apple","Epigenetics","Maya","Microsoft","Precision","Tuscany","99 balloons","Computer Programming"\
            ,"Financial meltdown","Justin Timberlake","Least Squares", "Mars robots","Page six",\
            "Roman Empire", "Solar energy", "Statistical Significance", "Steve Jobs", \
            "The Maya", "Triple Cross", "US Constitution", "Eye of Horus", "Madam I'm Adam", \
            "Mean Average Precision", "Physics Nobel Prizes", "Read the manual",\
            "Spanish Civil War", "Do geese see god", "Much ado about nothing"]
    #print(list)
   # list2 = ["DNA","Hollywood"]
  #  save_data_to_JSON(list)
    read_line(list)
    
