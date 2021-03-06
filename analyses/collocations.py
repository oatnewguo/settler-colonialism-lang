import nltk
from nltk.collocations import *
from nltk.tag import StanfordPOSTagger
from functools import partial
import os
import re

class Collocations:

    def __init__(self, file_path, tagged_words_path=None):
        '''Creates a Collocations instance with a text

        file_path - string path to .txt input file; used to generate full
            description of results in output file, whether or not tagged_words
            is given
        tagged_words_path - string path to .txt file containing string
            representation of list of tagged words in input file; saves time and
            resources on computation
        '''

        self.file_path = file_path

        if tagged_words_path == None:
            #open input file, extract text, and close file
            document = open(file_path, 'r', encoding='utf-8')
            raw = document.read().lower()
            document.close()

            #tokenize text into words and tag parts of speech using the
            #Stanford part-of-speech tagger
            sentences = nltk.sent_tokenize(raw)
            tokenized_sentences = [nltk.word_tokenize(w) for w in sentences]

            java_path = 'C:/Program Files/Java/jdk-9.0.1/bin/java.exe'
            os.environ['JAVAHOME'] = java_path
            path_to_model = ('stanford-postagger-2017-06-09/models/'
                'english-left3words-distsim.tagger')
            path_to_jar = ('stanford-postagger-2017-06-09/'
                'stanford-postagger.jar')
            tagger = StanfordPOSTagger(path_to_model, path_to_jar)
            tagger.java_options='-mx4096m'
            tagged_sentences = tagger.tag_sents(tokenized_sentences)
            self.tagged_words = sum(tagged_sentences, [])
        else:
            #load pre-tagged words
            import ast
            document = open(tagged_words_path, 'r', encoding='utf-8')
            self.tagged_words = ast.literal_eval(document.read())
            document.close()

    def tagged_words_to_file(self, destination_path):
        '''Writes the current list of tagged words as a string to file.

        destination_path - string path to .txt output file
        '''

        words = open(destination_path, 'w', encoding='utf-8')
        words.write(str(self.tagged_words))
        words.close()

    def tagged_bigrams(self, destination_path, num_bigrams=100, window_size=5,
        freq_filter=1, bigram_filter=None, terms=None, collapse_terms=False):
        '''Finds bigrams in the list tagged_words in the manner specified by the
            parameters and writes results to a text file.

        destination_path - string path to .txt output file
        num_bigrams - int number of bigrams to display from among the highest
            scored
        window_size - int size of window within which to find bigrams
        freq_filter - int minimum number of occurrences for a bigram to count
        bigram_filter - function ngram filter for bigrams
        terms - string list of terms of interest to use in ngrams filter
            --- will only be used if a bigram_filter is given
        collapse_terms - boolean that is True if collocations should be found
            with all words in terms treated as the same, and False if
            collocations should be found with individual words in terms
        '''

        #delete any words that contain non-alphabetical characters
        self.tagged_words = [(w, pos) for (w, pos) in self.tagged_words if
            w.isalpha()]

        #find bigrams
        if collapse_terms:
            tagged_words_collapsed = []
            for (w, pos) in self.tagged_words:
                if w in terms:
                    tagged_words_collapsed.append(('___', '*'))
                else:
                    tagged_words_collapsed.append((w, pos))
            finder = BigramCollocationFinder.from_words(tagged_words_collapsed,
                window_size = window_size)
        else:
            finder = BigramCollocationFinder.from_words(self.tagged_words,
                window_size = window_size)

        #apply filters
        finder.apply_freq_filter(freq_filter)
        if not bigram_filter == None:
            if collapse_terms:
                finder.apply_ngram_filter(partial(bigram_filter, ['___']))
            else:
                finder.apply_ngram_filter(partial(bigram_filter, terms))

        #open output file, write results, and close file
        results = open(destination_path, 'w', encoding='utf-8')
        results.write('Top {} bigram collocations in {}, with a window size of '
            '{}. Filtered for bigrams with a minimum frequency of {}. '
            .format(num_bigrams, self.file_path, window_size, freq_filter))
        if not bigram_filter == None:
            results.write('Filtered for bigrams for which {} returns False. '
                'Depending on {}, potentially filtered using the following '
                'terms of interest:\n'.format(bigram_filter.__name__,
                bigram_filter.__name__))
            for t in terms:
                results.write('\t{}\n'.format(t))
            if collapse_terms:
                results.write('Terms of interest, represented as \"___\", were '
                    'collapsed and treated as the same term for collocations. ')
        results.write('Sorted according to Dunning\'s log-likelihood ratio, but'
            ' displaying frequency counts.\n')
        results.write('-----------------------------------------------------\n')
        results.write('Rank | Log-Likelihood Score | Frequency | Collocation\n')
        results.write('-----------------------------------------------------\n')

        bigram_measures = nltk.collocations.BigramAssocMeasures()
        bigrams = finder.score_ngrams(bigram_measures.likelihood_ratio)
        freq_dist = finder.ngram_fd
        count = 1
        for ((word1, pos1), (word2, pos2)), score in bigrams:
            results.write('{:<4}   {:<20.10}   {:<9}   {} {} \n'.format(count,
                score, freq_dist[(word1, pos1), (word2, pos2)], word1, word2))
            if count == num_bigrams:
                break
            count += 1
        results.close()

    def simple_filter(self, terms, word1, word2):
        '''Returns False if one word is a term of interest.

        terms - string list of terms of interest; if None, then the function
            will not filter at all
        word1, word2 - tuples of a string word and its string pos tag
        '''

        if (word1[0] in terms or word2[0] in terms):
            return False
        else:
            return True

    def adjective_filter(self, terms, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as an adjective.

        terms - string list of terms of interest; if None, then the function
            will not filter for terms of interest
        word1, word2 - tuples of a string word and its string pos tag
        '''

        if terms == None:
            if (word1[1] == 'JJ' or word2[1] == 'JJ'):
                return False
            else:
                return True
        else:
            if (word1[0] in terms and word2[1].startswith('JJ') or
                word2[0] in terms and word1[1].startswith('JJ')):
                return False
            else:
                return True

    def verb_filter(self, terms, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as a verb.

        terms - string list of terms of interest; if None, then the function
            will not filter for terms of interest
        word1, word2 - tuples of a string word and its string pos tag
        '''

        if terms == None:
            if (word1[1].startswith('VB') or word2[1].startswith('VB')):
                return False
            else:
                return True
        else:
            if (word1[0] in terms and word2[1].startswith('VB') or
                word2[0] in terms and word1[1].startswith('VB')):
                return False
            else:
                return True

    def adverb_filter(self, terms, word1, word2):
        '''Returns False if one word is a term of interest and the other has
            been tagged as an adverb.

        terms - string list of terms of interest; if None, then the function
            will not filter for terms of interest
        word1, word2 - tuples of a string word and its string pos tag
        '''

        if terms == None:
            if (word1[1].startswith('RB') or word2[1].startswith('RB')):
                return False
            else:
                return True
        else:
            if (word1[0] in terms and word2[1].startswith('RB') or
                word2[0] in terms and word1[1].startswith('RB')):
                return False
            else:
                return True
