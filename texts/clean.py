import sys
import re
from cleaning_misspellings import misspellings

def read(path):
    '''Reads a text file to be cleaned.'''

    raw = open(path, 'r', encoding='utf-8')
    text = raw.read()
    raw.close()
    return text

def clean_and_write(text, new_path):
    '''Cleans text and saves it to file.'''

    #get rid of words that don't contain alphanumerical characters
    temp_text = ''
    while not text == temp_text:
        temp_text = text
        text = re.sub(r' [^\w\s]+ ', ' ', text)
        text = re.sub(r'(\n[^\w\s]+ )|( [^\w\s]+\n)', '\n', text)
        text = re.sub(r'\n[^\w\s]+\n', '\n\n', text)

    #get rid of double periods and double commas
    text = text.replace('..', '.')
    text = text.replace(',,', ',')

    #remove periods and commas directly preceding words and in between words, as
    #well as hyphens directly preceding and quotation marks in between
    text = re.sub(r'(\s)[\.,-](\w+)', r'\1\2', text)
    text = re.sub(r'(\w+)[\.,\'\"](\w+)', r'\1 \2', text)

    #correct misspellings, listed in file. Many misspellings are surrounded by
    #their immediate context (e.g., spaces or punctuation) to prevent over-
    #correction of other correct words that contain misspellings as substrings.
    for misspelling, correct in misspellings.items():
        text = text.replace(misspelling, correct)

    #join hyphenated words; unwanted hyphens not followed by whitespace may need
    #to be cleaned manually or removed using misspellings
    text = re.sub(r'-\s+', '', text)

    new_file = open(new_path, 'w', encoding='utf-8')
    new_file.write(text)
    new_file.close()

def clean_flint():
    text = read('raw/flint.txt')
    text = re.sub(r'\nCHAPTER \w+\.\n*', '\n', text)
    clean_and_write(text[text.index('INDIAN WARS OF THE WEST.'):],
        'clean/flint.txt')

def clean_oldschool():
    text = read('raw/oldschool.txt')
    clean_and_write(text[text.index('The publisher of the Port Folio'):
        text.index('MISS SOMEDAY.')] + text[text.index(
        'In removing an artificial mound'):], 'clean/oldschool.txt')

def clean_darby():
    text = read('raw/darby.txt')
    text = re.sub('\n(EMIGRANT\'S GUIDE. \w*)|(\w* EMIGRANT\'S GUIDE.)\n', '\n', text, flags=re.I)
    clean_and_write(text[:text.index('Note.—These tables ought to have made part')], 'clean/darby.txt')

def clean_generic(path, new_path):
    text = read(path)
    clean_and_write(text, new_path)

def main():
    clean_flint()
    clean_oldschool()
    clean_darby()
    clean_generic('raw/rafinesque.txt', 'clean/rafinesque.txt')
    clean_generic('raw/cuming.txt', 'clean/cuming.txt')
    clean_generic('raw/cutlerfirstmap.txt', 'clean/cutlerfirstmap.txt')
    clean_generic('raw/cutlertopographicaldescription.txt', 'clean/cutlertopographicaldescription.txt')
    clean_generic('raw/brown.txt', 'clean/brown.txt')
    clean_generic('raw/evans.txt', 'clean/evans.txt')
    clean_generic('raw/peck.txt', 'clean/peck.txt')
    clean_generic('raw/clark.txt', 'clean/clark.txt')
    clean_generic('raw/jennings.txt', 'clean/jennings.txt')
    clean_generic('middle/stclair1.txt', 'clean/stclair1.txt')
    clean_generic('middle/stclair2.txt', 'clean/stclair2.txt')
    clean_generic('middle/harrison1.txt', 'clean/harrison1.txt')
    clean_generic('middle/harrison2.txt', 'clean/harrison2.txt')

if __name__ == '__main__':
    main()
