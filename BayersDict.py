import nltk
import os
import csv
import operator
import math
from decimal import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer as wnl
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from shutil import copyfile

class BayerDict:
    # path: the folder path which contains training csv files
    def __init__(self):
        self.dic = {}   # dictionary for saving words
        self.word_size = 0  # the total number of vocabulary
        self.word_type_list_In = ("NN" , "VB", "JJ", "RB")   # included words type
        self.word_type_list_Ex = () # excluded words type
        self.word_list_Ex = ("/", "br", "<", ">","be","movie","film","have","do","none","none none") # excluded words
        self.PCpos = Decimal(0.5)  # P(Cpos)
        self.PCneg = Decimal(0.5)  # P(Cneg)

    # read files into dictionary in folder
    # inputpath: input folder with single classfication
    # cat: classfication name
    # outputpath: outputfile address
    # mode: output mode. "a" = append "w"= write
    def readfile(self, inputpath, cat, outputpath, mode):
        for filename in os.listdir(inputpath):
            # print(filename)
            # open each file
            filepath = inputpath +filename
            with open(filepath,"r",encoding="utf8") as newf:
                txtdata = newf.read()
            # group to n-gram words
            ngram_wordslist = self.__ngramwords(txtdata)
            # move words into dictionary
            for words in ngram_wordslist:
                if str(words).lower() in self.word_list_Ex:
                    continue
                elif words in self.dic:
                    self.dic[words] += 1
                else:
                    self.dic[words] = 1
            self.word_size += len(ngram_wordslist)
        # caculate p(n|c) for each word
        # maxd = max(self.dic.items(), key=operator.itemgetter(1))[1]
        # maxp = math.log(10, maxd / (maxd + self.word_size))
        # print(maxp)
        for key in self.dic:
            self.dic[key] = Decimal((self.dic[key]+1)/(self.dic[key]+self.word_size))# / maxp
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
        stop_words = set(stopwords.words('english'))  # set stop words type
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
                # filter stop words
                if words[0] in stop_words:
                    continue
                # print(words[0] + ":" + words[1])
                if words[1][:2] in self.word_type_list_In and words[1] not in self.word_type_list_Ex \
                        and str(words[0]).lower() not in self.word_list_Ex:
                    if words[1][:2] == "VB": # change verb to parent tense
                        add_word = wnl().lemmatize(words[0], "v")
                    elif words[1][:2] == "NN": # change noun to morphy
                        add_word = wordnet.morphy(words[0])
                    elif words[1][:3] in ("JJR","JJS"): # change adj to ordinal
                        add_word = wnl().lemmatize(word=words[0], pos=wordnet.ADJ)
                    elif words[1][:3] in ("RBR","RBS"): # change adv to ordinal
                        add_word = wnl().lemmatize(word=words[0], pos=wordnet.ADV)
                    else:
                        add_word = words[0]
                    temp_wordlist.append(add_word)
        # create n-gram words
        ngram_wordslist = self.__word_grams(temp_wordlist, 1, 3)
        return ngram_wordslist

    # validationpath:  validation folder
    # posdicfile: positive dictionary csv file
    # negdicfile: negtive dictionary csv file
    # catgory: "neg" or "pos" for validation folder
    # maxfilemum: maximun number of validation
    def validation(self,validationpath, posdicfile,negdicfile, catgory, maxfilenum):
        right = 0
        wrong = 0
        filenum = 0
        # read csv into two dictionaries
        posdic = {}
        negdic = {}
        amplif_num = 1
        with open(posdicfile, "r", encoding="utf8") as newf:
            reader = csv.DictReader(newf)
            for row in reader:
                posdic[row["word"]] = Decimal(row["perc"]) *amplif_num
        min_p_posdic = Decimal(1/len(posdic))*amplif_num # minim p
        with open(negdicfile, "r", encoding="utf8") as newf:
            reader = csv.DictReader(newf)
            for row in reader:
                negdic[row["word"]] = Decimal(row["perc"]) *amplif_num
        min_p_negdic = Decimal(1/len(negdic)) *amplif_num # minim p
        # loop file to classfication
        error_pool = ()
        for filename in os.listdir(validationpath):
            # print(filename)
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
                    pos_word_pro *= min_p_posdic
                # neg P
                if words in negdic:
                    neg_word_pro *= negdic[words]
                else:
                    neg_word_pro *= min_p_negdic
                # if words in posdic and words in negdic:
                #     pos_word_pro *= posdic[words]
                #     neg_word_pro *= negdic[words]
            # pick up max one
            if ((pos_word_pro * self.PCpos > neg_word_pro*self.PCneg) \
                and catgory == "pos") \
                or ((pos_word_pro * self.PCpos < neg_word_pro*self.PCneg) \
                and catgory == "neg"):
                right += 1
            else:
                wrong += 1
                print(catgory,":",filename,pos_word_pro, neg_word_pro )
                # please comment this if error
                # copyfile(filepath,"/home/jie/Documents/aclImdb/"+catgory+"_error/"+filename)
        print("-------------------"+ catgory+":"+ str(right/(right+wrong)))