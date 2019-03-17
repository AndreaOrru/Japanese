#!/usr/bin/env python3

import argparse
import mechanicalsoup
import re
from getpass import getpass
from time import sleep


parser = argparse.ArgumentParser('koohii', description='Grab the best stories from Kanji Koohii.')
required = parser.add_argument_group('required arguments')
required.add_argument('-i', metavar='INPUT',  required=True, help='TSV file containing the kanji info')
required.add_argument('-o', metavar='OUTPUT', required=True, help='TSV file where to export the stories')

parser.add_argument('-n', metavar='STORIES', default=5, type=int, help='number of stories per kanji (default 5)')
args = parser.parse_args()

username =   input('Koohii username: ')
password = getpass('Koohii password: ')

browser = mechanicalsoup.Browser()
login_page = browser.get('http://kanji.koohii.com/login')
login_form = login_page.soup.select('form')[0]
login_form.select('#username')[0]['value'] = username
login_form.select('#password')[0]['value'] = password
browser.submit(login_form, login_page.url)

rtk    = open(args.i).readlines()
output = open(args.o, 'w')

for line in rtk:
    line = line.split('\t')

    kanji   = line[1]
    number  = line[3]
    keyword = line[6]
    print('{:<4}  {}  {}'.format(number, kanji, keyword))

    page = browser.get('http://kanji.koohii.com/study/kanji/{}'.format(kanji))
    stories = page.soup.select('#sharedstories-fav .story')[:args.n]
    stories = [''.join(map(str, x.contents)) for x in stories]
    stories = [re.sub(r'<a href="/study/kanji/(.*?)">(.*?)</a>.*?</span>\)',
                      r'<a href="https://kanji.koohii.com/study/kanji/\1">\2</a>',
                      x) for x in stories]
    stories = [re.sub(r'\n|\t', r' ', x) for x in stories]
    stories = (stories + ['']*args.n)[:args.n]

    outputline = '{}\t{}\t{}\t{}\n'.format(number, kanji, keyword, '\t'.join(stories))
    if outputline.count('"') % 2:
        outputline = outputline.replace('"', '', 1)
    output.write(outputline)
    sleep(2)

output.close()
