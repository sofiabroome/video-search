import json
import sys
from nltk.corpus import wordnet as wn

def extract_descriptor(json_data):
    """ Turn .json data into a concatenation of words """
    samples = [sample[1] for sample in json_data]
    words = [word[0].replace("_", " ") for sample in samples for word in sample]
    return " ".join(words)

def read_json_data(file_name):
    """ Loads json data from file. """
    with open(file_name) as json_file:
      data = json.load(json_file)
    return data

def expand_query(words, lu):
    """ Expands query to include mother categories (hypernyms) from 
	Wordnet as many levels up as the method parameter lu is set to."""
    expansion = []
    for word in words.split(" "):
        ss = wn.synsets(word)
	first_ss = ss[0]
	hypernyms = first_ss.hypernym_paths()
	for hyper in hypernyms:
	    for l in range(1,lu+1):		
		one_hyper = hyper[-(l+1):-(l)]
		hyper_clean = find_between(str(one_hyper), "Synset('", ".")
	if hyper_clean not in expansion:
		    expansion.append(hyper_clean)
    expansion_string = " ".join(expansion)
    expanded_query = " ".join([words, expansion_string])
    """ Returns the expanded query as a string with space-separated words """
    return expanded_query

def find_between(s, first, last):
    try:
	s.index(first)
	len(first)
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

if __name__ == "__main__":
    ARGV = sys.argv
    if len(ARGV) == 1:
	print """ usage: python wordnetscript.py <jsondata file>
		  <no of considered hypernyms per word> """
    elif len(ARGV) == 3:
        JSON_DATA_FILE = ARGV[1]
        lu = int(ARGV[2])
        json_data = read_json_data(JSON_DATA_FILE)
        words = extract_descriptor(json_data)
	print "original query:"
	print words
	print "expanded query:"
        expanded_query = expand_query(words, lu) 
