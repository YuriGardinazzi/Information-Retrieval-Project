# -*- coding: utf-8 -*-
"""

Main file of the search-engine
"""

from dump_splitter import WikiSplitter
from index_creator import Index

def split_files():
    splitter = WikiSplitter()
    splitter.splitFiles()  
    
def create_index():
    Ind = Index()
    Ind.createIndex()
    
def make_query(text):
    Ind = Index()  
    result = Ind.makeQuery(text)
    if result != None:
        for x in result:
            print("*********************")
            print(x['title'])
            print(x['textdata'][:500])

if __name__ == "__main__":
    
    response = str(input("Vuoi creare l'indice?[Y/N]"))
    if response == 'Y':
        create_index()
    query = str(input("Cosa vuoi ricercare?"))
    make_query(query)