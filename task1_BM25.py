from math import log
from operator import itemgetter
from itertools import groupby
import sys
import time
import csv


b = 0.75
k1 = 1.2
k2 = 100
R = 0.0            

index = {}
doID_termfreq_mapping = {}  
avdl = 0 


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

# Functions:
def extract_inverted_files():
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
        index[line[0]] = []
        for l in xrange(len(d)):
            index[line[0]].append((d[l],fr[l]))

        for n in xrange(len(d)):
            if d[n] in doc_term_index:
                doc_terms[d[n]].append([line[0]])
            else:
                doc_terms[d[n]] = []
                doc_terms[d[n]].append([line[0]])

def BM25_score(n,dl,f):
    r = 0       
    qf = 1       
    N = len(doID_termfreq_mapping)
    K = compute_K(dl, avdl) 
    mul1 = ((k1+1)*f)/(K+f)
    mul2 = ((k2+1)*qf)/(k2+qf)
    mul3 = log(((r+0.5)/(R-r+0.5))/((n-r+0.5)/(N-n-R+r+0.5)))
    return mul1*mul2*mul3

def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)) )

def calculate_avdl():
    sum = 0
    for key, values in index.items():
        for each in values:
            sum += int(each[1])
            if each[0] in doID_termfreq_mapping:
                doID_termfreq_mapping[each[0]].append(each[1])
            else:
                doID_termfreq_mapping[each[0]] = [each[1]]
    return float(sum)/float(len(doID_termfreq_mapping))

def input_query(query_file):
    f = open(query_file)
    lines = ''.join(f.readlines())
    query_list = [x.rstrip().split() for x in lines.split('\n')[:]]
    return query_list


# Function to implement BM25 Algorithm for query list
def bm25_for_queries(queries):
    global avdl
    avdl = calculate_avdl()
    results = []
    for query in queries:
        results.append(bm25_for_each_query(query))
    return results


def bm25_for_each_query(query):
    doc_to_score = {}                         # This dictionary contains the docid as key and it's score as values
    N = len(doID_termfreq_mapping)
    for each_word in query:
        if each_word in index.keys():
            word_val = index[each_word]       # Word_val is a list of tuples that contain the docid, freq for each word
            word_to_docid_n_freq = dict(word_val) # This dictionary contains the docid and frequency for the given word
            n = len(word_to_docid_n_freq)
            for docid,freq in word_to_docid_n_freq.items():
                score = BM25_score(n,calculate_dl(docid),freq)
                if docid not in doc_to_score:
                    doc_to_score[docid] = score
                else:
                    doc_to_score[docid] += score
    return doc_to_score

def calculate_dl(docid):
    dl = 0
    for each_tf in doID_termfreq_mapping[docid]:
        dl += each_tf
    return dl

# Main function
def main():
    start_time = time.time()
    extract_inverted_files()
    extract_cacm_rel()
    queries = input_query('queries.txt')    
    result_list = bm25_for_queries(queries) 
    del result_list[-1]
    query_id = 1
    task1_file = open('task1_query_result_BM25.txt','a')
    writer = csv.writer(task1_file)
    writer.writerow(["Query_Id", "Literal", "Doc_Id",'Rank','Score','System Name'])
    query_id = 1
    for each in result_list:
        output = []
        query = ''
        for i in queries[query_id-1][1:]:
            query += ' '+ i
        doc_list = calculate_R(query_id)
        calculate_r(new_query,doc_list)
        sorted_result_list = sorted(each.items(),key = itemgetter(1),reverse = True)
        rank = 1
        for each_list in sorted_result_list[:int(100)]:
            output.append([query_id,'Q0',each_list[0],rank,each_list[1]])
            rank += 1
        for row in output:
            writer.writerow(row)
        query_id += 1

    print("\n\nTime Taken : %0.2f seconds" % (time.time() - start_time))

if __name__=='__main__':
    main()