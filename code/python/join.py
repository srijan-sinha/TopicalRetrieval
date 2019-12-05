import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', action="store", dest="folder", help="folder path to get files for concatenation")
parser.add_argument('-o', action="store", dest="out_file", help="location for concatenated output")

results = parser.parse_args()
folder = results.folder + "/*"
out_file = results.out_file

list_files = glob.glob(folder)
list_files.sort()

f_out = open(out_file,"w")

for i in list_files:
	f = open(i, "r")
	text = f.read()
	f_out.write(text)
