import sys
import re

def main(path, new_path):
    file = open(path, 'r')
    text = file.read()
    file.close()

    text = text.replace('{page image}', '')
    text = re.sub('Page \d*', '', text)

    new_file = open(new_path, 'w')
    new_file.write(text)
    new_file.close()

if __name__ == '__main__':
    main('raw\\filson.txt', 'clean\\filson.txt')
