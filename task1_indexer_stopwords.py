import sys
import requests
import time
import os
import re
import glob
import operator

inverted_dict_unigram = {}

stopwords = []

def make_stopwords_list():
	filename = open("common_words" , "r")
	for i in filename:
		stopwords.append(i.strip('\n'))


def make_dict_unigram(file):
	filename = open(file,'r')
	current_file = []
	for i in filename:
		current_file.append(i.strip('\n'))
	name  = file.split('\\')
	docid = name[1].split('.')[0]

	for i in xrange(len(current_file)):
		token = current_file[i].strip('\n')
		if (token != '' or token != ' ') and token not in stopwords:
			if token in inverted_dict_unigram:
				a = inverted_dict_unigram[token]
				if docid in a:
					inverted_dict_unigram[token][docid] += 1
				else:
					inverted_dict_unigram[token][docid] = 1 
			else:
				inverted_dict_unigram[token] = {}
				inverted_dict_unigram[token][docid] = 1


if __name__ == "__main__":
	start_time = time.time()
	i_n = 0
	i = 1
	make_stopwords_list()
	for filename in glob.glob('Tokenized_Corpus/*.txt'):
		make_dict_unigram(filename)
		i_n += 0.0312
		if i == 3204:
			i_n = 100
		sys.stdout.flush()
		sys.stdout.write("\r[%s%s] %d%% Completed" % ('=' * int(i_n), ' ' * (100 - int(i_n)), i_n))
		i += 1

	print '\n MAKING INVERTED INDEX...'

	sorted_keys = sorted(inverted_dict_unigram.items(), key=operator.itemgetter(0), reverse=False)

	mydict1 = open('Inverted_Index_Stopped.txt','w')
	for i in sorted_keys:
		sorted_doc = sorted(i[1].items(), key=operator.itemgetter(0), reverse=False)
		mydict1.writelines(i[0]+' -> ')
		for j in xrange(len(sorted_doc)):
			if j == len(sorted_doc) - 1:
				mydict1.writelines('('+sorted_doc[j][0]+','+str(sorted_doc[j][1])+')')
			else:
				mydict1.writelines('('+sorted_doc[j][0]+','+str(sorted_doc[j][1])+'),')
		mydict1.writelines('\n')

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))