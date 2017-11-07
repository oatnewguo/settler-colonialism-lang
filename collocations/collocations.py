import nltk
from nltk.collocations import *

class Collocations:

    def __init__(self, file_path, terms=[]):
        '''Creates a Collocations instance with a text and, optionally, terms of interest.

        file_path - path to input file
        terms - words of interest to be used in ngrams filters
        '''

        #open input file, extract text, and close file
        self.document = open(file_path, 'r')
        self.raw = self.document.read().encode().decode('utf-8').lower()
        self.document.close()

        #tokenize text into words and tag parts of speech
        self.sentences = nltk.sent_tokenize(self.raw)
        self.tokenized_sentences = [nltk.word_tokenize(w) for w in self.sentences]
        self.tagged_sentences = nltk.pos_tag_sents(self.tokenized_sentences)
        self.tagged_words = sum(self.tagged_sentences, [])

        #initialize terms of interest
        self.terms = terms

    def bigrams(self, destination_path, num_bigrams=10, window_size=5, freq_filter=3, bigram_filter=None):
        '''Finds bigrams in the text in the manner specified by the parameters and writes results to a text file.

        destination_path - path to output file
        num_bigrams - the number of bigrams to display from among the most frequent
        window_size - size of window within which to find bigrams
        freq_filter - minimum number of occurrences for a bigram to count
        bigram_filter - ngram filter for bigrams
        '''

        #find bigrams
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(self.tagged_words, window_size = window_size)

        #apply filters
        finder.apply_freq_filter(freq_filter)
        if not bigram_filter == None:
            finder.apply_ngram_filter(bigram_filter)

        #open output file, write results, and close file
        results = open(destination_path, 'w')
        for (word1, pos1), (word2, pos2) in finder.nbest(bigram_measures.likelihood_ratio, num_bigrams):
            results.write(word1 + ' ' + word2 + '\n')
        results.close()

    def adjective_filter(self, word1, word2):
        '''Returns False if one word is a term of interest and the other has been tagged as an adjective.'''

        if (word1[0] in self.terms and word2[1] == 'JJ') or (word2[0] in self.terms and word1[1] == 'JJ'):
            return False
        return True

    def verb_filter(self, word1, word2):
        '''Returns False if one word is a term of interest and the other has been tagged as a verb.'''

        if (word1[0] in self.terms and word2[1].startswith('VB')) or (word2[0] in self.terms and word1[1].startswith('VB')):
            return False
        return True

    def set_terms(self, terms):
        '''Set a new list of terms of interest.'''

        self.terms = terms
