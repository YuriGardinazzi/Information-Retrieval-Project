# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 20:18:47 2020

This test it's like test_splitting_dump_1.py but it works with 
dumps retrieved from https://en.wikipedia.org/wiki/Special:Export
useful link: https://en.wikipedia.org/wiki/Help:Export
It saves documents as <id> 
                      <title>
                      <text>
if the field text has the attribute bytes < Min_byte it doesn't save the file
              
"""
        
import bz2
import xml.sax
import os.path


class PagesHandler( xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.id = ""
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
                self.id = ""
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
        elif self.CurrentData == "id":
            self.id += content
        elif self.CurrentData == "text":
            self.text += content
        elif self.CurrentData == "format":
            self.format += content

    def savePage(self):
        """Save id,title,text attributes in a file named self.pageCounter.txt"""
        data = str(self.id) +"\n" + self.title +"\n"+self.text

        directory = 'pages'
        filename = str(self.pageCounter)+ ".txt"
        file_path = os.path.join(directory, filename)

        print("file path: ", file_path)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "wb")
        file.write(data.encode()) #data.encode  <= str to byte
        file.close()


        print(r'Saved file: ',self.pageCounter, ".txt")





if (__name__ == "__main__"):

    filename = "custom_wikipedia.xml"

    parser = xml.sax.make_parser() #create XMLReader
    Handler = PagesHandler()
    parser.setContentHandler(Handler)
    parser.parse(filename)
