# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 18:24:22 2020

@author: Yuri
"""

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path, io, shutil

class Index:
    
    def __init__(self,index_directory = 'index_dir', input_files = 'pages'):
        '''
           Initialize index parameters
           optional parameters: index_directory if different from index_dir
           input_files: if different from pages'''
        #creation of the schema
        self.directory = index_directory
        self.files_path = input_files
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))

   
    def createSchema(self): #aggiungere parametri per schemi personalizzati
        '''create a schema for the index'''
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT, textdata=TEXT(stored=True))
        
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
                print(path)
                text = fp.read()
                #title it's not the real title of the document but just the filename
                writer.add_document(title=(os.path.split(path))[1], path=path, content=text,textdata=text)
                fp.close()
        writer.commit()
    
    def makeQuery(self,input_query,index_directory = 'index_dir'):
        '''Input_query = query to search
           index_diretory: if different from index_dir'''
        if index_directory != self.directory:
            self.directory
           
        ix = open_dir(index_directory)
        searcher = ix.searcher()
        parser = QueryParser("content", schema=ix.schema)
        query = parser.parse(input_query)  
        results = searcher.search(query)
        
        if len(results) == 0:
            print("Empty Result")
            return None
        else:
            return results
        
        