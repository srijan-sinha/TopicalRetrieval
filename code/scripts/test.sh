export GREEN="\e[0;33m"
export NC="\e[0;m"

mkdir -p ./data/output/

echo -e "${GREEN}================================================Running Unoptimized============================================${NC}"
python ./python/bm25.py 

echo -e "${GREEN}=================================================Running Optimized=============================================${NC}"
echo "=======================================Dimension = 400 | Top N = 1000=================================="
python ./python/bm25Optimized.py -d 400 -n 1000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 400 | Top N = 5000=================================="
python ./python/bm25Optimized.py -d 400 -n 5000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 400 | Top N = 10000================================="
python ./python/bm25Optimized.py -d 400 -n 10000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 200 | Top N = 1000=================================="
python ./python/bm25Optimized.py -d 200 -n 1000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 200 | Top N = 5000=================================="
python ./python/bm25Optimized.py -d 200 -n 5000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 200 | Top N = 10000================================="
python ./python/bm25Optimized.py -d 200 -n 10000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 100 | Top N = 1000=================================="
python ./python/bm25Optimized.py -d 100 -n 1000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 100 | Top N = 5000=================================="
python ./python/bm25Optimized.py -d 100 -n 5000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 100 | Top N = 10000================================="
python ./python/bm25Optimized.py -d 100 -n 10000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 60 | Top N = 1000==================================="
python ./python/bm25Optimized.py -d 60 -n 1000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 60 | Top N = 5000==================================="
python ./python/bm25Optimized.py -d 60 -n 5000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 60 | Top N = 10000=================================="
python ./python/bm25Optimized.py -d 60 -n 10000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 16 | Top N = 1000==================================="
python ./python/bm25Optimized.py -d 16 -n 1000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 16 | Top N = 5000==================================="
python ./python/bm25Optimized.py -d 16 -n 5000 -e 4 -m ./data/embeddings/model
echo "=======================================Dimension = 16 | Top N = 10000=================================="
python ./python/bm25Optimized.py -d 16 -n 10000 -e 4 -m ./data/embeddings/model