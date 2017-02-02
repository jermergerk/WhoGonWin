#!/usr/bin/env python2.7

import urllib2, json, re, scrub, collections
from bs4 import BeautifulSoup

URL = 'https://www.grammy.com/nominees'


class NomineeParser(object):
    def __init__(self):
        self.output = collections.defaultdict(list)
        self.count = 0

    def _get_nominee_details(self, nominee_html):
        artist = nominee_title = None
        for child in nominee_html.children:
            child_value = unicode(child.string)
            child = unicode(child)
            if 'nominee-title' in child:
                nominee_title = child_value
            if 'nominee-artist' in child:
                if child_value:
                    artist = scrub.replace_parentheses(child_value)
            if 'nominee-description' in child:
                if not artist:
                    found = re.search('\((.*)\)', child_value)
                    if found:
                        artist = found.group(1)
        return artist, nominee_title

    def get_html_elements(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        view_content = soup.find_all(True, {'class': ['title',
                                                      'nominee-details']})
        return view_content

    def parse(self, html, output_format='csv'):
        #  output format can be csv or json
        title = None
        html_elements = self.get_html_elements(html)
        for html_part in html_elements:
            if 'class="title"' in unicode(html_part):
                title = unicode(html_part.string)
                self.count += 1 
            else:
                artist, nominee_title = self._get_nominee_details(html_part)
                output_dict = {'nominee_title': nominee_title,
                               'nominee_artist': artist}
                self.output[title].append(output_dict)
                nominee_title = artist = None
        self._write_output(output_format)

    def _write_output(self, output_format):
        if output_format == 'json':
            with open('current_grammy_nominations.json', 'w') as out_fh:
                json.dump(self.output, out_fh)
        if output_format == 'csv':
            with open('current_grammy_nominations.csv', 'w') as out_fh:
                for key, nominees in self.output.iteritems():
                    for nominee in nominees:
                        artist = nominee['nominee_artist']
                        title = nominee['nominee_title']
                        row = (key,
                               artist if artist else 'none',
                               title if title else 'none')
                        out_fh.write(','.join(row).encode('utf-8') + '\n')

if __name__ == '__main__':
    parser = NomineeParser()
    html = urllib2.urlopen(URL).read()
    #html = open('grammys_html')
    parser.parse(html, 'json')
    print parser.count
