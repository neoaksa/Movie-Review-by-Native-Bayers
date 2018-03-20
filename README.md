# Movie-Review-by-Native-Bayers
This program is coded for classificating movie comments to positive and negative, the basic algo is native bayers. 
The data we use is IMDB Movie Review dataset. The code was written in python, and a method of creating two dictionaries was used. Dictionaries consisted of the words in the reviews of each class and conditional probability of each word in two groups(pos, neg) respectively. Since the samples for training in two groups are 50-50 ratio, we set the P(Cj) as 0.5 as default. 
    we use NLTK package to split the sentence to the words and count frequency of each word, see function description on Table 1-1:

Package
Desc
nltk.pos_tag
Append word type
wordnet.lemmatize
Change verb tense to present
Change adjective to ordinal
Change adverb to ordinal
wordnet.morphy
Change plural to singular
stopwords
Filter all stopwords
word_type_list_In
Type of words included
word_type_list_Ex
Type of words excluded( higher priority than included words list according to type level), like some stop words
word_type_Ex
Words excluded. Some useless words like “<”,”br”,”movie”,”film”, etc
ngrams
Combine the words nearby, initial n =2 
Multiprocessing, partial
Multi processors acceleration
