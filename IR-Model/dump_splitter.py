# -*- coding: utf-8 -*-
"""
This file splits custom_wikipedia.xml into single .txt files inside the folder "pages"
"""
import xml.sax
import os.path, io
from cleaner import Cleaner


class PagesHandler( xml.sax.ContentHandler):
    '''This class is Handler for the wikipedia dump that saves retrieved files
    into an input folder or the default one "pages" '''
    def __init__(self, input_directory = 'pages'):
        self.directory = input_directory
        self.CurrentData = ""
        self.title = ""
        self.text = ""
        self.pageCounter = 0
        self.MAX_PAGE = 300
        self.MIN_BYTES = 2000
        self.bytes = 0
        self.format = ""

    def startElement(self, tag, attributes):
        """Call when an element starts"""
        self.CurrentData = tag

        if tag == "page":
            if self.pageCounter < self.MAX_PAGE:
                print("inizio pagina #", self.pageCounter)
        if tag == "text":
            self.bytes = int(attributes["bytes"])

    def endElement(self, tag):
        """Call when an element ends"""
        if tag == "page":
            if self.format == "text/x-wiki":
                self.pageCounter += 1
                if self.pageCounter < self.MAX_PAGE and self.bytes >= self.MIN_BYTES:
                    print("fine pagina")
                    self.savePage()
            else:
                self.title = ""
                self.text = ""
                self.format = ""
                self.bytes = 0
                return
        #reset current data field because the element ended
        self.CurrentData = ""

    def characters(self,content):
        """Call when a character is read"""
        if self.CurrentData == "title":
            self.title += content
        elif self.CurrentData == "text":
            self.text += content
        elif self.CurrentData == "format":
            self.format += content

    def savePage(self):
        """Save id,title,text attributes in a file named self.pageCounter.txt"""
        data = self.title +"\n"+ Cleaner().page_cleaner(self.text)

        
        filename = str(self.pageCounter)+ ".txt"
        file_path = os.path.join(self.directory, filename)

        print("file path: ", file_path)
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
            
        file = io.open(file_path, "w",encoding="utf-8")
        file.write(data)
        file.close()

        print(r'Saved file: ',self.pageCounter, ".txt")

class WikiSplitter():
    '''Splitter class, it splits a dump into many *.txt files inside a folder'''
    def __init__(self, input_file = "custom_wikipedia.xml"):
        self.filename = input_file
        
    def splitFiles(self):
        parser = xml.sax.make_parser() #create XMLReader
        Handler = PagesHandler()
        parser.setContentHandler(Handler)
        parser.parse(self.filename)

        













