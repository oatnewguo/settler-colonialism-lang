import sys
from collocations import *
from evaluate_tagging import *

def main():
    e = EvaluateTagging('tagged_words\\jennings.txt')
    e.evaluate(7, 'tagging_evaluations\\jennings.txt')

if __name__ == '__main__':
    main()
