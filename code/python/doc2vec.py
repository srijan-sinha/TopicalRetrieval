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
import sys

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# usage
# python doc2vec.py dimensions epochs

dimensions=int(sys.argv[1])
epochs = int(sys.argv[2])


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
tagdic = {}
def read_corpus_mine(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            linarr = line.split('\t')
            mytag = linarr[0]
            tagdic[mytag] = i
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

# %%time
# train_corpus = list(read_corpus_mine('../../data/trainall.txt'))

# traincorpusfile = open("../../data/traincorpus.pkl", "wb")
# pickle.dump(train_corpus, traincorpusfile)
# traincorpusfile.close()

f = open('../../data/pickle/traincorpus.pkl','rb')
train_corpus = pickle.load(f)
f.close()

# realtagdic ={}
# for key, value in tagdic.items():
#     realtagdic[value] = key
# print(len(realtagdic))

# tagdicfile = open("../../data/trainTagsToIndex.pkl", "wb")
# pickle.dump(realtagdic, tagdicfile)
# tagdicfile.close()

model = gensim.models.doc2vec.Doc2Vec(vector_size=dimensions, min_count=2, epochs=epochs)

# %%time
starttime = time.time()
model.build_vocab(train_corpus)
endtime = time.time()
print("Vocab build in ", str(endtime - starttime))

# %%time
starttime = time.time()
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
endtime = time.time()
print("Model train in ", str(endtime - starttime))

embeddingmodelfile = open("../../data/model_embeddings/modelembedding" +str(dimensions)+"_"+str(epochs)+".pkl", "wb")
pickle.dump(model, embeddingmodelfile)
embeddingmodelfile.close()

