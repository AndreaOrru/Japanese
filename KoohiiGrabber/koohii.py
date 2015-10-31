#!/usr/bin/env python
import getpass

USERNAME = ''
PASSWORD = ''

if(USERNAME == '')
    USERNAME = raw_input("Enter Koohii username")
if(PASSWORD == '')
    PASSWORD = getpass.getpass("Enter Koohii password")


INPUT  = 'rtk.tsv'     # https://docs.google.com/spreadsheet/ccc?key=0AqYInAMvWw-2dGdzUV9uUXpaLXNhYy1Qb3Z0NVRidnc#gid=0
OUTPUT = 'stories.txt'

import re
import mechanize
from time import sleep

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9')]

br.open('http://kanji.koohii.com/login')
br.select_form(nr = 0)
br.form['username'] = USERNAME
br.form['password'] = PASSWORD
br.submit()

f   = open(OUTPUT, 'w')
rtk = open(INPUT , 'r').readlines()
for line in rtk:
    line = line.split('\t')
    kanji   = line[1]
    number  = line[3]
    keyword = line[6]
    print(number)

    html = br.open('http://kanji.koohii.com/study/kanji/' + kanji).read()
    html = html[html.index('<div id="sharedstories-fav">'):]

    stories = re.findall(r'<div class="bookstyle">(.*?)</div>', html, re.DOTALL)[:5]
    stories = [x.replace('\n', ' ') for x in stories]
    stories = [re.sub(r'<a href="/study/kanji/(.*?)">(.*?)</a>.*?</span>', r'<a href="http://kanji.koohii.com/study/kanji/\1">\2</a>', x) for x in stories]
    while len(stories) < 5:
        stories.append('')

    f.write('{}\t{}\t{}\t{}\n'.format(number, kanji, keyword, '\t'.join(stories)))
    sleep(2)

f.close()
