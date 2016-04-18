import nltk
import json
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import shelve
import math

#open and read a json file into "data"
with open('2015_movies.json') as data_file:
    data = json.load(data_file)

#build a stemmer
stemmer = SnowballStemmer("english", ignore_stopwords=True)
#build a stop words corpus
stop_words = set(stopwords.words("english"))

#build dictionaries
terms_tfs = {}#each key is a term, each value is a list of term frequencies
terms_dfs = {}#each key is a term, each value is document frequency
terms_weights = {}#each key is a term, each value is a other dictionary of document id and term weight
doc_weights = {}#each key is a doc id, each value is a list of weights for this doc.
docs_lengths = {}#each key is a doc id, each value is doc length.


for key, value in data.iteritems():#key is movie id, value is all information of a movie
    long_string = str(value['title']) + " " + str(value['text'].strip())
    words = word_tokenize(str(long_string))#tokenize the words in title and text fields
    for word in words:
        word = str(stemmer.stem(word))
        if word not in stop_words:
            if word not in terms_tfs and word not in terms_dfs:
                terms_dfs[word] = 0
                terms_tfs[word] = [0]*2342#because we have 1~2341 of movie. For example, terms_tfs[word][1] means the term "word" frequency in document 1
            terms_tfs[word][int(key)] = terms_tfs.get(word)[int(key)] + 1

#build docs_lengths dictionary
for term, list in terms_tfs.iteritems():
    sum = 0
    for tf in list:
        if tf != 0:
            sum = sum + 1
    terms_dfs[term] = sum

#documents as vectors
#use both dictionaries of "terms_tfs" and "terms_dfs" we just created to make "doc_weights" dictionary
#Each document will be represented as a real-valued vector of tf-idf weights.
for i in range(1, 2342):#the range of movie id is 1 to 2341.
    weights_list = []
    for term in terms_tfs:#only access keys
        if terms_tfs.get(term)[i] != 0:
            weight = (1+math.log10(terms_tfs.get(term)[i]))*math.log10(2341/terms_dfs.get(term))
        else:
            weight = 0
        weights_list.append(weight)
    doc_weights[i] = weights_list

#calculate length of each document
for doc_id, list in doc_weights.iteritems():
    sum = 0
    for weight in list:
        sum = sum + math.pow(weight, 2)
    length = math.sqrt(sum)
    docs_lengths[doc_id] = length

#terms as vectors
#use both dictionaries of "terms_tfs" and "terms_dfs" we just created to make "terms_weights" dictionary
#Each term will be represented as a real-valued vector of tf-idf weights.
for term, tf_list in terms_tfs.iteritems():
    docid_weight = {}
    id = -1
    for tf in tf_list:
        id = id + 1
        if tf >= 1:
            weight = (1+math.log10(tf))*math.log10(2341/terms_dfs.get(term))
            docid_weight[id] = weight
    terms_weights[term] = docid_weight

#store terms_dfs data into a shelf
myShelvedDict = shelve.open('terms_dfs')
try:
    for term in terms_dfs:
        myShelvedDict[term] = terms_dfs.get(term)
finally:
    myShelvedDict.close()

#store terms_weights data into a shelf
myShelvedDict = shelve.open('terms_weights')
try:
    for term in terms_weights:
        myShelvedDict[term] = terms_weights.get(term)
finally:
    myShelvedDict.close()

#store docs_lengths data into a shelf
myShelvedDict = shelve.open('docs_lengths')
try:
    for id in docs_lengths:
        myShelvedDict[str(id)] = docs_lengths.get(id)
finally:
    myShelvedDict.close()
