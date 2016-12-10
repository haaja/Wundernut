#!/usr/bin/env python

"""
Tällä kertaa tutkimme muhkeita sanapareja.

Sanaparin muhkeus määritellään seuraavasti: muhkeus on yhtä kuin
sanaparin sisältämien uniikkien kirjainten määrä. Kirjaimiksi
lasketaan seuraavat merkit: {a, b, c, d, e, f, g, h, i, j, k, l, m,
n, o, p, q, r, s, t, u, v, w, x, y, z, å, ä, ö}. Isot ja pienet
kirjaimet lasketaan samaksi. Esimerkiksi sanaparin {"Upea", "Kapteeni"}
muhkeus on 8, koska sanapari sisältää kirjaimet {a, e, i, k, n, p, t, u}.

Kysymys kuuluu: mikä on Alastalon salissa -kirjan muhkein sanapari, tai
muhkeimmat sanaparit, jos useampi pari saa korkeimmat muhkeuspisteet?
Sanojen ei tarvitse olla peräkkäin, vaan tarkoitus on löytää koko kirjan
kaikista sanoista ne kaksi sanaa, jotka muodostavat muhkeimman parin.

Löydät Alastalon salissa -kirjan sähköisessä muodossa täältä.

Vinkkejä

Tämänkertainen pähkinä on paljon vaikeampi kuin edellinen. Puhtaasti
brute forcella tämä ei onnistu.

Säännöt

Osallistua saa millä ohjelmointikielellä tahansa.


The solution uses epub library by Florian Strzelecki.
"""


import epub
import re

from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)


def strip_html(html):
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_data()


def get_words_from_book(book):
    """Returns words as a set of tuples

    Returns tuple in form of (word, uniq_chars, len(uniq_chars))
    """
    remover = re.compile('[\W_]', re.UNICODE)
    words = set()
    # Only take words from the actual chapters of the book.
    valid_identifiers = ['content-423849-2172623-luku_1',
                         'content-423849-2172623-luku_2',
                         'content-423849-2172623-luku_3',
                         'content-423849-2172623-luku_4',
                         'content-423849-2172623-luku_5',
                         'content-423849-2172623-luku_6',
                         'content-423849-2172623-luku_7',
                         'content-423849-2172623-luku_8',
                         'content-423849-2172623-luku_9',
                         'content-423849-2172623-luku_10',
                         'content-423849-2172623-luku_11',
                         'content-423849-2172623-luku_12',
                         'content-423849-2172623-luku_13',
                         'content-423849-2172623-luku_14',
                         'content-423849-2172623-luku_15',
                         'content-423849-2172623-luku_16',
                         'content-423849-2172623-luku_17',
                         'content-423849-2172623-luku_19',
                         'content-423849-2172623-luku_19b',
                         'content-423849-2172623-luku_20',
                         'content-423849-2172623-luku_21',
                         'content-423849-2172623-luku_lopputekstit']

    book = epub.open_epub(book, 'r')
    for item in book.opf.manifest.values():
        if item.identifier in valid_identifiers:
            data = book.read_item(item)
            data = strip_html(data.decode())
            for word in data.split():
                word = remover.sub('', word.lower()).strip()
                uniq_chars = get_uniq_chars(word)
                muhkeus = count_muhkeus(uniq_chars)
                words.add((word, uniq_chars,  muhkeus))

    return words


def get_uniq_chars(word):
    return ''.join(set(word))


def count_muhkeus(word):
    return len(word)


def solve(ebook):
    muhkein = set()
    pairs = set()
    top = 0

    words = list(get_words_from_book(ebook))
    words.sort(key=lambda key: key[2], reverse=True)

    for w1 in words:
        # Since the array is sorted by "muhkeus" there's no point going
        # further if top is longer than twice the lenght of muhkeus of
        # current word.
        if top > len(w1[1]) * 2:
            break
        for w2 in words:
            # lets not take two same words as a pair
            if w1[0] == w2[0]:
                continue
            if top > (len(w1[1]) + len(w2[1])):
                break

            muhkeus = count_muhkeus(get_uniq_chars(w1[1] + w2[1]))
            if muhkeus > top:
                if ((w1[0], w2[0]) not in pairs) and \
                   ((w2[0], w1[0]) not in pairs):
                    # lets clear leaderboard
                    pairs = set()
                    muhkein = set()
                    top = muhkeus
                    muhkein.add((w1[0], w2[0], muhkeus))
                    pairs.add((w1[0], w2[0]))
            elif muhkeus == top:
                if ((w1[0], w2[0]) not in pairs) and \
                   ((w2[0], w1[0]) not in pairs):
                    muhkein.add((w1[0], w2[0], muhkeus))
                    pairs.add((w1[0], w2[0]))

    return sorted(muhkein, key=lambda key: key[2], reverse=True)


if __name__ == '__main__':

    assert count_muhkeus(get_uniq_chars('kapteeni')) == 7
    assert count_muhkeus(get_uniq_chars('upeakapteeni')) == 8

    ebook = '../ebook/Alastalon-Salissa.epub'

    # Sort of a brute force solution but it gets the job done.
    result = list(solve(ebook))
    print("Found {0} pairs.".format(len(result)))
    for word in result:
        print(word)
