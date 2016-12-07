from math import log
from operator import itemgetter
from itertools import groupby
import sys


b = 0.75
k1 = 1.2
k2 = 100
R = 0.0            

index = {}
doID_termfreq_mapping = {}  
avdl = 0 

# Functions:

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


def extract_inverted_files(index_file):
    f = open(index_file)
    global index
    index = eval(f.read())


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
    extract_inverted_files(sys.argv[1])
    queries = input_query(sys.argv[2])    
    result_list = bm25_for_queries(queries)      
    query_id = 1
    for each in result_list:

        sorted_result_list = sorted(each.items(),key = itemgetter(1),reverse = True)
        rank = 1
        for each_list in sorted_result_list[:int(sys.argv[3])]:
            print 'query_id:', query_id, 'Q0: Q0', "doc_id:", each_list[0], "rank:", rank, "BM25_score:", each_list[1],\
                "system_name:", "BM25"
            rank += 1
        query_id += 1

if __name__=='__main__':
    main()