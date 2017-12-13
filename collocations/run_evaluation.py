import sys
from collocations import *
from evaluate_tagging import *

def main():
    e = EvaluateTagging('tagged_words/filson.txt')
    e.evaluate(100, 'tagging_evaluations/filson.txt')

if __name__ == '__main__':
    main()
