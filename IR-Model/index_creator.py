# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 18:24:22 2020

@author: Yuri
"""

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh import analysis
from whoosh import query as queryy
from whoosh.formats import Frequency
from whoosh.qparser import QueryParser
from whoosh.scoring import WeightingModel
from whoosh.scoring import Weighting
from whoosh.scoring import PL2

from math import log

import os, os.path, io, shutil

class Cosine(Weighting):
    """A cosine vector-space scoring algorithm, translated into Python
    from Terrier's Java implementation.
    """

    def score(self, searcher, fieldnum, text, docnum, weight, QTF=1):
        idf = searcher.idf(fieldnum, text)

        DTW = (1.0 + log(weight)) * idf
        QMF = 1.0 # TODO: Fix this
        QTW = ((0.5 + (0.5 * QTF / QMF))) * idf
        return DTW * QTW
    
class Index:
    
    def __init__(self,index_directory = 'index_dir', input_files = 'pages'):
        '''
           Initialize index parameters
           optional parameters: index_directory if different from index_dir
           input_files: if different from pages'''
        #creation of the schema
        self.directory = index_directory
        self.files_path = input_files
        #self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(), textdata=TEXT(stored=True))
        #analyzer = analysis.StandardAnalyzer(stoplist = frozenset(['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may', 'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are']))
        analyzer = analysis.StemmingAnalyzer()
        vector_format = Frequency()
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(analyzer=analyzer, vector=vector_format, stored=True), links = STORED, textdata=TEXT(stored=True))
   
    def createSchema(self): #aggiungere parametri per schemi personalizzati
        '''create a schema for the index'''
        analyzer = StandardAnalyzer(stoplist=ENGLISH_STOP_WORDS)
        vector_format = formats.Frequency(analyzer)
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(analyzer=analyzer, vector=vector_format), links = STORED, textdata=TEXT(stored=True))
        
    def createIndex(self):
        ''' Create an index and delete existing ones'''
        #check if there's a directory
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        else:
            shutil.rmtree(self.directory)
            print("Eliminated old indexes")
            os.mkdir(self.directory)
        #creation of the index
        ix = create_in(self.directory, self.schema)
        print("Created index")
        
        writer = ix.writer()
        #adding entries to the index

        filepaths = [os.path.join(self.files_path,i) for i in os.listdir(self.files_path)]
        print("Documents read: ", filepaths)
        for path in filepaths:
                fp = io.open(path,'r',encoding="utf-8")
                doc_title = fp.readline()
                print(path, " ", doc_title)
                text = fp.read()
                #title it's not the real title of the document but just the filename
                writer.add_document(title=doc_title, path=path, content=text,textdata=text)
                fp.close()
        writer.commit()
    
    def makeQuery(self,input_query, weighting, expanse_val, index_directory = 'index_dir'):
        '''Input_query = query to search
           index_diretory: if different from index_dir'''
        if index_directory != self.directory:
            self.directory
           
        ix = open_dir(index_directory)

        if(weighting == "default"):
            searcher = ix.searcher()
        elif(weighting == "cosine"):
            searcher = ix.searcher(weighting=Cosine)
        elif(weighting == "pl2"):
            searcher = ix.searcher(weighting=PL2)
            
                 
        parser = QueryParser("content", schema=ix.schema)
        query = parser.parse(input_query)  
        
        #Query-corrector
        corrected = searcher.correct_query(query, input_query)
        if corrected.query != query:
             print("Did you mean:", corrected.string)
             results = searcher.search(corrected.query, limit = 10)
        else:
            results = searcher.search(query, limit = 10)
        
        #Query-expansion (blank return atm)
        if expanse_val:
            number = int(input("Which document do you want to expand? "))
            docnum = results.docnum(number)
            key_terms = list(searcher.key_terms([docnum], "content", numterms=5))
            #print key_terms (debug purposes)
            for t in key_terms:
                print(t)
        
            """
            problem lines imo
            """
            new_query = queryy.Or([queryy.Term("content", t) for t in key_terms])
            results = searcher.search(new_query, limit = 10)
            
            #first_hit = results[0]
            #more_results = first_hit.more_like_this("content")
            #return more_results
        else:  
            if len(results) == 0:
                print("Empty Result")
                return None
            else:
                return results
            
        