#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Query tester with a custom query
"""

import searching_test_1 as search
import indexing_test_1 as index

class QueryTester:
    def inputQuery(self):
        str = input("Input a query: " )
        search.searchQuery(self, str)
        
#setup
index.createIndex()

qt = QueryTester()
qt.inputQuery()


        


