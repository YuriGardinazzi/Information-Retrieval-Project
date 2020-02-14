#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions to calculate ndcg and such (WiP)
"""

from nltk.corpus import wordnet

"""
Obtain set of relevant terms from a search term
"""
def obtainTerms(query):
    words = query.split(" ")
    relevant_terms = {}
    
    for word in words:
        #relevant_terms.append(word)
        relevant_terms[word] = 0
        #populate relevant_terms list
        for syn in wordnet.synsets(word):
            for name in syn.lemma_names():
                relevant_terms[name] = 0
            # relevant_terms.append(l.name(), 0)

    return relevant_terms
        
"""
Use list of search term + relevant terms to it to find the relevance of
a term in a query result
"""

def findWordInQuery(query, result_page):
    relevance_num = 0;
    words_list = obtainTerms(query)
    
    #total length used to calculate frequency
    total_length = len(result_page['title'].split()) + len(result_page['textdata'].split())
    print("Lunghezza: ")
    print(total_length)
    #find relevant words in the pages and update their frequency (value of a key in a dict)
    #TODO: non funziona il calcolo perché non trova le parole
    for word in words_list:
        if result_page != None:
            if word in result_page['title']:
                words_list[word] + 1
                print(words_list[word])
            for line in result_page['textdata']:
                if word in line:
                    words_list[word] + 1
                    print(words_list[word])
                    
        #update dictionary with relative frequencies
        words_list[word] /= total_length
        #update relevance general value of a query wrt a specific page result
        relevance_num += words_list[word]
        
    return relevance_num

