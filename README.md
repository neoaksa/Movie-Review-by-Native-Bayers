

**Naive Bayes Document Classification**

 The data used is the IMDB Movie Review dataset. The code was written in python, and a method of creating two dictionaries was used. Dictionaries consisted of the words in the reviews of each class and conditional probability of each word in two groups (positive, negative) respectively. Since the samples for training in two groups are 50-50 ratio, we set the P(Cj) as 0.5 as default.

 We used the NLTK package to split the sentence to the words and count frequency of each word, see function description in Table 1-1:

| **Package** | **Desc** |
| --- | --- |
| nltk.pos\_tag | Append word type |
| wordnet.lemmatize | Change verb tense to presentChange adjective to ordinalChange adverb to ordinal |
| wordnet.morphy | Change plural to singular |
| stopwords | Filter all stopwords |
| word\_type\_list\_In | Type of words included |
| word\_type\_list\_Ex | Type of words excluded( higher priority than included words list according to type level), like some stop words |
| word\_type\_Ex | Words excluded. Some useless words like &quot;&lt;&quot;,&quot;br&quot;,&quot;movie&quot;,&quot;film&quot;, etc |
| ngrams | Combine the words nearby, initial n =2 |
| Multiprocessing, partial | Multi processors acceleration |

Table 1-1. The packages used and their brief description.

 Since P(w|C) is very small number, we set the type of P as decimal. In the process of generating dictionaries and validation, we code multiprocessing to accelerate these processes.If the word doesn&#39;t exit either of two dictionaries, we will use 1/total number of dictionary as conditional probability which is a very tiny number.

 A dictionary without any filter will be huge and full of noisey words. Thus, we only keep

**Effectiveness of Classifier**

 To assess the effectiveness of the model, we determined the accuracy of positive and negative reviews using the provided test set. Since there are over 12,000 samples for each positive and negative test sets, we randomly selected examples to validate our model. Taking an increasing number of samples in the validation step gives us a decent idea of the true accuracy of the model. Using 5,000 validation samples, the accuracy of correctly predicting a positive review was 0.7088, while that for a negative review was 0.9422. The results are shown in Table 2-1.


|**Validation Samples** | **Positive Accuracy** | **Negative Accuracy** |
| --- | --- | --- |
| 50 | 0.76 | 0.90 |
| 100 | 0.71 | 0.93 |
| 500 | 0.736 | 0.942 |
| 1000 | 0.742 | 0.955 |
| 2000 | 0.722 | 0.9475 |
| 5000 | 0.7088 | 0.9422 |

Table 2-1. Positive and negative accuracy for different numbers of validation samples for 2-gram model.

 Since the above model used n-grams of 2, the next model we tried used n-grams of 3. The same relative pattern emerged, with the model more accurately classifying negative reviews. However, this time at 5,000 validation samples, the positive accuracy is slightly less for the 3-gram model than the 2-gram model, while the the negative accuracy is slightly higher. The results are shown in Table 2-2.

| **Validation Samples** | **Positive Accuracy** | **Negative Accuracy** |
| --- | --- | --- |
| 50 | 0.70 | 0.92 |
| 100 | 0.70 | 0.93 |
| 500 | 0.702 | 0.956 |
| 1000 | 0.702 | 0.965 |
| 2000 | 0.681 | 0.9575 |
| 5000 | 0.6674 | 0.9536 |

Table 2-2. Positive and negative accuracy for different numbers of validation samples for 3-gram model.

 To get a deeper understanding of how changing the value of n in the n-gram function, n was set to 10 for the following testing. The positive accuracy is much lower for the 10-gram model compared to the 2- and 3-gram models, while the negative accuracy is slightly higher.

| **Validation Samples** | **Positive Accuracy** | **Negative Accuracy** |
| --- | --- | --- |
| 50 | 0.44 | 1.0 |
| 100 | 0.42 | 1.0 |
| 500 | 0.44 | 0.99 |
| 1000 | 0.453 | 0.992 |
| 2000 | 0.429 | 0.9895 |
| 5000 | 0.4144 |



 The above were all without excluding first and third person present tense verbs via the nltk package. We decided to remove those verbs and rerun the model. The following analysis excludes them.The different levels of n-grams were tested with 5,000 validation samples. While the negative accuracy decreased slightly, the positive accuracy increased. The greatest accuracy increase for the positive class came when the first and third person present tense verbs were excluded for the 10-gram model, as it increased from 41.4% to 51.4%. Although this is a substantial increase, 51% accuracy is not great. The decrease in negative accuracy is not much to worry about, as it remains over 90% for each of the three models. The results can be seen in Table 2-4.

| **n-gram** | **Positive Accuracy** | **Negative Accuracy** |
| --- | --- | --- |
| 2 | 0.7624 | 0.9186 |
| 3 | 0.7132 | 0.9314 |
| 10 | 0.5148 | 0.9786 |

Table 2-4. Positive and negative accuracy for different n-gram models without first and third person present tense verbs.

**Results**

 As mentioned above, the model was much better at classifying negative reviews than positive ones. Without looking at the actual reviews, this must mean that there are some words that occur more often in the negative reviews than in the positive reviews.

 In the specific case of this data, IMDB may want to highlight a select few of the positive and negative reviews for quick reference for a user when viewing a page for a particular movie. This model would do well at showing negative reviews, but not all of those selected as positive reviews will actually be positive.

 While we were content with the accuracy of the classification of the negative reviews, we would have liked to increase the positive classification accuracy. To attempt to increase the positive accuracy, we needed to create new dictionaries. This is very time consuming, so we only created 3 sets of dictionaries before deciding to settle on the third set. Given more time, we would create more dictionaries and try to limit the number of words in common between the two. This would theoretically provide a greater number of unique words in the positive and negative dictionary. Another method on the short list of ways to investigate impact on the model is removing more or different types of words, in addition to or in place of the first and third person verbs.

