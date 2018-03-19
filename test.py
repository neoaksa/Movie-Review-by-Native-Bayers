import nltk

senlist = nltk.sent_tokenize("None is good", language="english")
words = nltk.word_tokenize(senlist[0], language="english")
print(words)
print(nltk.pos_tag(senlist[0], lang='eng'))