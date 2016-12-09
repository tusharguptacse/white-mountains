import sys
from bs4 import BeautifulSoup
import glob
import nltk
import os
import time
import csv

output = []

f = open('luceneResults.txt','r')
f2 = open('task1_query_result_LUCENE.csv','w')
for i in f :
	a = i.strip('\n')
	b = a.split()
	output.append([b[0],b[1],b[2],b[3],b[4],b[5]])
writer = csv.writer(f2)
writer.writerow(["Query_Id", "Literal", "Doc_Id",'Rank','Score','System Name'])
for row in output:
		writer.writerow(row)
