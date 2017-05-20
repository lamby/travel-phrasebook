#!/usr/bin/env python3

import re
import sys
import requests
import collections



class Phrasebook(collections.OrderedDict):
    re_phrase = re.compile(r'^; (?P<phrase>.+)\s*: (?P<translation>.+) \(\'\'(?P<pronunciation>.*)\'\'+\)')

    def __init__(self, language):
        self.session = requests.Session()
        self.language = language

    def download(self):
        r = self.session.get(
            'http://wikitravel.org/wiki/en/api.php',
            params={
                'prop': 'revisions',
                'action': 'query',
                'format': 'json',
                'titles': "{}_phrasebook".format(self.language),
                'rvprop': 'content',
            }
        )
        r.raise_for_status()

        revisions = list(r.json()['query']['pages'].values())[0]['revisions']

        for x in revisions[0]['*'].splitlines():
            m = self.re_phrase.match(x)

            if m is None:
                continue

            self[m.group('phrase').strip()] = (
                m.group('translation'),
                m.group('pronunciation'),
            )


def main(language, word):
    phrasebook = Phrasebook(language)
    phrasebook.download()

    #print(phrasebook)
    for x, y in phrasebook.items():
        break
        print()
        print(repr(x))
        print(y[0])
        print(y[1])

    print(phrasebook[word][0])
    print(phrasebook[word][1])


if __name__ == '__main__':
    try:
        sys.exit(main(*sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit(2)
