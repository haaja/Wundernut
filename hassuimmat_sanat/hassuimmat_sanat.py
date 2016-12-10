#!/usr/bin/env python

"""
Koodauspähkinä: Hassuimmat sanat

Monet ulkomaalaiset pitävät suomen kieltä hassun kuuloisena vokaalien
runsauden vuoksi. Erityisen hassulta kuulostaa, jos vokaaleja on monta
peräkkäin, kuten kuuluisassa sanassa "hääyöaie", jossa on seitsemän
peräkkäistä vokaalia.

Kehitämme tieteellisen tavan sanojen hassuuden pisteytykseen.

Jokainen vokaaliketju saa n×2n pistettä, jossa n on vokaalien määrä
ketjussa. Sanan vokaaliketjujen saamat pisteet lasketaan yhteen,
jolloin saadaan sanan hassuuspisteet.

Esimerkiksi sana "koira" saa 10 pistettä, koska "koira" sisältää
vokaaliketjut "oi" (2×22 = 8 pistettä) ja "a" (1×21 = 2 pistettä),
ja 8 + 2 = 10.

Sana "hääyöaie" saa 896 pistettä, koska vokaaliketju "ääyöaie"
saa (7×27 = 896 pistettä).

Jotta hauskuus ei loppuisi kesken, käytämme esimerkkiteoksena
Volter Kilven romaania Alastalon salissa, jota pidetään suomalaisen
kirjallisuuden mestarinäytteenä hassuuden saralla.

Mikä on Alastalon salissa -romaanin hassuin sana, tai hassuimmat
sanat, jos useampi sana saa korkeimmat hassuuspisteet?

Löydät Alastalon salissa -kirjan sähköisessä muodossa täältä.


The solution uses epub library by Florian Strzelecki.
"""


import epub
import math

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


def count_funniness(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'ä', 'ö']
    counter = 0
    streaks = []

    for char in word.lower():
        if char in vowels:
            counter += 1
        else:
            streaks.append(counter)
            counter = 0

    # If the word ends on vowel
    if counter != 0:
        streaks.append(counter)
        counter = 0

    sum = 0
    for streak in streaks:
        sum += streak * int(math.pow(2, streak))

    return sum


def solve(book):
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

    funny_words = []
    for item in book.opf.manifest.values():
        if item.identifier in valid_identifiers:
            data = book.read_item(item)
            data = strip_html(data.decode())

            for word in data.split():
                funniness = count_funniness(word)
                funny_words.append({"word": word, "funniness": funniness})

    return sorted(funny_words, key=lambda key: key['funniness'], reverse=True)


if __name__ == '__main__':

    # Let's make sure we count funniness correctly
    assert count_funniness('hääyöaie') == 896
    assert count_funniness('koira') == 10

    result = solve('../ebook/Alastalon-Salissa.epub')

    # Let's print top10
    for i in range(0, 10):
        print(result[i])
