#include <getopt.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <utility>
#include <boost/algorithm/string.hpp>
#include <boost/tokenizer.hpp>

using namespace std;

pair< int, unordered_map <string, int> > queries[50];

int tagType(string str) {
	
	int ans = 0;
	int len = str.length();
	if (str.at(0) == '<' && str.at(len-1) == '>') {
		ans = 1;
		if (str.at(1) == '/')
			ans = 2;
	}
	return ans;

}

void readQuery (ifstream& is, ofstream& os, int queryNum) {

	stringstream ss;
	string temp;
	
	is >> temp;
	if (tagType(temp) != 1)	cerr << "Error! Opening topic tag not found." << endl;

	is >> temp;
	if (tagType(temp) != 1)	cerr << "Error! Opening head tag not found." << endl;


	is >> temp;
	while (tagType(temp) != 1)
		is >> temp;

	is >> temp;
	is >> temp;
	queries[queryNum].first = stoi(temp);
	while (tagType(temp) != 1) {
		is >> temp;
	}

	while (temp != "</top>") {
		if (tagType(temp) == 1) {
			is >> temp;
			is >> temp;
			while (tagType(temp) == 0) {
				ss << temp << " ";
				is >> temp;
			}
		}
		else if (tagType(temp) == 2) {
			is >> temp;
		}
	}

	string s = ss.str();
	boost::algorithm::to_lower(s);
	boost::algorithm::trim(s);
	os << s <<endl;

}

void readFile (ifstream& is, ofstream& os) {

	for (int i = 0; i < 50; i++) {
		readQuery(is,os,i);
	}

}

void readCmdArgs (int argc, char *argv[], string& queryFile, string& outputFile) {

	int c;
	bool query = false, output = false;
	static struct option long_options[] = {{"query", required_argument, 0, 'q'}, {"output", required_argument, 0, 'o'}};
	int option_index = 0;
	while (1) {
		c = getopt_long (argc, argv, "q:o:", long_options, &option_index);
		if (c == -1)
			break;
		switch (c) {
			case 'q':
				queryFile = string(optarg);
				query = true;
				break;
			case 'o':
				outputFile = string(optarg);
				output = true;
				break;
			default:
				abort ();
		}
		if (query && output)
			break;
	}

}


int main(int argc, char *argv[]) {

	string queryFile, outputQueryFile;
	// topicFile = "/home/cse/btech/cs1160315/scratch/project_col864/data/topics.51-100";
	readCmdArgs(argc, argv, queryFile, outputQueryFile);				cerr << "Reading query file and writing output." << endl;
	ifstream fs_query (queryFile);
	ofstream fs_out (outputQueryFile);
	readFile(fs_query, fs_out);													cerr << "Done." << endl;

}