#!/usr/bin/env python
# coding: utf-8

import shutil
import glob
import os
import gensim
from sklearn.metrics.pairwise import cosine_similarity as cosvec
import numpy as np
import pickle
import random
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import smart_open
import time
import argparse

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-d', action="store", dest="dimension", help="embedding dimension", type=int)
parser.add_argument('-e', action="store", dest="epochs", help="number of epochs to run", type=int)
parser.add_argument('-l', action="store_true", dest="load", help="if to load train corpus form pickle")
parser.add_argument('-c', action="store", dest="corpus_pickle_file", help="file to load/store corpus pickle")
parser.add_argument('-f', action="store", dest="full_corpus", help="file having full corpus data (only needed if not loading corpus pickle)")
parser.add_argument('-m', action="store", dest="model_pre", help="embedding model output file prefix (without .pkl)")

results = parser.parse_args()
dimension = results.dimension
epochs = results.epochs
load = results.load
corpus_pickle_file = results.corpus_pickle_file
full_corpus = results.full_corpus
model_pre = results.model_pre

def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            print(i,line)
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
myjoiner = " "
def read_corpus_mine(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            linarr = line.split('\t')
            mytag = linarr[0]
            line = myjoiner.join(linarr[1:])
            print(i)
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

def read_corpus_query(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            print(i,line)
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

if (load):
    f = open(corpus_pickle_file,'rb')
    train_corpus = pickle.load(f)
    f.close()
else:
    train_corpus = list(read_corpus_mine(full_corpus))

    traincorpusfile = open(corpus_pickle_file, "wb")
    pickle.dump(train_corpus, traincorpusfile)
    traincorpusfile.close()

model = gensim.models.doc2vec.Doc2Vec(vector_size=dimensions, min_count=2, epochs=epochs)

starttime = time.time()
model.build_vocab(train_corpus)
endtime = time.time()
print("Vocab build in ", str(endtime - starttime))

starttime = time.time()
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
endtime = time.time()
print("Model train in ", str(endtime - starttime))

embeddingmodelfile = open(model_pre + "_" + str(dimensions)+"D_"+str(epochs)+"E.pkl", "wb")
pickle.dump(model, embeddingmodelfile)
embeddingmodelfile.close()

