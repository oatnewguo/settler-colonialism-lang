import nltk
from nltk.collocations import *

class Collocations:

    def __init__(self, file_path, terms=[], tagged_words_path=None):
        '''Creates a Collocations instance with a text and, optionally, terms of
            interest.

        file_path - string path to .txt input file; used to generate full
            description of results in output file, whether or not tagged_words
            is given
        terms - string list of words of interest to be used in ngrams filters
        tagged_words_path - string path to .txt file containing string
            representation of list of tagged words in input file; saves time and
            resources on computation
        '''

        self.file_path = file_path

        if tagged_words_path == None:
            #open input file, extract text, and close file
            document = open(file_path, 'r')
            raw = document.read().encode().decode('utf-8').lower()
            document.close()

            #tokenize text into words and tag parts of speech
            sentences = nltk.sent_tokenize(raw)
            tokenized_sentences = [nltk.word_tokenize(w) for w in sentences]
            tagged_sentences = nltk.pos_tag_sents(tokenized_sentences)
            self.tagged_words = sum(tagged_sentences, [])
        else:
            import ast
            document = open(tagged_words_path, 'r')
            self.tagged_words = ast.literal_eval(document.read())
            document.close()

        #initialize terms of interest
        self.terms = terms

    def set_terms(self, terms):
        '''Set a new list of terms of interest.

        terms - string list of words of interest to be used in ngrams filters
        '''

        self.terms = terms

    def tagged_words_to_file(self, destination_path):
        '''Writes the current list of tagged words as a string to file.

        destination_path - string path to .txt output file
        '''

        words = open(destination_path, 'w')
        words.write(str(self.tagged_words))
        words.close()

    def tagged_bigrams(self, destination_path, num_bigrams=10, window_size=5,
        freq_filter=3, bigram_filter=None):
        '''Finds bigrams in the list tagged_words in the manner specified by the
            parameters and writes results to a text file.

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
        results.write('Top %d bigram collocations in %s, with a window size of '
            '%d. Filtered for bigrams with a minimum frequency of %d. '
            % (num_bigrams, self.file_path, window_size, freq_filter))
        if not bigram_filter == None:
            results.write('Filtered for bigrams for which %s returns False. '
                'Potentially filtered using the following terms of interest:\n'
                % (bigram_filter.__name__))
            for t in self.terms:
                results.write('\t%s\n' % t)
        results.write('Sorted according to Dunning\'s log likelihood ratio, but '
            'displaying frequency counts.\n---------------------------------\n')

        bigrams = finder.nbest(bigram_measures.likelihood_ratio, num_bigrams)
        freq_dist = finder.ngram_fd
        for (word1, pos1), (word2, pos2) in bigrams:
            results.write('%d %s %s \n' %
                (freq_dist[(word1, pos1), (word2, pos2)], word1, word2))
        results.close()

    def adjective_filter(self, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as an adjective.

        word1, word2 - tuples of a string word and its string pos tag
        '''

        if (word1[0] in self.terms and word2[1] == 'JJ' or
            word2[0] in self.terms and word1[1] == 'JJ'):
            return False
        return True

    def verb_filter(self, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as a verb.

        word1, word2 - tuples of a string word and its string pos tag
        '''

        if (word1[0] in self.terms and word2[1].startswith('VB') or
            word2[0] in self.terms and word1[1].startswith('VB')):
            return False
        return True
