import sys
import os
import glob
import time
import math
import operator

docs = {}
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
		tf[line[0]] = []
		for l in xrange(len(d)):
			tf[line[0]].append((d[l],fr[l]))

		for n in xrange(len(d)):
			if d[n] in doc_term_index:
				doc_terms[d[n]].append([line[0]])
			else:
				doc_terms[d[n]] = []
				doc_terms[d[n]].append([line[0]])


def calculate_R(query_id):
	doc_list = []
	for i in docs:
		if query in docs[i]:
			doc_list.append(i)
	return doc_list

def calculate_r(query,doc_list):
	for i in query:
		for j in doc_list:
			if i in doc_terms[j]:
				count += 1



def main():
	lines = []
	f = open('cacm.rel','r')
	for i in f:
		text = i.strip('\n')
		words = text.split()
		if words[2] in docs:
			docs[words[2]].append(words[3])
		else:
			docs[words[2]] = []
			docs[words[2]].append(words[3])

	for i in queries:
		output = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		query_words = words[1:]
		doc_list = calculate_R(query_id)
		calculate_r(query,doc_list)
		break

if __name__ == "__main__":
	get_tf_df()
	main()