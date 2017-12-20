import ast
from random import *

class EvaluateTagging:

    def __init__(self, tagged_words_path):
        '''Initialize EvaluateTagging object with a list of tagged words.

        tagged_words_path - string path to .txt file containing a string literal
            representation of a list of tagged words
        '''

        document = open(tagged_words_path, 'r', encoding='utf-8')
        self.tagged_words = ast.literal_eval(document.read())
        document.close()
        self.list_length = len(self.tagged_words)

    def evaluate(self, num_words, output_path, window=3):
        '''With the help of the user, evaluate num_words tagged words and write
            results to file at output_path.

            output_path - string path to .txt file in which to write results
            num_words - int number of tagged words to evaluate
            window - number of words to show on either side of evaluated word
                for context
        '''

        print('\nYou will be evaluating the correctness of {} tagged words. For'
            ' each, please type in either \"y\" for a correct tag or \"n\" for '
            'an incorrect tag. Please refer to the Penn Treebank tagset, found '
            'here: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html'
            .format(num_words))
        print('\n===========================================================\n')

        correct = 0
        incorrect = 0
        results = ''

        for i in range(num_words):
            answer = None
            random = randint(0, self.list_length - 1)
            word, pos = self.tagged_words[random]
            before = self.tagged_words[max(0, random - window) : random]
            after = self.tagged_words[random + 1 : min(self.list_length,
                random + window + 1)]
            before = [word for word, pos in before]
            after = [word for word, pos in after]
            before = ' '.join(before)
            after = ' '.join(after)
            while not (answer == 'y' or answer == 'n'):
                answer = input('{}   ({} : {})   {}   |   '.format(before, pos, word,
                    after))
            if answer == 'y':
                correct += 1
                results += 'Y {}   ({} : {})   {}\n'.format(before, pos, word,
                    after)
            elif answer == 'n':
                incorrect += 1
                results += 'N {}   ({} : {})   {}\n'.format(before, pos, word,
                    after)

        results_file = open(output_path, 'w')
        results_file.write('Number correctly tagged: {}\n'.format(correct))
        results_file.write('Number incorrectly tagged: {}\n'.format(incorrect))
        results_file.write('Estimated accuracy on text: {}%\n\n'.format(
            100.0 * correct / (correct + incorrect)))
        results_file.write('==============================================\n\n')
        results_file.write(results)
        results_file.close()

        print('You have finished evaluating {} tagged words. {} words were '
            'tagged correctly, and {} were tagged incorrectly. Tagging has an '
            'estimated accuracy on this text of {}%.'.format(num_words,
            correct, incorrect, 100.0 * correct / (correct + incorrect)))
