export GREEN="\e[0;33m"
export NC="\e[0;m"

mkdir -p data/trec_data bin build

echo -e "${GREEN}======================================================Building=================================================${NC}"
make query
make doc

echo -e "${GREEN}==================================================Transforming queries=========================================${NC}"
./bin/query -q ./data/trec_data/topics.51-100 -o ./data/trec_data/queries.txt

echo -e "${GREEN}=================================================Transforming documents========================================${NC}"
echo -e "May take upto 1 minute."
./bin/doc -i ./data/trec_data/train/ -o ./data/trec_data/train_mod/

echo -e "${GREEN}====================================================Cleaning build=============================================${NC}"
make clean

echo -e "${GREEN}====================================================Concatenating==============================================${NC}"
python ./python/join.py -f ./data/trec_data/train_mod/ -o ./data/trec_data/train.txt
python ./python/map.py -f ./data/trec_data/train_mod -m ./data/pickle/trainTagsToIndex.pkl