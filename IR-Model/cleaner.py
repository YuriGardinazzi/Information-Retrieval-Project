# -*- coding: utf-8 -*-
"""
Cleaner modules, it cleans raw text data
"""

from os import listdir
from os.path import isfile, join
import os, io

class Cleaner:
    def findDoubleSign(self, line, simbleStart, simbleEnd):
        i = 0
        start = -1
        end = -1
        char = simbleStart
        flag = False
        startFind = False

        while(i + 1 < len(line) and flag == False):
            if(line[i] == char and line[i + 1] == char):
                if char == simbleStart and startFind == False:
                    start = i
                    char = simbleEnd
                    startFind = True
                
                elif char == simbleEnd and startFind == True:
                    end = i + 2
                    flag = True

            i += 1

        return start, end

    def findSquareBrackets(self, line, simbleStart, simbleEnd):
        i = 0
        start = -1
        end = -1
        char = simbleStart
        flag = False
        nested = False
        startFind = False

        
        if line.startswith("[[File:") or line.startswith("[[Image:") or line.startswith("[[Category:"):
            return -2, -2

        while(i + 1 < len(line) and flag == False):
            if(line[i] == char and line[i + 1] == char):
                if char == simbleStart:
                    if startFind == False:
                        start = i
                        char = simbleEnd
                        startFind = True
                    else:
                        nested = True   
                else:
                    if char == simbleEnd and startFind == True and nested == False:
                        end = i + 2
                        flag = True
                    else: 
                        if char == simbleEnd and nested == True:
                            nested = False
            i += 1

        return start, end

    # input: substring, string between [[ ]] with brackets included
    def twoWordInSquareBrackets(self, line):
        for c in line:
            if c == '|':
                return line.index(c)

        return -1

    # input: substring, string between [[ ]] with brackets included
    def wordToReplace(self, line):
        index = self.twoWordInSquareBrackets(line)

        if index == -1:
            return line[2 : -2]

        else:
            return line[index + 1 : -2]

    def findTripleApostrophe(self, line):
        i = 0
        start = -1
        end = -1
        char = "'"
        flag = False
        flagStart = False

        while(i + 2 < len(line) and flag == False):
            if(line[i] == char and line[i + 1] == char and line[i + 2] == char):
                if flagStart == False:            
                    start = i
                    flagStart = True

                else:
                    end = i + 3
                    flag = True

            i += 1

        return start, end

    def getWordTripleApostrophe(self, line):
        return line[3 : -3]
    
    def getWordDoubleSign(self, line):
        return line[2 : -2]       
        
    
    def page_cleaner(self, text):

        buff = io.StringIO(text)

        data = ""
        for line in buff:
            if line[0] == '|' or (line[0] == ' ' and line[1] == '|'):
                line = ""
            start, end = self.findSquareBrackets(line, '[', ']')
            startTA, endTA = self.findTripleApostrophe(line)
            startDA, endDA = self.findDoubleSign(line, "'", "'")
            startEq, endEq = self.findDoubleSign(line, '=', '=')
            startBr, endBr = self.findDoubleSign(line, '{', '}')
            flag = False
            
            while((start != -1 and end != -1) or (startTA != -1 and endTA != -1) \
                or (startDA != -1 and endDA != -1) or (startEq != -1 and endEq != -1) or (startBr != -1 and endBr != -1)):
                
                start, end = self.findSquareBrackets(line, '[', ']')
                if start == -2 and end == -2:
                    line = line.replace(line, "")
                    start, end = self.findSquareBrackets(line, '[', ']') 
                elif start != -1 and end != -1:
                    word = line[start : end]
                    replace = self.wordToReplace(line[start : end])
                    if replace == "":
                        flag = True
                    line = line.replace(word, replace)

                    start, end = self.findSquareBrackets(line, '[', ']')                
                
                startTA, endTA = self.findTripleApostrophe(line)
                if startTA != -1 and endTA != -1:
                    print(line[startTA : endTA])
                    print(self.getWordTripleApostrophe(line[startTA : endTA]))
                    line = line.replace(line[startTA : endTA], self.getWordTripleApostrophe(line[startTA : endTA]))
                    startTA, endTA = self.findTripleApostrophe(line)
                    print("LINE " + line)
                
                
                startDA, endDA = self.findDoubleSign(line, "'", "'")
                if startDA != -1 and endDA != -1:
                    line = line.replace(line[startDA : endDA], self.getWordDoubleSign(line[startDA : endDA]))
                    print(self.getWordDoubleSign(line[startDA : endDA]))
                    startDA, endDA = self.findDoubleSign(line, "'", "'")

                startEq, endEq = self.findDoubleSign(line, '=', '=')
                if startEq != -1 and endEq != -1:
                    line = line.replace(line[startEq : endEq], self.getWordDoubleSign(line[startEq : endEq]))
                    startEq, endEq = self.findDoubleSign(line, '=', '=')

                startBr, endBr = self.findDoubleSign(line, '{', '}')
                if startBr != -1 and endBr != -1:
                    print(line[startBr : endBr])
                    line = line.replace(line[startBr : endBr], "")
                    startBr, endBr = self.findDoubleSign(line, '{', '}')
             
            if(line == '\n'):  # tolto and flag == True per togliere le righe vuote
                flag = False
            elif line != '\n' and line != "*\n" and line != "* \n":    
                data += line
        
        data = data.replace("()", "")
        data = data.replace("( )", "")
        data = data.replace("===", "")
        # Per togliere {{ }} su più righe
        startBr, endBr = self.findDoubleSign(data, '{', '}')
        while(startBr != -1 and endBr != -1):
            print(data[startBr : endBr])
            data = data.replace(data[startBr : endBr], "")
            startBr, endBr = self.findDoubleSign(data, '{', '}')
          
        return data
