# -*- coding: utf-8 -*-
"""

Main file of the search-engine
"""

from dump_splitter import WikiSplitter
from index_creator import Index
import calc as Calculator

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
        make_query(query)
    elif answer == "4":
        raise SystemExit
    else:
        print("Invalid choice")
    
def split_files():
    print("start splitting")
    splitter = WikiSplitter()
    splitter.splitFiles()  
    print("finish splitting")
    
def create_index():
    print("start indexing")
    Ind = Index()
    Ind.createIndex()
    print("finish indexing")
    
def make_query(text):
    Ind = Index()  
    result = Ind.makeQuery(text)
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