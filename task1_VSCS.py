import sys
import os
import glob
import time
import math
import operator
from tabulate import tabulate
import csv

df = {}
idf = {} 
tf_idf = {}
tf = {}
term_docs = {}
doc_terms = {}
N = 3204
doc_term_index = {}
doc_length = {}

def get_tf_df():
	f = open('Inverted_Index.txt','r')
	for i in f:
		fr = []
		d = []
		data = ''
		line = i.split(' -> ')
		for j in line[1]:
			if j not in ('(',')',' ','\n'):
				data += j
		docs = data.split(',')
		for k in xrange(len(docs)):
			if k % 2 == 0:
				d.append(docs[k]+'.txt')
			else:
				fr.append(int(docs[k]))
		df[line[0]] = len(d)
		tf[line[0]] = {}
		term_docs[line[0]] = []
		for l in xrange(len(d)):
			tf[line[0]][d[l]] = fr[l]
			term_docs[line[0]].append(d[l])
		for m in xrange(len(d)):
			if d[m] in doc_terms:
				doc_terms[d[m]] += float(fr[m])
			else:
				doc_terms[d[m]] = {}
				doc_terms[d[m]] = 1.0
		for n in xrange(len(d)):
			if d[n] in doc_term_index:
				doc_term_index[d[n]][line[0]] = fr[n]
			else:
				doc_term_index[d[n]] = {}
				doc_term_index[d[n]][line[0]] = fr[n]

def get_term_idf():
	term_idf = {}
	for term in df:
		if df[term] > 0:
			idf[term] = 1.0 + math.log(N/float(df[term]))
		else:
			idf[term] = 1.0


def get_tf_idf():
	for token,docs in tf.iteritems():
		for i in docs:
			tfidf = (float(docs[i])/doc_terms[i]) * idf[token]
			if token in tf_idf:
				tf_idf[token][i] = tfidf
			else:
				tf_idf[token] = {}
				tf_idf[token][i] = tfidf

def get_all_doc_length():
	for i,x in doc_term_index.iteritems():
		length = 0.0
		for j in x:
			length += math.pow(tf_idf[j][i],2)
		doc_length[i] = math.sqrt(length)


def get_query_tf_idf():
	query_tf_idf = {}
	for token in tf:
		if token in query_words:
			t_f = 1/float(len(query_words))
			tf_idf = t_f * idf[token]
			if token in query_tf_idf:
				query_tf_idf[token] += tf_idf
			else:
				query_tf_idf[token] = tf_idf		
		else:
			query_tf_idf[token] = 0.0
	return query_tf_idf

def get_query_length(val):
	length = 0.0
	for i in val:
		length += math.pow(val[i],2)
	return math.sqrt(length)

def cosine_similarity(ql,qtfidf):
	VSCS = {}
	for i,x in doc_term_index.iteritems():
		numerator = 0.0
		denominator = 0.0
		for token in x:
			numerator += tf_idf[token][i] * qtfidf[token]

		denominator = doc_length[i] * ql
		VSCS[i] = numerator/denominator
	return VSCS

		 
def main():
	start_time = time.time()
	get_tf_df()
	get_term_idf()
	get_tf_idf()
	get_all_doc_length()
	global query_words
	queries = open('queries.txt','r')
	task1_file = open('task1_query_result_VSCS.csv','a')
	writer = csv.writer(task1_file)
	writer.writerow(["Query_Id", "Literal", "Doc_Id",'Rank','Score','System Name'])
	for i in queries:
		output = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		query_words = words[1:]
		val = get_query_tf_idf()
		query_length = get_query_length(val)
		VSCS = cosine_similarity(query_length,val)
		ranked_documents = sorted(VSCS.items(), key=operator.itemgetter(1), reverse=True)
		for y,z in enumerate(ranked_documents):
			if y < 100 and z[1] != 0:
				output.append([query_id,'Q0',z[0],y+1,z[1],'V.S.C.S.'])
		for row in output:
			writer.writerow(row)

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))

if __name__ == "__main__":
	main()