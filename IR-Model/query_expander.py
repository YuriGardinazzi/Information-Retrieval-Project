#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:56:47 2020

Query Expansion
@author: gabri
"""

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

def queryExpander(old_query):
    while True: 
        if not old_query:
            break
        tokenized_query = word_tokenize(old_query)
        
        count = 0
        print("Words available: ")
        for tok in tokenized_query:
            print(str(count) + ")" + str(tok))
            count +=1
        answer = int(input("Choose a term: "))
        count = 0
        
        #find synonyms of a certain word
        synonyms = []
        for syn in wordnet.synsets(tokenized_query[answer]):
            for l in syn.lemmas():
                synonyms.append(l.name())
        
        if len(synonyms) == 0:
            print("No expansion done! Old query will be returned! ")
            return old_query
        for w in synonyms:
            print(str(count) + ")" + str(w))
            count +=1
        answer = int(input("Choose a synonym: "))
        
        #clean string
        transf = synonyms[answer].lower().replace("_", " ")
        new_query = " ".join([str(old_query), transf])
        
        return new_query
    