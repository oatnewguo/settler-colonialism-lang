import sys
from collocations import *

def main():
    #sample testing code
    terms = ['indian', 'indians']

    '''Use this code in order to tag words with parts of speech and save results
        in a .txt file. Once a text file has been saved, use the code below to
        load data much faster.
        
    c = Collocations(file_path = 'data\\harrison1.txt', terms = terms)
    c.tagged_words_to_file(destination_path = 'tagged_words\\harrison1.txt')
    '''

    c = Collocations(file_path = 'data\\harrison1.txt', terms = terms,
        tagged_words_path = 'tagged_words\\harrison1.txt')
    c.tagged_bigrams(destination_path='results\\harrison1.txt',
        bigram_filter=c.adjective_filter)

if __name__ == '__main__':
    main()
