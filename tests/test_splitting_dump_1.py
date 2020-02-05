# -*- coding: utf-8 -*-
"""
This test aim to split a decompressed chunk into many files .xml
A single file consists of the elements inside the tag <page>, in particular
<id>, <title> and <text>
_____________________________________________________________________

Useful links:
http://etutorials.org/Programming/Python+tutorial/Part+IV+Network+and+Web+Programming/Chapter+23.+Structured+Text+XML/23.2+Parsing+XML+with+SAX/
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
		self.maxPage = 1000
	
	def startElement(self, tag, attributes):
		'''Call when an element starts'''
		self.CurrentData = tag
		#if tag == "title":
		#	print("****************")
		if tag == "page":
			if self.pageCounter < self.maxPage:
				print("inizio pagina #", self.pageCounter)
	def endElement(self, tag):
		'''	Call when an element ends'''
		""""
		if self.CurrentData == "id":
			#print("ID: ", self.id)
		elif self.CurrentData == "title":
			#print("TITLE: ", self.title)
		elif self.CurrentData == "text":
			#print("TEXT: \n", self.text)
		"""
		if tag == "page":
			self.pageCounter += 1
			if self.pageCounter < self.maxPage:
				print("fine pagina")
				self.savePage()
			else:
				return
		#reset current data field because the element ended
		self.CurrentData = "" 

	def characters(self,content):
		''' Call when a character is read'''
		if self.CurrentData == "title":
			self.title = content
		elif self.CurrentData == "id":
			self.id = content
		elif self.CurrentData == "text":
			self.text = content

	def savePage(self):
		
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
	
	filename = "itwikictionary.xml.bz2"
	zipfile = bz2.BZ2File(filename) # open the file
	data = zipfile.read() # get the decompressed M bytes

	newfile = filename[:-4] #take the file name withotu ".bz2"
	open(newfile,"wb").write(data)
	zipfile.close()

	
	parser = xml.sax.make_parser() #create XMLReader
	parser.setFeature(xml.sax.handler.feature_namespaces, 0) #turn off namespaces
	parser.setFeature(xml.sax.handler.feature_validation, 0)
	parser.setFeature(xml.sax.handler.feature_validation,0)
	Handler = PagesHandler()
	parser.setContentHandler(Handler)
	
	parser.parse(newfile)
	
	