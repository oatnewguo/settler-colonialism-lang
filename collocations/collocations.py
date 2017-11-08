import nltk
from nltk.collocations import *

class Collocations:

    def __init__(self, file_path, terms=[], tagged_words=None):
        '''Creates a Collocations instance with a text and, optionally, terms of
            interest.

        file_path - string path to .txt input file; used to generate full
            description of results in output file, whether or not tagged_words
            is given
        terms - string list of words of interest to be used in ngrams filters
        tagged_words - string path to .txt file containing string representation
            of list of tagged words in input file; saves time and resources on
            computation
        '''

        #open input file, extract text, and close file
        self.file_path = file_path
        self.document = open(file_path, 'r')
        self.raw = self.document.read().encode().decode('utf-8').lower()
        self.document.close()

        #tokenize text into words and tag parts of speech
        self.sentences = nltk.sent_tokenize(self.raw)
        self.tokenized_sentences = [nltk.word_tokenize(w) for w in
            self.sentences]
        self.tagged_sentences = nltk.pos_tag_sents(self.tokenized_sentences)
        self.tagged_words = sum(self.tagged_sentences, [])

        #initialize terms of interest
        self.terms = terms

    def bigrams(self, destination_path, num_bigrams=10, window_size=5,
        freq_filter=3, bigram_filter=None):
        '''Finds bigrams in the text in the manner specified by the parameters
            and writes results to a text file.

        destination_path - string path to .txt output file
        num_bigrams - int number of bigrams to display from among the most
            frequent
        window_size - int size of window within which to find bigrams
        freq_filter - int minimum number of occurrences for a bigram to count
        bigram_filter - function ngram filter for bigrams
        '''

        #find bigrams
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(self.tagged_words,
            window_size = window_size)

        #apply filters
        finder.apply_freq_filter(freq_filter)
        if not bigram_filter == None:
            finder.apply_ngram_filter(bigram_filter)

        #open output file, write results, and close file
        results = open(destination_path, 'w')
        results.write('Top ' + str(num_bigrams) + ' bigram collocations in ' +
            self.file_path + ', with a window size of ' + str(window_size) +
            '. Filtered for bigrams with a minimum frequency of ' +
            str(freq_filter) + ' and for bigrams for which ' +
            bigram_filter.__name__ + ' returns False.\n---------------------\n')

        bigrams = finder.nbest(bigram_measures.likelihood_ratio, num_bigrams)
        for (word1, pos1), (word2, pos2) in bigrams:
            results.write(word1 + ' ' + word2 + '\n')
        results.close()

    def adjective_filter(self, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as an adjective.'''

        if (word1[0] in self.terms and word2[1] == 'JJ') or
            (word2[0] in self.terms and word1[1] == 'JJ'):
            return False
        return True

    def verb_filter(self, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as a verb.'''

        if (word1[0] in self.terms and word2[1].startswith('VB')) or
            (word2[0] in self.terms and word1[1].startswith('VB')):
            return False
        return True

    def set_terms(self, terms):
        '''Set a new list of terms of interest.'''

        self.terms = terms
