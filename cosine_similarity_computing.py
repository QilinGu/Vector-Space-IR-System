from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import math
import shelve
import heapq
import json
import operator

#open and read a json file into "data"
with open('2015_movies.json') as data_file:
    data = json.load(data_file)

myShelved_term_df = shelve.open('terms_dfs')
myShelved_term_weights = shelve.open('terms_weights')
myShelved_docs_lengths = shelve.open('docs_lengths')

#build a stemmer
stemmer = SnowballStemmer("english", ignore_stopwords=True)
#build a stop words corpus
stop_words = set(stopwords.words("english"))


def search(query):
    ignore_words = []#store the words that are ignored
    query_words = []#the words to be calculated for query
    query_weights = []#the list of weights for in query
    unknown_search_words = []#the list of words that are not in the dictionary
    heap = []#a list represents a heap
    hits = 0#the number of hits
    words = word_tokenize(str(query))
    #calculate the valid query words
    for w in words:
        w = str(stemmer.stem(w))
        if w in stop_words:
            ignore_words.append(w)
        elif w not in myShelved_term_df.keys():
            unknown_search_words.append(w)
        else:
            query_words.append(w)
    #calculate query as a vector
    counts = Counter(query_words)#use Counter to count the frequency of each word in list
    for w in query_words:#only access keys
        query_weights.append((1+math.log10(counts[w]))*math.log10(2341/myShelved_term_df.get(w)))
    #calculate cosine similarities, and store the results into min-heap
    for doc_id in range(1, 2342):#[1,2341]
        weights_for_document = []
        has_both = True
        for w in set(query_words):
            if doc_id in myShelved_term_weights.get(w):
                weights_for_document.append(myShelved_term_weights.get(w)[doc_id])
            else:
                has_both = False
        if has_both:
            hits = hits + 1
            heapq.heappush(heap, {cosine_similarity(query_weights, weights_for_document, myShelved_docs_lengths.get(str(doc_id))) : str(doc_id) })#each node in heap is a hash
    #find and return top 30 in the heap
    return hits, heapq.nlargest(30, heap), ignore_words, unknown_search_words

def cosine_similarity(vector1, vector2, length_of_vector2):
    dot_product = 0.0
    cos = 0.0
    #calculate dot product
    for i in range(0,len(vector1)):
        dot_product = dot_product + (vector1[i] * vector2[i])
    #calculate cosine
    if length_of_vector2 == 0:
        cos = 0
    else:
        cos = dot_product/length_of_vector2
    return cos

def get_similar_docs(target_id):
    query_words = []#the words to be calculated for query
    query_weights = {}#this is a dictionary to store pairs of term and weight
    scores = {}#this dictionary stores pairs of document id and score
    long_string = str(data[target_id]['title']) + " " + str(data[target_id]['text'])
    words = word_tokenize(str(long_string))
    #calculate the valid query words
    for w in words:
        w = str(stemmer.stem(w))
        if w not in stop_words:
            query_words.append(w)
    #calculate query as a vector
    counts = Counter(query_words)#use Counter to count the frequency of each word in list
    for w in query_words:#only access keys
        query_weights[w] = (1+math.log10(counts[w]))*math.log10(2341/myShelved_term_df.get(w))
    #calculate and update score for each document, and return the documents with the highest score
    for term, qw in query_weights.iteritems():
        posting_list = myShelved_term_weights.get(term)
        for doc_id, weight in posting_list.iteritems():
            if str(doc_id) in scores:
                scores[str(doc_id)] = scores.get(str(doc_id)) + (qw * weight)/myShelved_docs_lengths.get(str(doc_id))
            else:
                scores[str(doc_id)] = (qw * weight)/myShelved_docs_lengths.get(str(doc_id))
    #sort the dictionary of scores by value from small to large
    sorted_socres = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_socres[0:30]
