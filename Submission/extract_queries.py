import sys
from bs4 import BeautifulSoup, NavigableString
import glob
import nltk
import os
import time

queries = []

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

def get_text(filename):
	file = open(filename, 'r')
	source_code = file.read()
	soup = BeautifulSoup(source_code, "lxml")
	for text in soup.findAll('doc'):
		inner_text = [element for element in text if isinstance(element, NavigableString)]
		sentence = inner_text[1].strip('\n')
		words = sentence.split()
		query_words = clean_query(words)
		queries.append(query_words)
	write_to_file()
	
def write_to_file():
	file = open('queries.txt','w')
	i = 1
	for tup in queries:
		file.writelines(str(i))
		for q in tup:
			query = q.replace(' ','')
			file.writelines(' '+query)
		file.writelines('\n')
		i += 1


def main():
	start_time = time.time()
	get_text('cacm.query')
	print("\nTime Taken : %0.2f seconds" % (time.time() - start_time))


if __name__ == "__main__":
	main()