import sys
import os
import glob
import time
import math
import operator
import csv
import task4_BM25
from task4_BM25 import main,extract_data,second_run

alpha = 1.0
beta = 0.5
stopwords = []

def extract_stopwords():
	filename = open("common_words" , "r")
	for i in filename:
		stopwords.append(i.strip('\n'))

def get_query_vector(query):
	query_vector = {}
	for i in vocabulary:
		if i in query:
			query_vector[i] = calculate_query_tf(i,query)
		else:
			query_vector[i] = 0
	return query_vector

def calculate_query_tf(word,query):
	count = 0
	for i in query:
		if i == word:
			count += 1
	return count

def get_relevant_vector(docs):
	relevant_vector = {}
	for i,x in vocabulary.iteritems():
		for j in x:
			if j in docs:
				relevant_vector[i] = vocabulary[i][j]
			else:
				if i in relevant_vector:
					continue
				else:
					relevant_vector[i] = 0
	return relevant_vector

def get_non_relevant_vector(docs):
	nonrelevant_vector = {}
	for i,x in vocabulary.iteritems():
		for j in x:
			if j in docs:
				nonrelevant_vector[i] = vocabulary[i][j]
			else:
				if i in nonrelevant_vector:
					continue
				else:
					nonrelevant_vector[i] = 0
	return nonrelevant_vector

def calculate_rocchio_feedback(query,rdocs,ndocs,query_words,query_id):
	rocchio = {}
	output = []
	new_query = ''
	for i in vocabulary:
		rocchio[i] = query[i] + (alpha * rdocs[i]) - (beta * ndocs[i])

	ranked_documents = sorted(rocchio.items(), key=operator.itemgetter(1), reverse=True)

	for add in xrange(10):
		query_words.append(ranked_documents[add][0])

	for j in query_words:
		new_query += ' '+j

	result = second_run(query_words,query_id,relevant_documents)
	task2_file = open('task4_result.csv','a')
	writer = csv.writer(task2_file)
	if query_id == '1':
		writer.writerow(["Query_Id", "Literal", "Doc_Id",'Rank','Score','System Name'])
	for y,z in enumerate(result):
			if y < 100 and z[1] != 0:
				output.append([query_id,'Q0',z[0],y+1,z[1],'BM25'])
	for row in output:
		writer.writerow(row)

if __name__ == "__main__":
	start_time = time.time()
	extract_data()
	extract_stopwords()
	global vocabulary
	vocabulary = task4_BM25.tf
	queries = open('queries.txt','r')
	for i in queries:
		query_words = []
		global relevant_documents
		top_documents = []
		relevant_documents = []
		non_relevant_documents = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		for j in words[1:]:
			if j not in stopwords:
				query_words.append(j)
		result = main(query_words,query_id)
		for docs in result:
			top_documents.append(docs[0])
		for i in task4_BM25.doc_term_index:
			if i in top_documents:
				relevant_documents.append(i)
			else:
				non_relevant_documents.append(i)
		query_vector = get_query_vector(query_words)
		relevant_vector = get_relevant_vector(relevant_documents)
		nonrelevant_vector = get_non_relevant_vector(non_relevant_documents)
		calculate_rocchio_feedback(query_vector,relevant_vector,nonrelevant_vector,query_words,query_id)

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))