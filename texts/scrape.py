import urllib.request

def scrape_loc(base_url, destination_folder, begin, end):
    '''Scrapes a series of .jpg images from a specified work in the Library of
        Congress American Memory historical collections and saves them in a
        folder.

    base_url - if jpg is located at
        https://memory.loc.gov/award/icufaw/bbf0054/0001v.jpg, then base_url
        should be 'https://memory.loc.gov/award/icufaw/bbf0054/'
    destination_folder - folder (for example, 'raw/filson') in which .jpg files
        will be saved as 1.jpg, 2.jpg, etc.
    begin - int index of first image to scrape (usually 1)
    end - int index of last image to scrape
    '''

    for i in range(begin, end+1):
        urllib.request.urlretrieve('{}{:04d}v.jpg'.format(base_url, i),
            '{}/{:04d}.jpg'.format(destination_folder, i))
