#!/usr/bin/env python
# coding: utf-8

import smart_open
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', action="store", dest="full_corpus", help="full corpus file")
parser.add_argument('-m', action="store", dest="map_file", help="map file")

results = parser.parse_args()
full_corpus = results.full_corpus
map_file = results.map_file

tagdic = {}
with smart_open.open(full_corpus, encoding="iso-8859-1") as f:
    for i, line in enumerate(f):
        linarr = line.split('\t')
        mytag = linarr[0]
        tagdic[i] = mytag

file_out = open(map_file, "wb")
pickle.dump(tagdic, file_out)
file_out.close()
