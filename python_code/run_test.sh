# !/bin/bash

# DIM=('2' '4' '8' '16' '60' '100' '200' '400')
DIM=('2' '4' '8')
TOPN=('50' '100' '1000' '5000' '10000')

for i in 0 1 2
do
	for j in 0 1 2 3 4
	do
		python bm25Optimized.py ../../data/model_embeddings/modelembedding${DIM[$i]}_40.pkl ${DIM[$i]} ${TOPN[$j]}
	done
done
