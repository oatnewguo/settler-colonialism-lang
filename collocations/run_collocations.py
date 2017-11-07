import sys
from collocations import *

def main():
    #sample testing code
    terms = ['indian', 'indians']
    c = Collocations('data\\harrison1.txt', terms)
    c.bigrams(destination_path='results\\harrison1.txt', bigram_filter=c.adjective_filter)


if __name__ == '__main__':
    main()
