import sys
from collocations import *

def main():
    #sample testing code
    terms = ['indian', 'indians', 'native', 'natives']
    document = open('tribe_names.txt', 'r')
    tribe_names = document.read().lower()[3:]
    document.close()
    terms += nltk.word_tokenize(tribe_names)

    # Use this code the first time reading a text in order to tag words with
    # parts of speech and save a list of tagged words in a .txt file.
    #
    # c = Collocations(file_path = 'data\\raw\\clair.txt')
    # c.tagged_words_to_file(destination_path = 'tagged_words\\clair.txt')

    # After a .txt file containing a list of tagged words has been saved for a
    # text, use this code to load data much faster.
    #
    '''
    c = Collocations(file_path = 'data\\jennings.txt',
        tagged_words_path = 'tagged_words\\jennings.txt')

    c.tagged_bigrams(destination_path='results\\clark_adverbs.txt',
        bigram_filter=c.adverb_filter, terms=terms, collapse_terms=True)
    c.tagged_bigrams(destination_path='results\\clark_verbs.txt',
        bigram_filter=c.verb_filter, terms=terms, collapse_terms=True)
    c.tagged_bigrams(destination_path='results\\clark_adjectives.txt',
        bigram_filter=c.adjective_filter, terms=terms, collapse_terms=True)
'''
if __name__ == '__main__':
    main()
