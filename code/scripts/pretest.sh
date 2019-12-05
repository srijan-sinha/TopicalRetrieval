export GREEN="\e[0;33m"
export NC="\e[0;m"

mkdir -p ./data/pickle/ ./data/embeddings/

echo -e "${GREEN}==================================================Building Index===============================================${NC}"
python ./python/build_index.py -s stopwords.txt -p punctuation.txt -c ./data/trec_data/train.txt -i ./data/pickle/inverted_index.pkl -d ./data/pickle/doc_length.pkl

echo -e "${GREEN}==================================================Running Doc2Vec==============================================${NC}"
echo "==============================================Dimension = 400=========================================="
python ./python/doc2vec.py -d 400 -e 4 -c ./data/pickle/train_corpus.pkl -f ./data/trec_data/train.txt -m ./data/embeddings/model
echo "==============================================Dimension = 200=========================================="
python ./python/doc2vec.py -d 200 -e 4 -l -c ./data/pickle/train_corpus.pkl -f ./data/trec_data/train.txt -m ./data/embeddings/model
echo "==============================================Dimension = 100=========================================="
python ./python/doc2vec.py -d 100 -e 4 -l -c ./data/pickle/train_corpus.pkl -f ./data/trec_data/train.txt -m ./data/embeddings/model
echo "==============================================Dimension = 60==========================================="
python ./python/doc2vec.py -d 60 -e 4 -l -c ./data/pickle/train_corpus.pkl -f ./data/trec_data/train.txt -m ./data/embeddings/model
echo "==============================================Dimension = 16==========================================="
python ./python/doc2vec.py -d 16 -e 4 -l -c ./data/pickle/train_corpus.pkl -f ./data/trec_data/train.txt -m ./data/embeddings/model
