# -*- coding: utf-8 -*-
"""

Main file to use the search engine from terminal
"""

from dump_splitter import WikiSplitter
from index_creator import Index
import nltk
from nltk.corpus import wordnet
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from remove_duplicates import remove_duplicate_files

def display_menu():
    print("""
          1. Create Index
          2. Create Pages
          3. Search something
          4. Get Suggestion
          6. Try Did you mean
          7. Get Expanded terms
          8. Exit
          """)
    answer = input("What would you like to do? ")
    if answer == "1":
        create_index()
    elif answer == "2":
        split_files()
        #remove duplicates as well
        remove_duplicate_files()
    elif answer == "3":
        query = str(input("Insert a term to search: "))
        choose_model(query)
    elif answer == "4":
        query = str(input("Insert a term to search: "))
        print(getSuggestion(query))
    elif answer == "6":
        query = str(input("Insert a term to search: "))
        print(get_did_you_mean(query))
    elif answer == "7":
        query = str(input("Insert a term to search: "))
        print(get_expanded_terms(query))
    elif answer == "8":
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
    else:
        print("Invalid choice!")
    
def split_files():

    splitter = WikiSplitter()
    splitter.splitFiles()  

    
def create_index():
    print("Start indexing")
    Ind = Index()
    Ind.createIndex()
    print("Finished indexing")
    
def make_query(text, model="default"):
    Ind = Index()  
    result = Ind.makeQuery(text, model)
    if result != None:
        num = len(result)
        for x in result:
            print("*********************\n TITLE:")
            print(x['title'])
            print("PATH: ", x['path'])
            print("-----------------------------------------------------------------")
            print(x['textdata'][:100])
            print("-----------------------------------------------------------------")
        print("Results found: ", num)
        
def getSuggestion(input_query,num = 3, index_directory ='index_dir'):
         ix = open_dir(index_directory)
         searcher = ix.searcher()
         parser = QueryParser("nTitle", schema=ix.schema)
         query = parser.parse(input_query)
         results = searcher.search(query)
         dim_res = len(results)

         if (dim_res > num):
             return [x['title'][:-1] for x in results[:num]]
         else:
             return [x['title'][:-1] for x in results[:num]]       

def get_expanded_terms(input_query):
    
    
    query_words = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(input_query)) if pos[0] == 'N']
    query_words = [x.lower() for x in query_words]
    print(query_words)
    result = ""
    for word in query_words:
        if(len(wordnet.synsets(word)) > 1):                
            syn =  wordnet.synsets(word)[0]
            if len(syn.lemmas()) >= 2:    
                result += " " + syn.lemmas()[1].name()

                 
    return result
def get_did_you_mean(input_query,index_directory ='index_dir'):
     ix = open_dir(index_directory)
     searcher = ix.searcher()
     parser = QueryParser("content", schema=ix.schema)
     query = parser.parse(input_query) 
     #Query-corrector
     corrected = searcher.correct_query(query, input_query)
     if corrected.query != query:
         return(True, corrected.string)
     return(False, input_query)
    
def get_retrieved_pages(text, model="default"):
    Ind = Index()
    result = Ind.makeQuery(text,model)
    if result != None:
        result_pages=[]
        for x in result:
              result_pages.append((x['title'], x['textdata'][:300]))
        return result_pages

if __name__ == "__main__":
    while True:
        display_menu()