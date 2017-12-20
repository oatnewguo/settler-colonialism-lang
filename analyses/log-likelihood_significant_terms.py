'''This file was adapted from a file taken from the GitHub of Ted Dunning, creator of the log-
    likelihood score. It can be found here: https://github.com/tdunning/python-llr'''

import sys

from collections import Counter
import re

import llr

def count(files):
    '''Counts the words contained in a list of files'''
    words = []
    for file in files:
        document = open(file, 'r', encoding='utf-8')
        words += re.findall('\w+', re.sub('[\r\n]', ' ', document.read()))
        document.close()
    words = [w.lower() for w in words]
    return Counter(words)

def main(focus_path, other_paths, output_path, num_terms=30):
    '''Finds the significant words in the text located at focus_path, compared
        with the rest of the corpus.

    focus_path - string path to .txt file to focus on
    other_paths - list of string paths to .txt files comprising the rest of the
        corpus
    output_path - string path to .txt file in which to write results
    num_terms - number of significant terms to show
    '''

    focus_text = count([focus_path])
    other_text = count(other_paths)

    diff = llr.llr_compare(focus_text, other_text)
    ranked = sorted(diff.items(), key=lambda x: x[1])

    with open(output_path, 'w') as output:
        for word, score in reversed(ranked[-num_terms:]):
            output.write('{:<20.10}   {}\n'.format(score, word))

if __name__ == '__main__':
    #main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    main('../texts/clean/publicdiscourse.txt', ['../texts/clean/privatediscourse.txt'], 'results/public_terms.txt')
    main('../texts/clean/privatediscourse.txt', ['../texts/clean/publicdiscourse.txt'], 'results/private_terms.txt')
