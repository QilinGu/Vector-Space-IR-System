Data:
	For each document, I combined "title" and "text" to a long string, and then did word tokenize using
"word_tokenize()" method from nltk, and used SnowBall stemmer for each token and English stop words corpus.  
	In my "vs_index.py" file, I first built two main dictionaries called "terms_tfs" and "terms_dfs" 
respectively. "terms_tfs" stores pairs of a term and a list of term frequencies for each document. For example, 
terms_tfs["hello"][1] will return a value of frequency of term "hello" for document 1.
"terms_dfs" stores pairs of term and corresponding document frequency. Then, I used these two dictionaries
to make shelves. 
	
Shelves:
	I made three shelves in total, which will take about 2 mins and 30 seconds. The first shelve is called 
"terms_dfs", I just converted my "terms_dfs" dictionary into shelve file. The second one is called 
"terms_weights", it is like a dictionary, in which each key is a term, and each corresponding value is other 
dictionary storing pairs of document id and weight of that term for this document. The third shelve is called 
"docs_lengths", it stores pairs of document id and corresponding document length. 

Packages:
	nltk, json, shelve, math, heapq, collections, operator.
	"heapq" is a python minimum heap which can store all the search results and sort the results automately.
	I used "Counter()" method in package of "collections" to count the frequency of each word in a list. 
	
Running instructions:
	For query search, when I put "god is good", it will appear 20 results which are related to "god" and "good",
and term "is" will be ignored, and no unknown search term. Click on each movie title, the full text
information will be shown or hiden by jQuery. The "Next" and "Last" buttons on the bottom of the page navigate
you to the next/last 10 results. 
	For "more like this" function, when you click the link under each movie information, you will see 30 
similar movies shown on other page.
