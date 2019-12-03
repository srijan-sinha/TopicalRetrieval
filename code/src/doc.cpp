#include <stdlib.h>
#include <getopt.h>
#include <dirent.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include "rapidxml.hpp"
#include <sstream>
#include <boost/algorithm/string.hpp>
#include <boost/tokenizer.hpp>
#include "rapidxml_print.hpp"
#include "rapidxml_utils.hpp"

using namespace std;

vector<string> files;
vector<string> file_name;
uint64_t totalDocs = 0;
uint64_t totalFiles = 0;

void listFiles (string directory) {

	DIR *dir;
	struct dirent *ent;
	string fname;
	char directory_name[64];
	strcpy(directory_name, directory.c_str()); 
	if ((dir = opendir (directory_name)) != NULL) {
	  while ((ent = readdir (dir)) != NULL) {
	  	fname = ent->d_name;
	  	if (fname != ".." && fname != ".") {
	  		stringstream ss;
	  		string s;
	  		ss << directory;
	  		ss << fname;
	  		s = ss.str();
	    	files.push_back(s);
	    	file_name.push_back(fname);
	    }
	  }
	  closedir (dir);
	}
	else {
	  perror ("Not able to open directory");
	}

}

void retrieveText (rapidxml::xml_node<>* text, ostringstream& ss, bool debug) {

	while (text != 0) {
		rapidxml::xml_node<>* innerNode = text->first_node();
		while (innerNode != 0) {
			ss << innerNode->value();
			innerNode = innerNode->next_sibling();
		}
		text = text->next_sibling();
	}

}

void readFile (string filename, string inputDir, string outputDir) {
	

	stringstream input;
	input << inputDir << filename;
	string inputFile = input.str();

	stringstream output;
	output << outputDir << filename;
	string outputFile = output.str();

	streampos size;
	char *fileContent;
	ifstream file;
	ofstream os (outputFile);
	file.open(inputFile, ios::in|ios::ate|ios::binary);

	if (file.is_open()) {
		size = file.tellg();
		size += 1;
		fileContent = new char[size];
		file.seekg(0, ios::beg);
		size -= 1;
		file.read(fileContent, size);
		file.close();
	}
	else {
		cerr << "Unable to open file " << filename << endl;
	}
	fileContent[size]= '\0';

	rapidxml::xml_document<> doc;
	doc.parse<0>(fileContent);
	rapidxml::xml_node<>* document = doc.first_node();

	rapidxml::xml_node<>* docno;
	rapidxml::xml_node<>* text;
	while (document != 0) {
		docno = document->first_node();
		text = docno->next_sibling();

		string docNum(docno->value());
		boost::algorithm::trim(docNum);

		string str(text->name());
		while (str != "TEXT") {
			text = text->next_sibling();
			str.assign(text->name());
		}

		ostringstream ss;
		retrieveText(text, ss, false);
		string s = ss.str();
		boost::algorithm::to_lower(s);
		boost::algorithm::trim(s);
		s = boost::algorithm::replace_all_copy(s, "\n", " ");
		os << docNum << "\t" << s << endl;

		totalDocs++;
		document = document->next_sibling();
	}
	doc.clear();
	free(fileContent);
	return;

}

void readCmdArgs (int argc, char *argv[], string& inputDir, string& outputDir) {

	int c;
	bool input = false, output = false;
	static struct option long_options[] = {{"input", required_argument, 0, 'i'}, {"output", required_argument, 0, 'o'}};
	int option_index = 0;
	while (1) {
		c = getopt_long (argc, argv, "i:o:", long_options, &option_index);
		if (c == -1)
			break;
		switch (c) {
			case 'i':
				inputDir = string(optarg);
				input = true;
				break;
			case 'o':
				outputDir = string(optarg);
				output = true;
				break;
			default:
				abort ();
		}
		if (input && output)
			break;
	}

}

int main (int argc, char *argv[]) {

	string inputDir, outputDir;
	if (argc != 3) {
		cerr << "Usage: <binary> -i <inputDir> -o <outputDir>" << endl;
		return 0;
	}
	readCmdArgs(argc, argv, inputDir, outputDir);		cerr << "Collecting file names." << endl;
	listFiles(inputDir);								cerr << "Iterating and creating files." << endl;
	for (auto i : file_name) {
		readFile(i, inputDir, outputDir);
		totalFiles++;
	}
	cout << "Total docs: " << totalDocs << endl;
	cout << "Total files: " << totalFiles << endl;

	return 0;

}