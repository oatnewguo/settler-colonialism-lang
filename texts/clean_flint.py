import sys
import re
from clean_loc_misspellings import misspellings

def main(path, new_path):
    raw = open(path, 'r', encoding='utf-8')
    text = raw.read()
    raw.close()

    #ignore non-content beginning and end of book
    text = text[text.index('INDIAN WARS OF THE WEST.'):]

    #get rid of words that don't contain alphanumerical characters
    temp_text = ''
    while not text == temp_text:
        temp_text = text
        text = re.sub(r' [^\w\s]* ', ' ', text)
        text = re.sub(r'(\n[^\w\s]* )|( [^\w\s]*\n)', '\n', text)
        text = re.sub(r'\n[^\w\s]*\n', '\n\n', text)

    #get rid of double periods and double commas
    text = text.replace('..', '.')
    text = text.replace(',,', ',')

    #remove periods and commas directly preceding words and in between words, as
    #well as hyphens directly preceding and quotation marks in between
    text = re.sub(r'(\s)[\.,-](\w+)', r'\1\2', text)
    text = re.sub(r'(\w+)[\.,\'\"](\w+)', r'\1 \2', text)

    #delete unwanted phrases
    text = re.sub(r'\nCHAPTER \w+\.\n*', '\n', text)

    #correct more misspellings, listed in file. Many misspellings are surrounded
    #by their immediate context (e.g., spaces or punctuation) to prevent over-
    #correction of other correct words that contain misspellings as substrings.
    for misspelling, correct in misspellings.items():
        text = text.replace(misspelling, correct)

    #join hyphenated words; unwanted hyphens not followed by whitespace may need
    #to be cleaned manually or removed using misspellings
    text = re.sub(r'-\s+', '', text)

    new_file = open(new_path, 'w', encoding='utf-8')
    new_file.write(text)
    new_file.close()

if __name__ == '__main__':
    main('raw/flint.txt', 'clean/flint.txt')
