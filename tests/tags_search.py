from redgifs import Tags

import time

words = [
    'tits',
    'tIts',
    'ass',
    'asS',
    'milf',
    'horny',
    'hentai',
    'seX',
    'sister',
    'mom',
    'mia khalifa',
    'dick',
    'boobs',
    'cuck',
    'cuckold',
    'virgin',
    'busty',
    'indian',
    'cum',
    'american',
    'japanese',
    'korean',
    'big ass',
    'huge tits',
    'sexy milf',
    'hitomi tanaka',
    'alexa pearl',
    'ava addams',
    'abcdef',
]

def tags_search():
    for word in words:
        try:
            start = time.monotonic()
            found = Tags.search(word)
            print(f'Found "{word}" as "{found}" in {time.monotonic() - start}')
        except Exception as e:
            print(f'[!] Failed: {word}\n{e}')

if __name__ == '__main__':
    tags_search()
