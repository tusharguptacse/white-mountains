import sys
import requests
import time
import os
import re
import glob
import operator

file_content = {}
final_snippet = {}
def read_files():
	for filename in glob.glob('Tokenized_Corpus/*.txt'):
		name1 = filename.split('/')
		name2 = name1[1].split('.')[0]
		f = open(filename,'r')
		file_content[name2] = []
		for j in f:
			a = j.strip('\n')
			file_content[name2].append(a)

def get_words(list_of_words,query_term):
	index = 0
	string = ''

	index = list_of_words.index(query_term)
	
	if index > 2 and index < len(list_of_words)-2 :
		string = list_of_words[index-2]+' '+list_of_words[index-1]+' '+'<b>'+query_term+'</b>'+' '+list_of_words[index+1]+' '+list_of_words[index+2]
	elif index > 2 and index < len(list_of_words)-1 :
		string = list_of_words[index-2]+' '+list_of_words[index-1]+' '+'<b>'+query_term+'</b>'+' '+list_of_words[index+1]
	elif index > 2 and index < len(list_of_words) :
		string = list_of_words[index-2]+' '+list_of_words[index-1]+' '+'<b>'+query_term+'</b>'
	elif index == 1 :
		string = list_of_words[index-1]+' '+query_term+' '+'<b>'+query_term+'</b>'+' '+list_of_words[index+1]+' '+list_of_words[index+2]
	elif index == 0 :
		string = '<b>'+query_term+'</b>'+' '+list_of_words[index+1]+' '+list_of_words[index+2]
	return string



def generate_snippet():
	data = ''
	for i in file_content:
		snippet = ''
		for j in query_words:
			if j in file_content[i]:
				snippet += '...'+' '+get_words(file_content[i],j)
		snippet += ' '+'...'
		final_snippet[i] = snippet

	f = open('bonus_result.txt','a')
	for k in query_words:
		data += ' '+k
	f.writelines('Query: '+data+'\n')
	for l in final_snippet:
		if len(final_snippet[l]) > 0:
			f.writelines('Document Id: '+l+'\n')
			f.writelines(final_snippet[l]+'\n\n')


def main():
	start_time = time.time()
	read_files()
	global query_words
	queries = open('queries.txt','r')
	for i in queries:
		output = []
		sentence = i.strip('\n')
		words = sentence.split()
		query_id = words[0]
		query_words = words[1:]
		generate_snippet()

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))

if __name__ == "__main__":
	main()