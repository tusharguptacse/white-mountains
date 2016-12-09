import sys
import time
import csv
import math
import operator

tf = {}
df = {}
term_docs = {}
doc_terms = {}
doc_term_index = {}
docs = {}
dl = {}
b = 0.75
k1 = 1.2
k2 = 100
N = 3204
k = {}
BM25 = {}

def get_tf_df():
    f = open('Inverted_Index_Stopped.txt','r')
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
                d.append(docs[k])
            else:
                fr.append(int(docs[k]))
        df[line[0]] = len(d)
        tf[line[0]] = {}
        term_docs[line[0]] = []
        for l in xrange(len(d)):
            tf[line[0]][d[l]] = fr[l]
            term_docs[line[0]].append(d[l])
        for m in xrange(len(d)):
            if d[m] in doc_terms:
                doc_terms[d[m]] += float(fr[m])
            else:
                doc_terms[d[m]] = {}
                doc_terms[d[m]] = 1.0
        for n in xrange(len(d)):
            if d[n] in doc_term_index:
                doc_term_index[d[n]][line[0]] = fr[n]
            else:
                doc_term_index[d[n]] = {}
                doc_term_index[d[n]][line[0]] = fr[n]

def extract_cacm_rel():
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

def get_dl_avdl():
    global avdl
    for i,x in doc_term_index.iteritems():
        count = 0
        for j in x:
            count += x[j]
        dl[i] = count
    count = 0
    for k in dl:
        count += dl[k]

    avdl = float(count)/float(len(dl))

def calculate_K():
    for i in dl:
        k[i] = k1*((1-b)+(b*(dl[i]/avdl)))

def calculate_R(query_id):
    doc_list = []
    for i in docs:
        if query_id in docs[i]:
            doc_list.append(i)
    return doc_list

def calculate_r(word,doc_list):
    count = 0
    for i in doc_list:
        if word in doc_term_index[i]:
            count += 1
    return count

def count_frq_terms(word):
    count = 0
    for i in query_words:
        if i == word:
            count += 1
    return count

def BM25_score(query_id,level,reldocs):
    if level == 0:
        R = calculate_R(query_id)
    else:
        R = reldocs
    for i in doc_term_index:
        score = 0.0
        K = k[i]
        for j in query_words:
            if j in tf:
                if i in tf[j]:
                    f = tf[j][i]
                else:
                    f = 0
            else:
                f = 0
            qf = count_frq_terms(j)
            r = calculate_r(j,R)
            if j in df:
                n = df[j]
            else:
                n = 0
            mul1 = ((k1+1)*f)/(K+f)
            mul2 = ((k2+1)*qf)/(k2+qf)
            exp = (((r+0.5)/(len(R)-r+0.5))/((n-r+0.5)/(N-n-len(R)+r+0.5)))
            if exp > 0:
                mul3 = math.log(exp)
            else:
                mul3 = 0
            score += (mul1 * mul2 * mul3)
        BM25[i] = score

def extract_data():
    get_tf_df()
    extract_cacm_rel()
    get_dl_avdl()
    calculate_K()

def second_run(query,query_id,docs):
    global query_words
    query_words = query
    BM25_score(query_id,1,docs)
    ranked_documents = sorted(BM25.items(), key=operator.itemgetter(1), reverse=True)
    return ranked_documents[:100]


def main(query,query_id):
    global query_words
    query_words = query
    BM25_score(query_id,0,[])
    ranked_documents = sorted(BM25.items(), key=operator.itemgetter(1), reverse=True)
    return ranked_documents[:10]
