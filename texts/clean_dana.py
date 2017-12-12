import sys
import re

def main(path, new_path):
    raw = open(path, 'r', encoding='utf-8')
    text = raw.read()
    raw.close()

    #ignore non-content beginning and end of book
    text = text[text.index('BE IT REMEMBERED'):text.index('CORRECTIONS AND ADDITIONS')]

    #get rid of words that don't contain alphanumerical characters
    temp_text = ''
    while not text == temp_text:
        temp_text = text
        text = re.sub(' [^\w\s]* ', ' ', text)
        text = re.sub('(\n[^\w\s]* )|( [^\w\s]*\n)', '\n', text)
        text = re.sub('\n[^\w\s]*\n', '\n\n', text)

    #correct misspellings
    misspellings = {
        'WWWWLVNVVN AW.N. W.W.M.A\R.S' : 'PRELIMINARY REMARKS',
        'FRELIMINARY' : 'PRELIMINARY',
        'GEOGRAWWWC AWA SRWWCW.S' : 'GEOGRAPHIC SKETCHES',
        'UłIO' : 'OHIO',
        'QHIO' : 'OHIO',
        'GHIO' : 'OHIO',
        'OHIOs' : 'OHIO',
        'OH10' : 'OHIO',
        'RENTUCKY' : 'KENTUCKY',
        '*NDIANA' : 'INDIANA',
        'INDIAN.A' : 'INDIANA',
        'Isbiana' : 'INDIANA',
        'ILLINQIS' : 'ILLINOIS',
        'ill DNOIS' : 'ILLINOIS',
        'JLLINOIS' : 'ILLINOIS',
        'LLLINOIs' : 'ILLINOIS',
        'Miss ISSIPPI' : 'MISSISSIPPI',
        'ALARAMA' : 'ALABAMA',
        'LočislanA' : 'LOUISIANA',
        'ILOUISIANA' : 'LOUISIANA',
        'Louis1ANA' : 'LOUISIANA',
        'LOUISHANA' : 'LOUISIANA',
        'WoRTHwESTERN' : 'NORTHWESTERN',
        'NORTHwBSTERN' : 'NORTHWESTERN',
        'NORTHWESTERN, TERRITORY' : 'NORTHWESTERN TERRITORY',
        'MISSOURITERRITORY' : 'MISSOURI TERRITORY',
        'MISSOURL' : 'MISSOURI',
        '_TENNESSEE' : 'TENNESSEE'
    }
    for misspelling, correct in misspellings.items():
        text = text.replace(misspelling, correct)

    #delete headings and page numbers, as well as extra noise
    headings = ['PREFACE', 'PRELIMINARY REMARKS', 'GEOGRAPHIC SKETCHES', 'OHIO',
        'KENTUCKY', 'INDIANA', 'ILLINOIS', 'TENNESSEE', 'MISSISSIPPI', 'ALABAMA',
        'EAST AND WEST FLORIDA', 'THE FLORIDAS', 'LOUISIANA', 'TEXAS',
        'MICHIGAN TERRITORY', 'NORTHWESTERN TERRITORY', 'ARKANSAW TERRITORY',
        'MISSOURI TERRITORY', 'COLUMBIA RIVER']
    text = re.sub('\n(' + '|'.join(headings)+')\S* \S* ', '', text, flags=re.I)
    text = re.sub('\n\S* (' + '|'.join(headings)+')\S* ', '', text, flags=re.I)

    #delete unwanted phrases
    text = text.replace('End of Section. Continue to next section or go to Table of Contents\nSection\n', '')
    text = text.replace('This page contains an image.\n', '')
    text = re.sub('Page \w*', '', text)

    #join hyphenated words
    text = re.sub('-\s?', '', text)

    #correct more misspellings. Some misspellings that may be correct parts of
    #other words must include spaces or punctuation that distinguish them (for
    #example, ' twe ' : ' two ' instead of 'twe' : 'two' to avoid correcting
    #'twentyfirst' to 'twontyfirst')
    misspellings = {
        'twontyfirst' : 'twentyfirst',
        'matters die subject' : 'matters on the subject',
        'Oldo, a' : 'Ohio.',
        ' eredit,' : ' credit,',
        'perma> nent' : 'permanent',
        ' twe ' : ' two ',
        'par. ticular' : 'particular',
        'descrip•tion' : 'description',
        '*interesting' : 'interesting',
        'authentic cations' : 'authentic publications',
        'JVatural' : 'Natural',
        ' Principat ' : ' Principal ',
        ' Vative ' : ' Native ',
        'Mgricultural' : 'Agricultural',
        'JMinerals' : 'Minerals',
        'intermisA.\n\nsion' : 'intermission',
        ' impor ' : ' importance. ',
        'ofthe' : 'of the',
        'surroundcd' : 'surrounded',
        'countryand' : 'country and',
        'EuropeThe' : 'Europe. The',
        'FWhat' : 'What',
        'aboufiding' : 'abounding',
        'from.natural' : 'from natural',
        'aggressionThe' : 'aggression. The',
        'rightshaving' : 'rights—having',
        'riverthence' : 'river—thence',
        'butlines' : 'outlines',
        'rivers.This' : 'rivers. This',
        'projecB2\n\ntions' : 'projections',
        'the mouth. La' : 'the mouth.',
        'Missouririses' : 'Missouri rises',
        'dischar, ged' : 'discharged',
        'currentis' : 'current is',
        'itsmouth' : 'its mouth',
        'riversrises' : 'rivers rises',
        'MobileFrom' : 'Mobile. From',
        'jourth' : 'fourth',
        ' canaf ' : ' canal ',
        'PRooUCTIoxs' : 'PRODUCTIONS',
        'prevail. ing' : 'prevailing',
        'cottonThe' : 'cotton. The',
        'cropsThe' : 'crops. The',
        'hewever' : 'however',
        'that C\n\n\nquarter' : 'that quarter',
        'lifesuch' : 'life such',
        'credulousand' : 'credulous and',
        'watthtower' : 'watchtower',
        'enemyThe' : 'enemy. The',
        'prospect.In' : 'prospect. In',
        'bbdies' : 'bodies',
        'custóm' : 'custom',
        'popu\'lation' : 'population',
        'dis\" tance' : 'distance',
        'al\'e' : 'are',
        'agowhose' : 'ago whose',
        'CURíos TIES' : 'CURIOSITIES',
        'soft and#\"' : 'soft and insipid.',
        'tribes E.\n\nof' : 'tribes of',
        'NATIows' : 'NATIONS',
        'Jorests' : 'forests',
        'weapon. i\nThe' : 'weapons. The',
        'szA VE' : 'SLAVE',
        'Pr\"\n\nceeded' : 'Proceeded',
        'standardthat' : 'standard—that',
        'Cherokeewomen' : 'Cherokee women',
        'whitesuitors' : 'white suitors',
        'hus\n\n\n\nMISSISSIPPI. 481\n\nbands' : 'husbands',
        'bat iing' : 'bathing',
        'tribed nsiderably' : 'tribe is considerably',
        'numerous. Q\n\n\n..Animals' : 'numerous.\n\nAnimals'
    }
    for misspelling, correct in misspellings.items():
        text = text.replace(misspelling, correct)

    new_file = open(new_path, 'w', encoding='utf-8')
    new_file.write(text)
    new_file.close()

if __name__ == '__main__':
    main('raw/dana.txt', 'clean/dana.txt')
