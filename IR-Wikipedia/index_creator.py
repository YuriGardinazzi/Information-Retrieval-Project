# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 18:24:22 2020

@author: Yuri
"""

from whoosh.index import create_in, open_dir
from whoosh.fields import *
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
        #NGRAMWORDS è meglio di NGRAM perché non considera la punteggiatura e gli spazi
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT,textdata= TEXT(stored=True), nTitle= NGRAMWORDS(2,4))

    def createSchema(self): #aggiungere parametri per schemi personalizzati
        '''create a schema for the index'''
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT,textdata= TEXT(stored=True), nTitle= NGRAM(2,4))
       
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
                writer.add_document(title=doc_title, path=path, content=text,textdata=text, nTitle=doc_title)
                fp.close()
        writer.commit()

             
         
    def makeQuery(self,input_query, weighting, index_directory = 'index_dir'):
        '''Input_query = query to search
           index_diretory: if different from index_dir'''
           
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
             results = searcher.search(corrected.query)
        else:
            results = searcher.search(query)
                
        if len(results) == 0:
            print("Empty Result")
            return None
        else:
            return results
        
        