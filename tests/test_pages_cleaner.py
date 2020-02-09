"""
Pulitore di file.

Toglie le [[ ]]:
CASO 1: [[parola1|parola2]]  ->   tengo soltanto parola2
CASO 2: [[parola]]  ->  mi limito a togliere le [[ ]]
CASI SPECIALI -> elimino la riga
    [[File:
    [[Image:
    [[Category:

Tolgo i ''' -> si riferiscono a parole in grassetto
Tolgo i ''  -> si riferiscono a parole in corsivo
"""
from os import listdir
from os.path import isfile, join
import os, io

class Cleaner:
    def findSquareBrackets(self, line):
        i = 0
        start = -1
        end = -1
        char = '['
        flag = False

        while(i + 1 < len(line) and flag == False):
            if(line[i] == char and line[i + 1] == char):
                if char == '[':
                    start = i
                    char = ']'
                else:
                    end = i + 1
                    flag = True

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
        if line.startswith("[[File:") or line.startswith("[[Image:") or line.startswith("[[Category:"):
            return ""
        
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

    def findDoubleApostrophe(self, line):
        i = 0
        start = -1
        end = -1
        char = "'"
        flag = False
        flagStart = False

        while(i + 1 < len(line) and flag == False):
            if(line[i] == char and line[i + 1] == char):
                if flagStart == False:            
                    start = i
                    flagStart = True

                else:
                    end = i + 2
                    flag = True

            i += 1

        return start, end

    def getWordDoubleApostrophe(self, line):
        return line[2 : -2]
    
    def page_cleaner(self, text):
        buff = io.StringIO(text)
        #line = buf.readline()
        data = ""
        for line in buff:
            start, end = self.findSquareBrackets(line)
            startTA, endTA = self.findTripleApostrophe(line)
            startDA, endDA = self.findDoubleApostrophe(line)
            flag = False
            
            while((start != -1 and end != -1) or (startTA != -1 and endTA != -1) or (startDA != -1 and endDA != -1)):
                 startTA, endTA = self.findTripleApostrophe(line)
                 if startTA != -1 and endTA != -1:
                    line = line.replace(line[startTA : endTA], self.getWordTripleApostrophe(line[startTA : endTA]))
                    startTA, endTA = self.findTripleApostrophe(line)

                 startDA, endDA = self.findDoubleApostrophe(line)
                 if startDA != -1 and endDA != -1:
                    line = line.replace(line[startDA : endDA], self.getWordDoubleApostrophe(line[startDA : endDA]))
                    startDA, endDA = self.findDoubleApostrophe(line)
                
                 start, end = self.findSquareBrackets(line)
                 if start != -1 and end != -1:
                    word = line[start : end + 1]
                    replace = self.wordToReplace(line[start : end + 1])

                    if replace == "":
                        flag = True
                    line = line.replace(word, replace)

                    start, end = self.findSquareBrackets(line)
             
            if(line == '\n') and flag == True:
                flag = False
            else:    
                data += line 

        print(data)
        return data  


# ____________
#c = Cleaner()

#fin = open("pages" + os.path.sep + "14.txt", "rt")
#text = fin.read()
#c.page_cleaner(text)
'''
folder = "pages"
files = [f for f in listdir(folder) if isfile(join(folder, f))]

for page in files:
    print(page)
    #fin = open(folder + os.path.sep + page, "rt")
    #data = fin.read()

    with io.open(folder + os.path.sep + page, "rt", encoding="utf-8") as fin:
        data = ""
        for line in fin:
            start, end = findSquareBrackets(line)
            startTA, endTA = findTripleApostrophe(line)
            startDA, endDA = findDoubleApostrophe(line)
            flag = False

            while((start != -1 and end != -1) or (startTA != -1 and endTA != -1) or (startDA != -1 and endDA != -1)):
                #print(str(start) + " " + str(end) + " " + line[start:end+1] + " " + wordToReplace(line[start:end+1]))
                #print(line[end-1])
                 
                 if startTA != -1 and endTA != -1:
                    line = line.replace(line[startTA : endTA], getWordTripleApostrophe(line[startTA : endTA]))
                    startTA, endTA = findTripleApostrophe(line)

                 startDA, endDA = findDoubleApostrophe(line)
                 if startDA != -1 and endDA != -1:
                    line = line.replace(line[startDA : endDA], getWordDoubleApostrophe(line[startDA : endDA]))
                    startDA, endDA = findDoubleApostrophe(line)
                
                 start, end = findSquareBrackets(line)
                 if start != -1 and end != -1:
                    word = line[start : end + 1]
                    replace = wordToReplace(line[start : end + 1])

                    if replace == "":
                        flag = True
                    line = line.replace(word, replace)

                    start, end = findSquareBrackets(line)
                
                 
                 
            if(line == '\n') and flag == True:
                flag = False
            else:    
                data += line   

    fin.close()

    fin = io.open(folder + os.path.sep + page, "wt",encoding="utf-8")
    fin.write(data)
    fin.close()
'''
