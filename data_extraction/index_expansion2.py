import json
import sys
from nltk.corpus import wordnet as wn

def expand_index(words, lu):
    """Creates list of mother categories (hypernyms) from 
    Wordnet as many levels up as the method parameter lu is set to."""
    #expansion = []
    expansion_terms = dict()
    for word in words.split(" "):
        ss = wn.synsets(word)
        # some words like "of" has no hypernyms in wordnet; we should skip expanding these
        if len(ss) == 0:
            continue
        for synset in ss
            hypernyms = synset.hypernym_paths()
            for hypers in hypernyms:
                for l in range(1,lu+1):		
                    one_hyper = hypers[-(l+1):-(l)]
                    hyper_clean = find_between(str(one_hyper), "Synset('", ".n")
                    if "_" in hyper_clean:
                        hc_as_list = list(hyper_clean)
                        underscore_idx = [i for i, x in enumerate(hc_as_list) if x == "_"]
                        for idx in underscore_idx:
                            hc_as_list[idx] = " "
                        fixed_string = "".join(hc_as_list)
                        separate_words = fixed_string.split(" ")
                        for sepword in separate_words:
                            #expansion.append(sepword)
                            expansion_terms[sepword] = True
                    else:
                        #expansion.append(hyper_clean)
                        expansion_terms[hyper_clean] = True
    expander_term_string = " ".join(expansion_terms.keys())
    #expansion_string = " ".join(expansion)
    #expanded_term_string = " ".join([words, expansion_string])
    """ Returns the list of expanded terms as a string with space-separated words """
    return expanded_term_string

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
    expanded_query = expand_index(words, lu)
    print expanded_query
