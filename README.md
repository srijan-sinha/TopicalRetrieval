# TopicalRetrieval
This project uses the TIPSTER dataset available at TREC. The aim is to improve query speed by using a candidate set of documents rather than the whole collection.
##How to Run

Copy the TIPSTER dataset at ```./code/data/trec_data/``` such that the query file (```topics.51-100```) is located at ```code/data/trec_data/``` and the documents are located in a directory named ```train``` inside the same folder.  

Now from the ```./code/``` directory run the scripts one after the other as follows:  
```
./scripts/preprocess.sh
./scripts/pretest.sh
./scripts/test.sh
```  
The output rankings will be suitably generated at ```code/data/output/``` and the query timings will be outputted to the console.

