import nltk
import os
import csv
import operator
import math
from decimal import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer as wnl



class BayerDict:
    # path: the folder path which contains training csv files
    def __init__(self):
        self.path = None
        self.dic = {}   # dictionary for saving words
        self.word_size = 0  # the total number of vocabulary
        self.word_type_list_In = ("NN", "VB", "JJ", "RB")   # included words type
        self.word_type_list_Ex = ("VBZ","VBP") # excluded words type
        self.word_list_Ex = ("/", "br", "<", ">") # excluded words
        self.PCpos = Decimal(0.5)  # P(Cpos)
        self.PCneg = Decimal(0.5)  # P(Cneg)

    # read files into dictionary in folder
    # inputpath: input folder with single classfication
    # cat: classfication name
    # outputpath: outputfile address
    # mode: output mode. "a" = append "w"= write
    def readfile(self, inputpath, cat, outputpath, mode):
        self.path = inputpath
        for filename in os.listdir(self.path):
            # print(filename)
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
        # caculate p(n|c) for each word
        maxd = max(self.dic.items(), key=operator.itemgetter(1))[1]
        maxp = math.log(10, maxd / (maxd + self.word_size))
        # print(maxp)
        for key in self.dic:
            self.dic[key] = math.log(10, (self.dic[key]+1)/(self.dic[key]+self.word_size)) / maxp
            # self.dic[key] = (self.dic[key] + 1) / (self.dic[key] + self.word_size)
        # print(self.dic)
        # print(self.word_size)
        self.__output(outputpath, cat, mode)

    # regroup words list to n-gram words list
    # min: minimum n
    # max: maximum n
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

    # transfer a txt to n-gram words list
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
                if words[1][:2] in self.word_type_list_In and words[1] not in self.word_type_list_Ex \
                        and words[0] not in self.word_list_Ex:
                    if words[1][:2] == "VB": # change verb to parent tense
                        add_word = wnl().lemmatize(words[0], "v")
                    else:
                        add_word = words[0]
                    temp_wordlist.append(add_word)
        # create n-gram words
        ngram_wordslist = self.__word_grams(temp_wordlist, 1, 3)
        return ngram_wordslist

    def validation(self,validationpath, posdicfile,negdicfile, catgory, maxfilenum, missingvalue):
        right = 0
        wrong = 0
        filenum = 0
        missingvalue = Decimal(missingvalue)
        # read csv into two dictionaries
        posdic = {}
        negdic = {}
        with open(posdicfile, "r", encoding="utf8") as newf:
            reader = csv.DictReader(newf)
            for row in reader:
                posdic[row["word"]] = Decimal(row["perc"])
        with open(negdicfile, "r", encoding="utf8") as newf:
            reader = csv.DictReader(newf)
            for row in reader:
                negdic[row["word"]] = Decimal(row["perc"])
        # loop file to classfication
        for filename in os.listdir(validationpath):
            print(filename)
            if filenum >= maxfilenum:
                break
            filenum += 1
            pos_word_pro = Decimal(1)
            neg_word_pro = Decimal(1)
            # open each file
            filepath = validationpath + filename
            with open(filepath, "r", encoding="utf8") as newf:
                txtdata = newf.read()
            # group to n-gram words
            ngram_wordslist = self.__ngramwords(txtdata)
            # search each word in two dictionary
            for words in ngram_wordslist:
                # pos P
                if words in posdic:
                    pos_word_pro *= posdic[words]
                else:
                    pos_word_pro *= missingvalue
                # neg P
                if words in negdic:
                    neg_word_pro *= negdic[words]
                else:
                    neg_word_pro *= missingvalue
            # pick up max one
            if ((pos_word_pro * self.PCpos > neg_word_pro*self.PCneg) \
                and catgory == "pos") \
                or ((pos_word_pro * self.PCpos < neg_word_pro*self.PCneg) \
                and catgory == "neg"):
                right += 1
            else:
                wrong += 1
        print(catgory+":"+ str(right/(right+wrong)))