import sys
import os
import time
from itertools import groupby


index = {}


def extract_from_input(input_file):
    
    f = open(input_file, 'r')

    input = f.read().split()
    doc_list = []           
    for k, g in groupby(input, lambda x: x == '#'):
        if not k:
            doc_list.append(list(g))
    for values in doc_list:
        doc_token_list = {}       
    for each_list in doc_list:
        token_list = []         
        for tokens in each_list[1:]:
            if not str.isdigit(tokens):
                token_list.append(tokens)
        doc_token_list['CACM-' + str(each_list[0])] = token_list
    return doc_token_list


# Function to compute the inverted index
def compute_index(doc_token_list):
    for k, val in doc_token_list.iteritems():
        word_frequency_pair = {}       
        for word in val:
            if word not in word_frequency_pair:
                word_frequency_pair[word] = 1
            else:
                word_frequency_pair[word] += 1

        for ky, values in word_frequency_pair.iteritems():
            index.setdefault(ky,[]).append((k,values,))



# Function to write the inverted index to output_file
# def write_index_to_file(indexed_file, final):
#     f = open(indexed_file, 'w')
#     for i in final:    
#         f.writelines(i + " -> " + str(final[i])[1:-1] + "\n")
#     f.close()

# Function to write the inverted index to output_file
def write_index_to_file(indexed_file, final):
    f = open(indexed_file, 'w')
    for i in final:    
        f.writelines(i + " -> ")
        l = 1
        for j in final[i]:
            if l == len(final[i]):
                f.writelines('(' + j[0] + ',' + str(j[1]) + ')')
            else:
                f.writelines('(' + j[0] + ',' + str(j[1]) + ')' + ',')
                l+=1
        f.writelines('\n')



# Main function
def main():
    doc_token_list = extract_from_input("cacm_stem.txt")
    compute_index(doc_token_list)
    write_index_to_file("Inverted_Index_Stemmed.txt", index)
    
if __name__== '__main__':
    start_time = time.time()
    print("\n\nTime Taken: %0.2f seconds" % (time.time() - start_time))
    main()
