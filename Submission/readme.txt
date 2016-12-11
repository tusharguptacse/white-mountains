********************************************************************
                           P R O J E C T
********************************************************************
Name: Information Retrieval Project
Author: Aly Akhtar 	 <akhtar.a@husky.neu.edu>
		Lalit Pathak <pathak.l@husky.neu.edu>
		Tushar Gupta <gupta.t@husky.neu.edu>
Python: 2.7
Java : 1.8.0_112
********************************************************************

NOTE: The scripts use UNIX based path system ('/'), therefore will 
work only on UNIX based OS (MacOS/Ubuntu).

Third party Libraries: 

- Beautiful Soup 4 [https://www.crummy.com/software/BeautifulSoup/]
- requests 		   [http://docs.python-requests.org/en/master/]
- NLTK             [http://www.nltk.org]
- CSV			   [https://docs.python.org/3/library/csv.html]

      
DESCRIPTION:

Tokenizer.py is used for tokenizing the CACM corpus.

indexer.py is used to create inverted index

extract_queries.py is used to extract queries and writes it into
queries.txt

Task - 1: 
This task runs the task1_BM25.py, task1_VSCS.py, task1_TFIDF.py and 
task1_lucene.java.

This task implements the lucene library. The indexing and the searching 
is done in both in the task1.java fle. The file is provided with the 
tokenized corpus location and the location for the queries file. The 
output of the first 100 results are then given out.
Similarly 100 results are stored in files for the rest of the 3 approches.

Task-2:
The Task2_pseudo_relebvance.py is used to run this task. The retrieval model used in this is BM25 which runs automatically in the background.

Task-3:
In this task first the stemmed corpus is used to creat a new stemmed inverted
index and then an inverted index is created after stopping.
The BM25 model is run on both and the results are written.
task3_indexing_stemmedpy and task3_indexing_stopped.py are used for the 
indexes and task3_stemming and task3_stopping to get the results.

Task-4:
In this task the query expansion is combined with stopping, the file used for this is task4_expansion.py and task4_BM25.py runs automatically in the background for this.

task4_precision_recall is used to get the results for precision and recall.

Bonus:
This task is run by bonus.py. It takes in the tokenized corpus, for generating snipet
and returns the result in bonus_result.txt.


********************************************************************
INSTALLATION:

* Python 2.7

- Mac OS :
https://www.python.org/ftp/python/2.7.12/python-2.7.12-macosx10.6.pkg
- Windows 64
https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi

* Libraries:

- install using 'pip' command directly -
	* pip install requests
	* pip install beautifulsoup4
	* pip install nltk
	* pip install csv

download files for nltk:
run python in shell and then use -
nltk.download('punkt')
nltk.downlaod('averaged_perceptron_tagger')

********************************************************************
RUN:

Task1:
	python task1_BM25.py or task1_VSCS.py or task1_TFIDF.py
	or
	javac task1_LUCENE.java
	java task1_LUCENE

Task2:
	python task2_pseudo_relevance.py

Task3:
	python task3_indexing_stemmed.py or
	python task3_inddxing_stopped.py or
	python task3_stemming.py or
	python task3_stopping.py

Task4:
	python task4_expansion.py

	or

	python task4_precison_recall.py 1/2/3/4/5/6/7


	1 - BM25
	2 - TFIDF
	3 - VSCS
	4 - LUCENE
	5 - QUERY EXPANSION
	6 - STOPPING
	7 - EXPANSIN + STOPPPING

	NOTE: change file names in task4_precision_recall.py for correct 
	result files.

Bonus:
	python bonus.py

***********************************************************************