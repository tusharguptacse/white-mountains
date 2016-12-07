import sys
import os
import glob
import time
import math
import operator
from tabulate import tabulate
import task2_VSCS
from task2_VSCS import main,extract_data

alpha = 1.0
beta = 0.5

def get_query_vector(query):
	query_vector = {}
	for i in vocabulary:
		if i in query:
			if i in query_vector:
				query_vector[i] += 1
			else:
				query_vector[i] = 1
		else:
			query_vector[i] = 0
	return query_vector

def get_relevant_vector(docs):
	relevant_vector = {}
	for i,x in vocabulary.iteritems():
		for j in x:
			if j in docs:
				if j in relevant_vector:
					relevant_vector[i] += 1
				else:
					relevant_vector[i] = 1
			else:
				relevant_vector[i] = 0
	return relevant_vector

def get_non_relevant_vector(docs):
	nonrelevant_vector = {}
	for i,x in vocabulary.iteritems():
		for j in x:
			if j in docs:
				if j in nonrelevant_vector:
					nonrelevant_vector[i] += 1
				else:
					nonrelevant_vector[i] = 1
			else:
				nonrelevant_vector[i] = 0
	return nonrelevant_vector

def calculate_rocchio_feedback(query,rdocs,ndocs,query_words):
	rocchio = {}
	output = []
	new_query = ''
	for i in vocabulary:
		rocchio[i] = query[i] + (alpha * rdocs[i]) - (beta * ndocs[i])

	ranked_documents = sorted(rocchio.items(), key=operator.itemgetter(1), reverse=True)
	
	query_words.append(ranked_documents[0][0])
	query_words.append(ranked_documents[1][0])

	for j in query_words:
		new_query += ' '+j

	result = main(query_words,1)
	task2_file = open('task2_result_after_expansion.txt','a')
	for y,z in enumerate(result):
			if y < 100 and z[1] != 0:
				output.append([query_id,'Q0',z[0],y+1,z[1],'V.S.C.S.'])
	headers = ['Query_Id','Literal','Doc_Id','Rank','Score','System Name']
	task2_file.writelines('Query: '+new_query+'\n')
	task2_file.write(tabulate(output,headers,tablefmt="grid"))
	task2_file.writelines('\n\n')

if __name__ == "__main__":
	start_time = time.time()
	extract_data()
	global vocabulary
	vocabulary = task2_VSCS.tf
	queries = open('queries.txt','r')
	for i in queries:
		top_documents = []
		relevant_documents = []
		non_relevant_documents = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		query_words = words[1:]
		result = main(query_words,0)
		for docs in result:
			top_documents.append(docs[0])
		for i in task2_VSCS.doc_length:
			if i in top_documents:
				relevant_documents.append(i)
			else:
				non_relevant_documents.append(i)
		query_vector = get_query_vector(query_words)
		relevant_vector = get_relevant_vector(relevant_documents)
		nonrelevant_vector = get_non_relevant_vector(non_relevant_documents)
		calculate_rocchio_feedback(query_vector,relevant_vector,nonrelevant_vector,query_words)

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))