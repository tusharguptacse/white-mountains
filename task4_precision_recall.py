import sys
import os
import glob
import time
import math
import operator
import csv

docs = {}
results = []
PatK = {}
count = 0

def get_relevant_document_data():
	lines = []
	f = open('cacm.rel','r')
	for i in f:
		text = i.strip('\n')
		words = text.split()
		if len(words[2]) == 8:
			word = words[2][:5] + '0' + words[2][5:]
		elif len(words[2]) == 7:
			word = words[2][:5] + '00' + words[2][5:]
		else:
			word = words[2]

		if word in docs:
			docs[word].append(words[0])
		else:
			docs[word] = []
			docs[word].append(words[0])

def get_query_results():
	file = open(filename,'r')
	reader = csv.reader(file)
	for i,row in enumerate(reader):
		if i != 0:
			results.append([row[2],row[0]])

def calculate_rdocs_for_query(query_id):
	rdocs = []
	for i in docs:
		if str(query_id) in docs[i]:
			rdocs.append(i)
	return len(rdocs)

def write_to_file(precision,recall,query_id):
	file = open(filename,'r')
	task4_file = open('task4_result_BM25.csv','a')
	reader = csv.reader(file)
	writer = csv.writer(task4_file)
	if query_id == 1:
		writer.writerow(["Query_Id", "Literal", "Doc_Id",'Rank','Score','System Name','Recall','Precision'])
	for i,row in enumerate(reader):
		if i != 0:
			new_row = []
			if row[0] == str(query_id):
				new_row.append(row[0])
				new_row.append(row[1])
				new_row.append(row[2])
				new_row.append(row[3])
				new_row.append(row[4])
				new_row.append(row[5])
				new_row.append(recall[row[2]])
				new_row.append(precision[row[2]])
				writer.writerow(new_row)

def calculate_precision_recall(query_id):
	precision = {}
	recall = {}
	global count
	global avg
	global total_RR
	flag1 = 0.0
	flag2 = 0.0
	flag3 = 0
	files = 0.0
	r = 0.0
	p = 0.0
	MAP = 0.0
	RR = 0.0
	Pat5 = 0.0
	Pat20 = 0.0
	total_p = 0.0
	N = calculate_rdocs_for_query(query_id)
	for i,x in enumerate(results):
		if x[1]  == str(query_id):
			files += 1.0
			if x[0] in docs and x[1] in docs[x[0]]:
				flag1 += 1.0
				if flag1 == 1.0:
					RR = 1.0/files
				r = flag1 / N
				p = flag1 / files
				total_p += p
			else:
				p = flag1/files
			if files == 5:
				Pat5 = p
			if files == 20:
				Pat20 = p
			precision[x[0]] = p
			recall[x[0]] = r
			flag3 = 1

	if N != 0 and flag3 == 1:
		count += 1
		total_RR += RR
		avg += total_p/N
		PatK[query_id] = [Pat5,Pat20]
		write_to_file(precision,recall,query_id)
	
def main():
	start_time = time.time()
	global avg
	global total_RR
	global filename
	avg = 0.0
	total_RR = 0.0
	filename = 'task1_query_result_BM25.csv'
	get_relevant_document_data()
	get_query_results()
	for i in xrange(1,65):
		calculate_precision_recall(i)
	task4_file = open('task4_result_BM25.csv','a')
	writer = csv.writer(task4_file)
	writer.writerow(['Mean Average Precision',avg/count])
	writer.writerow(['Mean Rank Reciprocal',total_RR/count])
	writer.writerow(['Query_Id','P@5','P@20'])
	for j in xrange(1,65):
		if j in PatK:
			writer.writerow([j,PatK[j][0],PatK[j][1]])

	print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))
		
if __name__ == "__main__":
	main()