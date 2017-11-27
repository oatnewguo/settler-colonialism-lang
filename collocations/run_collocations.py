import sys
from collocations import *

def main():
    #sample testing code
    terms = ['indian', 'native']
    document = open('tribe_names.txt', 'r')
    tribe_names = document.read().lower()[3:]
    document.close()
    terms += nltk.word_tokenize(tribe_names)
    terms += [word + 's' for word in terms]
    terms += [word + 'es' for word in terms]

    # Use this code the first time reading a text in order to tag words with
    # parts of speech and save a list of tagged words in a .txt file.
    #
    #c = Collocations(file_path = 'data\\clean\\boone_from_filson.txt')
    #c.tagged_words_to_file(destination_path = 'tagged_words\\boone_from_filson.txt')

    # After a .txt file containing a list of tagged words has been saved for a
    # text, use this code to load data much faster.
    #
    c = Collocations(file_path = 'data\\clean\\filson.txt',
        tagged_words_path = 'tagged_words\\filson.txt')

    c.tagged_bigrams(destination_path='results\\filson_adverbs.txt',
        bigram_filter=c.adverb_filter, terms=terms, collapse_terms=True, freq_filter=1)
    c.tagged_bigrams(destination_path='results\\filson_verbs.txt',
        bigram_filter=c.verb_filter, terms=terms, collapse_terms=True, freq_filter=1)
    c.tagged_bigrams(destination_path='results\\filson_adjectives.txt',
        bigram_filter=c.adjective_filter, terms=terms, collapse_terms=True, freq_filter=1)

if __name__ == '__main__':
    main()
