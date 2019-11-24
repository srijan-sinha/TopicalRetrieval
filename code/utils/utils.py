import numpy as np
import pandas as pd
import math

stopwords = open('../code/stopwords.txt', 'r').readlines()
punctuation = open('../code/punctuation.txt', 'r').readlines()
stopwords = [i.strip() for i in stopwords]
punctuation = [i.strip() for i in punctuation]

def get_tokens (text, rem_whitespace=True, rem_stopwords=True, rem_punctuation=True):
	text = text.replace("\t", " ")
    text = text.replace("\n", " ")
    text = text.split()
    return [i for i in text if i not in stopwords and i not in punctuation and i not in vocab]