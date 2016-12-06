import sys
import os
import glob
import time
import math
import operator
from tabulate import tabulate


df = {}
VSCS = {}
tf_all = {}
term_docs = {}

def get_all_tf_df():
	f = open('Inverted_Index.txt','r')
	for i in f:
		fr = []
		d = []
		data = ''
		line = i.split('->')
		for j in line[1]:
			if j not in ('(',')',' ','\n'):
				data += j
		docs = data.split(',')
		for k in xrange(len(docs)-1):
			if k % 2 == 0:
				d.append(docs[k]+'.txt')
			else:
				fr.append(int(docs[k]))
		df[line[0]] = len(d)
		tf_all[line[0]] = {}
		term_docs[line[0]] = []
		for l in xrange(len(d)):
			tf_all[line[0]][d[l]] = fr[l]
			term_docs[line[0]].append(d[l])


def get_doc_list():
	doc_list = []
	for i in query_words:
		if i in term_docs:
			for j in term_docs[i]:
				if j not in doc_list:
					doc_list.append(j)
	return doc_list


def vector_space_cosine_similarity(file):
	dc_fr = {}
	docid = file
	dot_product = 0.0
	query = 0.0
	document = 0.0 
	cosine_similarity = 0.0

	tm_fr = get_tf(file)
	tm_idf = get_term_idf()
	document_tf_idf = get_document_tf_idf(tm_fr, tm_idf)
	query_tf = get_tf_for_query()
	query_tf_idf = get_query_tf_idf(query_tf,tm_idf)
	doc_tf_idf = get_all_doc_tf_idf(file)


	for i in query_words:
		dot_product += query_tf_idf[i] * document_tf_idf[i]
		query += math.pow(query_tf_idf[i],2)
	for j in doc_tf_idf:
		document += math.pow(doc_tf_idf[j],2)

	denominator = math.sqrt(query * document)
	numerator = dot_product

	if denominator == 0:
		VSCS[docid] = 0
	else:
		cosine_similarity = numerator / denominator
		VSCS[docid] = cosine_similarity

def get_tf(file):
	tf = {}
	docid = file
	global count
	count = 0.0
	for v,x in tf_all.iteritems():
		for y in x:
			if y == docid:
				count += x[y]

	for i in query_words:
		if i in tf_all and docid in tf_all[i]:
			tf[i] = tf_all[i][docid]
		else:
			tf[i] = 0

	for ntf in tf:
		tf[ntf] = float(tf[ntf])/count
	return tf


def get_term_idf():
	term_idf = {}

	for term in query_words:
		if df[term] > 0:
			term_idf[term] = 1 + math.log(1000/float(df[term]))
		else:
			term_idf[term] = 1

	return term_idf

def get_document_tf_idf(tm_fr, tm_idf):
	doc_tf_idf = {}

	for term in query_words:
		doc_tf_idf[term] = tm_fr[term] * tm_idf[term]

	return doc_tf_idf

def get_tf_for_query():
	new_tf = {}

	for term in query_words:
		if term in new_tf:
			new_tf[term] += 1/float(len(query_words))
		else:
			new_tf[term] = 1/float(len(query_words))

	return new_tf

def get_query_tf_idf(query_tf,term_idf):
	new_tf_idf = {}

	for term in query_words:
		new_tf_idf[term] = query_tf[term] * term_idf[term]

	return new_tf_idf

def get_all_doc_tf_idf(file):
	doc_term = {}
	file_tf = {}
	file_df = {}
	file_idf = {}
	file_tf_idf = {}

	for i in tf_all:
		if file in tf_all[i]:
			file_tf[i] = float(tf_all[i][file])/count

	for j in file_tf:
		file_df[j] = len(term_docs[j])

	for term in file_df:
		if file_df[term] > 0:
			file_idf[term] = 1 + math.log(1000/float(file_df[term]))
		else:
			file_idf[term] = 1

	for k in file_tf:
		file_tf_idf[k] = file_tf[k] * file_idf[k]

	return file_tf_idf

if __name__ == '__main__':
	start_time = time.time()
	global query_words
	get_all_tf_df()
	queries = open('queries.txt','r')
	task2_file = open('task2_queries3.txt','a')
	for i in queries:
		VSCS = {}
		output = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		query_words = words[1:]
		docs = get_doc_list()
		for d in docs:
			vector_space_cosine_similarity(d)
		ranked_documents = sorted(VSCS.items(), key=operator.itemgetter(1), reverse=True)
		for y,z in enumerate(ranked_documents):
			if y < 100 and z[1] != 0:
				output.append([query_id,'Q0',z[0],y+1,z[1],'V.S.C.S.'])
		headers = ['Query_Id','Literal','Doc_Id','Rank','Score','System Name']
		task2_file.writelines('Query: '+sentence[2:]+'\n')
		task2_file.write(tabulate(output,headers,tablefmt="grid"))
		task2_file.writelines('\n\n')

	print("\nTime Taken : %0.2f seconds" % (time.time() - start_time))