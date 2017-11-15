import sys
from collocations import *

def main():
    #sample testing code
    terms = ['indian', 'indians']

    '''Use this code in order to tag words with parts of speech and save results
        in a .txt file. Once a text file has been saved, use the code below to
        load data much faster.

    c = Collocations(file_path = 'data\\harrison.txt')
    c.tagged_words_to_file(destination_path = 'tagged_words\\harrison.txt')
'''

    c = Collocations(file_path = 'data\\harrison.txt',
        tagged_words_path = 'tagged_words\\harrison.txt')
    c.tagged_bigrams(destination_path='results\\harrison_verbs_collapsed.txt',
        bigram_filter=c.verb_filter, terms=terms, collapse_terms=True)

if __name__ == '__main__':
    main()
