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

def clean_query(words):
	query = []
	except_characters = ['!','.',':',',',';','}','{','^','*','=','|','[',']','#','@','&',')',\
	'(','?','/','`',"''",'``',"'",'%',' ','','$','<','>','"']
	for word in words:
		new_word = ''
		if '-' in word:
			i = word.split('-')
			try:
				a = float(i[0])
				query.append(word)
			except:
				continue
		else:
			try: 
				a = float(word)
				query.append(word)
			except:
				for letter in word:
					if letter not in except_characters:
						new_word += letter
				query.append(new_word.lower())
	return query

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
	return relevant_vector

def calculate_rocchio_feedback(query,rdocs,ndocs):
	rocchio = {}
	for i in vocabulary:
		rocchio[i] = query[i] + (alpha * rdocs[i]) - (beta * ndocs[i])
	
	f = open('test.txt','w')
	for j in rocchio:
		f.writelines(j + ' -> ' + str(rocchio[j]) + '\n')

if __name__ == "__main__":
	start_time = time.time()
	extract_data()
	global vocabulary
	vocabulary = task2_VSCS.tf
	queries = open('queries.txt','r')
	for i in queries:
		relevant_documents = []
		non_relevant_documents = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		query_words = clean_query(words[1:])
		result = main(query_words)
		for i in task2_VSCS.doc_length:
			if i in result:
				relevant_documents.append(i)
			else:
				non_relevant_documents.append(i)
		query_vector = get_query_vector(query_words)
		relevant_vector = get_relevant_vector(relevant_documents)
		nonrelevant_vector = get_non_relevant_vector(non_relevant_documents)
		calculate_rocchio_feedback(query_vector,relevant_vector,nonrelevant_vector)
		break

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))