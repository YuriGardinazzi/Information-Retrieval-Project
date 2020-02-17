#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Query-expander based on the idf of the terms of the query
"""

from whoosh.scoring import WeightingModel

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

class queryExpander():
    
    def __init__(self, searcher, input_query):
        self.searcher = searcher
        self.input_query = input_query
        
    def tokenizeQuery(self, input_query):
        while True:
            if not input_query:
                break
            #build dict with the tokens of the input_query (key: name, value: idf)
            tokens = {}
            tokenized_query = word_tokenize(input_query)
            for word in tokenized_query:
                tokens[word] = 0
                
            return tokens
   
    def calcTfIdf(self, searcher, tokens):
        #update with idf
        for word, value in tokens.items():
            tokens[word] = WeightingModel.idf(self, searcher, "title", word) + WeightingModel.idf(self, searcher, "content", word)
        #choose best term (high idf = rare term -> can be used more effectively than a common one)
        best_term = max(tokens, key = tokens.get)
        return best_term    
    
    def buildExpandedQuery(self, searcher, input_query):
        #find term
        tokens = self.tokenizeQuery(self, input_query)
        term = self.calcTfIdf(self, searcher, tokens)
        
        #find synonyms of a certain word
        synonyms = []
        for syn in wordnet.synsets(term):
            for l in syn.lemmas():
                synonyms.append(l.name())
        
        count = 0
        
        if len(synonyms) == 0:
            print("No expansion done! Old query will be returned! ")
            return input_query
    
        for w in synonyms:
            print(str(count) + ")" + str(w))
            count +=1
        answer = int(input("Choose a synonym: "))
        #clean string
        transf = synonyms[answer].lower().replace("_", " ")
        new_query = " ".join([str(input_query), transf])
        
        print("query expanded: " + new_query)
        return new_query
    
   
    
    