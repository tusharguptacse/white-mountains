import sys
from bs4 import BeautifulSoup
import glob
import nltk
import os
import time


def get_text(filename):
	file = open(filename, 'r')
	source_code = file.read()
	soup = BeautifulSoup(source_code, "lxml")
	for text in soup.findAll('pre'):
		tokenize(text.text,filename)

def tokenize(data,filename):
	clean_tokens = []
	words = data.split()
	except_characters = ['!','.',':',',',';','}','{','^','*','=','|','[',']','#','@','&',')',\
	'(','-','?','/','`',"''",'``',"'",'%',' ','','$','<','>',"'s"]
	tk = nltk.word_tokenize(data)
	for word in tk:
		if word not in except_characters:
			word = word.replace("'",'')
			word = word.replace("''",'')
			clean_tokens.append(word)
	write_to_file(clean_tokens,filename)
	
def write_to_file(tk,filename):
	file = filename.split('/')
	fn = file[1].split('.html')[0]
	if not os.path.exists("Tokenized_Corpus"):
	    os.makedirs("Tokenized_Corpus")
	file = open('Tokenized_Corpus/%s.txt'%fn,'w')
	for i in tk:
		try:
			num = int(i)
			file.writelines(i.encode('utf-8').lower()+'\n')
		except:
			if '.' in i:
				wd = i.replace('.','')
				if wd != '':
					file.writelines(wd.encode('utf-8').lower()+'\n')
			elif ',' in i:
				wd = i.replace(',','')
				if wd != '':
					file.writelines(wd.encode('utf-8').lower()+'\n')
			else:
				file.writelines(i.encode('utf-8').lower()+'\n')


def main():
	start_time = time.time()
	i_n = 0
	i = 1
	for filename in glob.glob('cacm/*.html'):
		get_text(filename)
		i_n += 0.0312
		if i == 3204:
			i_n = 100
		sys.stdout.flush()
		sys.stdout.write("\r[%s%s] %d%% Completed" % ('=' * int(i_n), ' ' * (100 - int(i_n)), i_n))
		i += 1
	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))


if __name__ == "__main__":
	main()