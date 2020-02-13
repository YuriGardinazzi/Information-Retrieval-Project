# -*- coding: utf-8 -*-
"""

Main file of the search-engine
"""

from dump_splitter import WikiSplitter
from index_creator import Index
#import calc as Calculator

def display_menu():
    print("""
          1. Create Index
          2. Create Pages
          3. Search something
          4. Exit
          """)
    answer = input("What would you like to do? ")
    if answer == "1":
        create_index()
    elif answer == "2":
        split_files()
    elif answer == "3":
        query = str(input("Insert a term to search: "))
        choose_model(query)
    elif answer == "4":
        raise SystemExit
    else:
        print("Invalid choice!")
    
def choose_model(query):
    print("""
          1. Default (BM25F)
          2. Cosine
          3. PL2
          4. Back
          """)
    answer = input("Choose Model to use: ")
    if answer == "1":
        print("Default model selected!")
        make_query(query, "default")
    elif answer == "2":
        print("Cosine weighting model selected!")
        make_query(query, "cosine")
    elif answer == "3":
        print("PL2 weighting model selected!")
        make_query(query, "pl2")
    elif answer == "4":
        print("Going back!")
        display_menu()
    else:
        print("Invalid choice!")
    
def split_files():
    print("Start splitting")
    splitter = WikiSplitter()
    splitter.splitFiles()  
    print("Finished splitting")
    
def create_index():
    print("Start indexing")
    Ind = Index()
    Ind.createIndex()
    print("Finished indexing")
    
def make_query(text, model):
    Ind = Index()  
    result = Ind.makeQuery(text, model)
    if result != None:
        num = len(result)
        for x in result:
            print("*********************\n TITLE:")
            print(x['title'])
            print("-----------------------------------------------------------------")
            print(x['textdata'][:100])
            print("-----------------------------------------------------------------")
          #3  print(Calculator.findWordInQuery(text, x))
        print("Results found: ", num)
            
if __name__ == "__main__":
    
    while True:
        display_menu()