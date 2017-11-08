import sys
from collocations import *

def main():
    #sample testing code
    terms = ['indian', 'indians']
    c = Collocations(file_path = 'data\\harrison1.txt', terms = terms,
        tagged_words_path = 'tagged_words\\harrison1.txt')
    c.tagged_bigrams(destination_path='results\\harrison1.txt',
        bigram_filter=c.adjective_filter)

if __name__ == '__main__':
    main()
