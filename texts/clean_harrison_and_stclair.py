from __future__ import division
from clean_harrison_and_stclair_misspellings import unwanted, misspellings
from nltk import sent_tokenize, word_tokenize
import matplotlib.pyplot, re, string
import regex as re
import sys

def main(path,new_path):
    new_file = open(new_path, 'w')

    dirty = importText(path)

    clean(dirty, new_path)

# imports text, tokenizes it into sentences
def importText(text):
    file = open(text)

    raw = file.read().encode().decode('utf8')

    file.close()

    sentences = sent_tokenize(raw)

    return sentences

#  helper function that compares if two word tokenized sentences are a
#  'close enough' match to be deleted
def closeEnoughMatch(s1, s2):
    count = 0

    sent1 = word_tokenize(s1)
    sent2 = word_tokenize(s2)
    length = len(sent2)

    for w1 in sent1:
        if w1 == sent2[0] and length == 1:
            return True
        if w1 in sent2:
            count += 1
        if (count == length) or (count >= length - 2 and length > 2):
            return True

    return False

def clean(text, new_path):
    new_file = open(new_path, 'w')

    # set to True if the previous token ends with a hyphen
    joinnext = False

    # sentence, word to be appended
    new_sentence = []
    new_word = ''

    # records current token
    save = ''

    new_clean = []

    new_joined_sentence = ''

    for sentence in text:
        for word in word_tokenize(sentence):
            new_word = word
            # concatenate hyphenated words
            if joinnext:
                new_word = save + word
                joinnext = False

            if word[-1] == '-':
                joinnext = True
                save = word[:-1]
                new_word = ''

            # correct misspellings
            elif word in misspellings:
                new_word = misspellings[word]

            new_sentence += [new_word]

        for unwanted_sent in unwanted:
        # take out extraneous sentences and phrases
            if closeEnoughMatch(sentence, unwanted_sent):
                new_sentence = []

        # add in line breaks
        if 'TO' in sentence:
            new_clean += '\n\n'

        new_clean += [' '.join(new_sentence)]

        new_sentence = []

    new_string = ' '.join(new_clean)

    new_file.write(new_string)
    new_file.close()

main('raw/stclair1.txt', 'middle/stclair1.txt')
main('raw/stclair2.txt', 'middle/stclair2.txt')
main('raw/harrison1.txt', 'middle/harrison1.txt')
main('raw/harrison2.txt', 'middle/harrison2.txt')
