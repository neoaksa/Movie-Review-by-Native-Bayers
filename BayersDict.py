import nltk
import os
import csv
from nltk.util import ngrams


class BayerDict:
    # path: the folder path which contains training text
    def __init__(self):
        self.path = None
        self.dic = {}   # dictionary for saving words
        self.word_size = 0  # the total number of vocabulary
        self.word_type_list_In = ("NN", "VB", "JJ", "RB")   # included words type
        self.word_type_list_Ex = ("VBZ","VBP") # excluded words type

    # read files into dictionary in folder
    # inputpath: input folder with single classfication
    # cat: classfication name
    # outputpath: outputfile address
    # mode: output mode. "a" = append "w"= write
    def readfile(self, inputpath, cat, outputpath, mode):
        self.path = inputpath
        for filename in os.listdir(self.path):
            print(filename)
            # open each file
            filepath = self.path +filename
            with open(filepath,"r",encoding="utf8") as newf:
                txtdata = newf.read()
            # group to n-gram words
            ngram_wordslist = self.__ngramwords(txtdata)
            # move words into dictionary
            for words in ngram_wordslist:
                if words in self.dic:
                    self.dic[words] += 1
                else:
                    self.dic[words] = 1
            self.word_size += len(ngram_wordslist)
        for key in self.dic:
            self.dic[key] = (self.dic[key]+1)/(self.dic[key]+self.word_size)
        print(self.dic)
        print(self.word_size)
        self.__output(outputpath, cat, mode)

    # group n grams words
    def __word_grams(self, words, min, max):
        s = []
        for n in range(min, max):
            for ngram in ngrams(words, n):
                s.append(' '.join(str(i) for i in ngram))
        return s

    # output csv
    # mode: "a" = append "w"= write
    def __output(self, file,cat, mode):
        with open(file,mode, encoding="utf8") as wfile:
            fieldnames = ['word', 'perc', 'category']
            writer = csv.DictWriter(wfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, item in self.dic.items():
                writer.writerow({'word': key, 'perc': item, 'category': cat})

    # txtdata: a utf-8 text string
    def __ngramwords(self, txtdata):
        # temp words list
        temp_wordlist = []
        # analysis words with nltk
        senlist = nltk.sent_tokenize(txtdata, language="english")
        wordlist = []
        for sent in senlist:
            wordlist.append(nltk.word_tokenize(sent, language="english"))
        # add tag for each words
        tags = []
        for tokens in wordlist:
            tags.append(nltk.pos_tag(tokens, lang='eng'))
        # filter words by vocabulary type
        for sent in tags:
            for words in sent:
                # print(words[0] + ":" + words[1])
                if words[1][:2] in self.word_type_list_In and words[1] not in self.word_type_list_Ex:
                    temp_wordlist.append(words[0])
        # create n-gram words
        ngram_wordslist = self.__word_grams(temp_wordlist, 1, 3)
        return ngram_wordslist