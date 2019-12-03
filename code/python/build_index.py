#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import math
import glob
import time
import pickle as pkl
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', action="store", dest="stopword_file", help="stopword file")
parser.add_argument('-p', action="store", dest="punctuation_file", help="punctuation file")
parser.add_argument('-c', action="store", dest="corpus_file", help="full document corpus file")
parser.add_argument('-i', action="store", dest="inverted_index_file", help="inverted index pickle (output)")
parser.add_argument('-d', action="store", dest="doc_length_file", help="document length array pickle (output)")

results = parser.parse_args()
stopword_file = results.stopword_file
punctuation_file = results.punctuation_file
corpus_file = results.corpus_file
inverted_index_file = results.inverted_index_file
doc_length_file = results.doc_length_file

stopwords = open(stopword_file, 'r').readlines()
punctuation = open(punctuation, 'r').readlines()
stopwords = [i.strip() for i in stopwords]
punctuation = [i.strip() for i in punctuation]

def find_count(text_arr):
    dict = {}
    for i in text_arr:
        if (i not in stopwords and i not in punctuation):
            if (i in dict):
                dict[i] += 1
            else:
                dict[i] = 1
    return dict

def doc_len (dict):
    sum = 0
    for i in dict:
        sum += dict[i]
    return sum

start = time.time()
count_docs = 0
inverted_index = {}
doc_length = []
docs = open(corpus_file, 'r').readlines()

for j in docs:
    doc_name = j[:13]
    text = j[13:]
    text = text.replace("\t", " ")
    text = text.replace("\n", " ")
    text = text.split()
    text = find_count(text)
    for i in text:
        if (i not in inverted_index):
            inverted_index[i] = np.array([[count_docs,text[i]]])
        else:
            inverted_index[i] = np.concatenate((inverted_index[i], np.array([[count_docs, text[i]]])), axis=0)
    doc_length.append(doc_len(text))
    count_docs += 1
    if (count_docs%5000 == 0):
        print (count_docs), " docs done"

end = time.time()
print (end - start)
doc_length = np.array(doc_length)


f = open(inverted_index_file, 'wb')
pkl.dump(inverted_index, f)
f.close()
f = open(doc_length_file, 'wb')
pkl.dump(doc_length, f)
f.close()
