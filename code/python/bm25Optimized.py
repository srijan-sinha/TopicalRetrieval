#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import math
import time
import pickle as pkl
import gensim
import shutil
import glob
import os
import smart_open
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', action="store", dest="dimension", help="embedding dimension to be used for ranking", type=int)
parser.add_argument('-e', action="store", dest="epochs", help="embedding model training epochs", type=int)
parser.add_argument('-n', action="store", dest="top_n", help="candidate set filter size", type=int)
parser.add_argument('-m', action="store", dest="model_pre", help="embedding file path prefix")

results = parser.parse_args()
dimensionidentifier = results.dimension
topn = results.top_n
epochs = results.epochs
model_pre = results.model_pre

IV_file = './data/pickle/inverted_index.pkl'
TAGDICFILE = './data/pickle/trainTagsToIndex.pkl'
DOC_LENGTH_FILE = './data/pickle/doc_length.pkl'
QUERIES_FILE = './data/trec_data/queries.txt'
DOC2VECMODEL = model_pre + '_' + str(dimensions)+"D_"+str(epochs)+"E.pkl"
STOPWORD_FILE = './stopwords.txt'
PUNCTUATION_FILE = './punctuation.txt'
OUTPUT_FILE = './data/output/ranking_optimized_' + str(dimensionidentifier)+'_'+str(topn) + '.txt'

stopwords = open(STOPWORD_FILE, 'r').readlines()
punctuation = open(PUNCTUATION_FILE, 'r').readlines()
stopwords = [i.strip() for i in stopwords]
punctuation = [i.strip() for i in punctuation]

f = open(IV_file, 'rb')
inverted_index = pkl.load(f)
f.close()

f = open(DOC_LENGTH_FILE, 'rb')
documentLenArr = pkl.load(f)
f.close()

f = open(TAGDICFILE, 'rb')
tagDic = pkl.load(f)
f.close()

numdocuments = len(documentLenArr)
k1 = 1.5
b = 0.5
avgDoclength = sum(documentLenArr)*1.0/numdocuments
maxranking = 50

f = open(DOC2VECMODEL, 'rb')
doc2vecmodel = pkl.load(f)
f.close()

def read_corpus_query(fname):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            yield tokens
            
#usage sort_index(getScoreForQuery(find_count(query)))
def getScoreForQuery(queryMap):
    documentToScore = {}
    for term, termfreq in queryMap.items():
        if term in inverted_index:
            posting = inverted_index[term]
            weightOrIdf = calcIdf(len(posting))
            for docInfo in posting:
                doc_id = docInfo[0]
                doc_id_freq = docInfo[1]
                scoreTermDoc = getScoreForTermForDocument(termfreq,doc_id,weightOrIdf,doc_id_freq)
                if doc_id in documentToScore:
                    documentToScore[doc_id] = documentToScore[doc_id] + scoreTermDoc
                else:
                    documentToScore[doc_id] = scoreTermDoc
    return documentToScore

def getScoreForQueryOptimized(queryMap, qindex):
    documentToScore = {}
    thisdocset = docsets[qindex]
    for term, termfreq in queryMap.items():
        if term in inverted_index:
            posting = inverted_index[term]
            weightOrIdf = calcIdf(len(posting))
            for docInfo in posting:
                doc_id = docInfo[0]
                if doc_id not in thisdocset:
                    continue
                doc_id_freq = docInfo[1]
                scoreTermDoc = getScoreForTermForDocument(termfreq,doc_id,weightOrIdf,doc_id_freq)
                if doc_id in documentToScore:
                    documentToScore[doc_id] = documentToScore[doc_id] + scoreTermDoc
                else:
                    documentToScore[doc_id] = scoreTermDoc
    return documentToScore

def calcIdf(lenposting):
    ans = math.log((numdocuments*1.0 - lenposting +0.5)/(lenposting+0.5))
    return ans

def getScoreForTermForDocument(qfi,docNo,weight,tfi):
    docLength = documentLenArr[docNo]*1.0
    ans = weight* ((tfi*(k1+1)*1.0)/(tfi+k1*(1.0-b+b*(docLength/avgDoclength))))
    ans = ans*qfi
    return ans

def find_count(text_arr):
    dictionary = {}
    for i in text_arr:
        if (i not in stopwords and i not in punctuation):
            if (i in dictionary):
                dictionary[i] += 1
            else:
                dictionary[i] = 1
    return dictionary

def sort_index(documentToScore):
    ans = []
    numvaluesAdded=0
    while(numvaluesAdded<=maxranking and len(documentToScore)!=0):
        tempkey = max(documentToScore, key=documentToScore.get)
        ans.append((tempkey, documentToScore[tempkey]))
        numvaluesAdded +=1
        del documentToScore[tempkey]
    return ans

def tagToScore(documentToScore):
    ans = []
    for doc_id, score in documentToScore:
        ans.append((tagDic[doc_id], score))
    return ans;

starttime = time.time()

queries = open(QUERIES_FILE, 'r').readlines()
test_corpus = list(read_corpus_query(QUERIES_FILE))
docsets = []
for doc_id in range(len(test_corpus)):
    inferred_vector = doc2vecmodel.infer_vector(test_corpus[doc_id])
    sims = doc2vecmodel.docvecs.most_similar([inferred_vector], topn=topn)
    docsets.append(set([x for x,_ in sims]))
answersallOptimized = []
for x in range(len(queries)):
    answersallOptimized.append(sort_index(getScoreForQueryOptimized(find_count(queries[x].split(' ')),x)))

endtime = time.time()
strprint = str(dimensionidentifier)+ ","+str(topn) + "," + str(endtime-starttime)
print(strprint)

def writeOutput(answers, filename):
    ansstr = ""
    for i in range(len(answers)):
        thisanswer = answers[i]
        doctagToScore = tagToScore(thisanswer)
        for j in range(len(doctagToScore)):
            tempstr = str(i+51) + " 0 "+ doctagToScore[j][0] + " " + str(j+1)+" "+ str(doctagToScore[j][1])+ " p\n"
            ansstr += tempstr
    outfile = open(filename, "w")
    outfile.write(ansstr)
    outfile.close()
    
writeOutput(answersallOptimized, )
