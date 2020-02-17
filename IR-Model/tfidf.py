#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 23:36:01 2020

@author: gabri
"""

from whoosh.scoring import WeightingModel

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

#from nltk.corpus import stopwords
#from nltk.stem import PorterStemmer
#from collections import Counter
#from num2words import num2words


class queryExpander():
    
    def __init__(self, results, searcher, input_query):
        self.results = results
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
        #choose best term
        best_term = min(tokens, key = tokens.get)
        return best_term
    
#    def preProcess(data):
#        
#        def convert_lower_case(data):
#            return np.char.lower(data)
#        
#        def remove_stop_words(data):
#            stop_words = stopwords.words('english')
#            words = word_tokenize(str(data))
#            new_text = ""
#            for w in words:
#                if w not in stop_words and len(w) > 1:
#                    new_text = new_text + " " + w
#            return new_text
#        
#        def remove_punctuation(data):
#            symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
#            for i in range(len(symbols)):
#                data = np.char.replace(data, symbols[i], ' ')
#                data = np.char.replace(data, "  ", " ")
#            data = np.char.replace(data, ',', '')
#            return data
#        
#        def remove_apostrophe(data):
#            return np.char.replace(data, "'", "")
#        
#        def stemming(data):
#            stemmer= PorterStemmer()
#            
#            tokens = word_tokenize(str(data))
#            new_text = ""
#            for w in tokens:
#                new_text = new_text + " " + stemmer.stem(w)
#            return new_text
#        
#        def convert_numbers(data):
#            tokens = word_tokenize(str(data))
#            new_text = ""
#            for w in tokens:
#                try:
#                    w = num2words(int(w))
#                except:
#                    a = 0
#                new_text = new_text + " " + w
#            new_text = np.char.replace(new_text, "-", " ")
#            return new_text
#        
#        data = convert_lower_case(data)
#        data = remove_punctuation(data) #remove comma seperately
#        data = remove_apostrophe(data)
#        data = remove_stop_words(data)
#        data = convert_numbers(data)
#        data = stemming(data)
#        data = remove_punctuation(data)
#        data = convert_numbers(data)
#        data = stemming(data) #needed again as we need to stem the words
#        data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
#        data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
#        return data
    
    
    def buildExpandedQuery(self, results, searcher, input_query):
        #find term
        term = self.calcTfIdf(self, results, self.tokenizeQuery(self, input_query))
        
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
        
        print("query expanded")
        return new_query
    
   
    
    