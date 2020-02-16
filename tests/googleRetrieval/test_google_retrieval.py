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
import urllib
from googleapiclient.discovery import build
import pprint
import os
import wikipediaapi
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
        for i_start in 0,1,2:
            results = google_search(query, my_api_key, my_cse_id, num=10, start = i_start*10)
            file_name = query+".json"
            with io.open(file_name,"a+") as f:
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
def download_web_pages(query_list):
    for x in query_list:
        with open(x+".json", 'r') as f:
            for line in f:

                el = json.loads(line)
                url = el['link']
                response = urllib.request.urlopen(url)
                webContent = response.read()

                html_file_name = el['title'].replace(" - Wikipedia","")
                print(html_file_name)
                #nel caso ci fossero degli /
                splitted = os.path.split(html_file_name)
                html_file_name = "".join(splitted)
                print("saving: ",html_file_name)
                p = open(html_file_name+".html", 'wb')
                p.write(webContent)
                p.close()
               
def  print_pages_wiki_api():
    
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI)
    num_file = 0
    for file in os.listdir("."):
        if file.endswith(".json"):
            c = 0
            print("pages for: ", file)
            with open(file, 'r') as f:
                for line in f:
                    c+=1
                    el = json.loads(line)
                    title = el['title'].replace(" - Wikipedia","")
                    print("###",c,"###",'''wiki_wiki.page(title).text''')
            print("end pages for: ", file,"_________________num: ", num_file)
        num_file += 1
def create_custom_dump():
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    with io.open("custom_dump.xml","a+", encoding="utf-8") as output_file:
        output_file.write("<root>\n")
        
        num_file = 0
        for file in os.listdir("."):
            if file.endswith(".json"):
                c = 0
                print("pages for: ", file)
                with open(file, 'r') as f:
                    for line in f:
                        c+=1
                        el = json.loads(line)
                        title = el['title'].replace(" - Wikipedia","")
                        text_to_save = "<page>\n<title>"+ title + "</title>\n" \
                                + "<text>" + clean_text(wiki_wiki.page(title).text) + "</text>\n</page>\n"
                        
                        output_file.write(text_to_save)
                        print("###",c,"###",'''wiki_wiki.page(title).text''')
                print("end pages for: ", file,"_________________num: ", num_file)
            num_file += 1
        output_file.write("</root>")
def clean_text(text):

    ris = text.replace("&", "&amp;")
    ris = ris.replace("<", "&lt;")
    ris = ris.replace(">", "&gt;")
    print(ris)
    return ris
def clean_file():
    with open("correct_dump.xml","w", encoding ="utf-8") as of:
        with open("custom_wikipedia.xml","r",encoding ="utf-8") as inputf:
            for line in inputf:
                oline = line.replace("&","&amp;")
                oline = oline.replace(" < ", "&lt;")
               # oline = oline.replace(" << ", "&lt;&lt;")
                oline = oline.replace(" > ", "&gt;")
#                oline = oline.replace(">>=", "&gt;&gt;")
                oline = oline.replace(">>=", "&gt;&gt;=")
#                oline = oline.replace(" >= ", "&gt;&gt;=")
                oline = oline.replace("<<=", "&gt;&gt;=")
                oline = oline.replace("<<", "&gt;&gt;")
                oline = oline.replace("<,", "&gt;")
                oline = oline.replace("<=", "&gt;&gt;")
                oline = oline.replace("<%", "&gt;%")
                oline = oline.replace("<:", "&gt;:")
                of.write(oline)       
if __name__ == "__main__":
    #"DNA","Hollywood","Apple","Epigenetics","Maya","Microsoft","Precision","Tuscany","99 balloons",
    """
    "
    """
    q_list = [ "Computer Programming"\
            ,"Financial meltdown","Justin Timberlake","Least Squares", "Mars robots","Page six",\
            "Roman Empire", "Solar energy", "Statistical Significance", "Steve Jobs", \
            "The Maya", "Triple Cross", "US Constitution", "Eye of Horus", "Madam I'm Adam", \
            "Mean Average Precision", "Physics Nobel Prizes","Read the manual",\
            "Spanish Civil War", "Do geese see god"]
    
    #print(list)
   # list2 = ["DNA","Hollywood"]
   # save_data_to_JSON(list)
    #download_web_pages(q_list)
    create_custom_dump()   
