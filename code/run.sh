echo -e "${GREEN}======================================================Building=================================================${NC}"
make query
make doc
echo -e "${GREEN}==================================================Transforming queries=========================================${NC}"
./bin/query -q ../../data/topics.51-100 -o ../../data/queries.txt
echo -e "${GREEN}=================================================Transforming documents========================================${NC}"
echo -e "May take upto 1 minute."
./bin/doc -i ../../data/train/ -o ../../data/train_mod/
echo -e "${GREEN}====================================================Cleaning build=============================================${NC}"
make clean
