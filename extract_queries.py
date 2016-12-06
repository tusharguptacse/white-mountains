import sys
from bs4 import BeautifulSoup, NavigableString
import glob
import nltk
import os
import time

queries = []

def get_text(filename):
	file = open(filename, 'r')
	source_code = file.read()
	soup = BeautifulSoup(source_code, "lxml")
	for text in soup.findAll('doc'):
		inner_text = [element for element in text if isinstance(element, NavigableString)]
		queries.append(inner_text[1])
	write_to_file()
	
def write_to_file():
	file = open('queries.txt','w')
	i = 1
	for q in queries:
		query = q.replace('\n',' ')
		file.writelines(str(i)+' '+query[4:]+'\n')
		i += 1


def main():
	start_time = time.time()
	get_text('cacm.query')
	print("\nTime Taken : %0.2f seconds" % (time.time() - start_time))


if __name__ == "__main__":
	main()