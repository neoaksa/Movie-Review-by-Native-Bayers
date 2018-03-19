from nltk.stem.wordnet import WordNetLemmatizer as wnl
from nltk.corpus import wordnet

wnl = wnl()
print(wnl.lemmatize( word="worse", pos=wordnet.ADJ))

dic = {"a":1,"b":2,"c":3}
print(len(dic))