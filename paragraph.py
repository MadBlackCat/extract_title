from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import UnicodeDammit
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import re
import json
import os
import sys
import html
import logging
import csv


def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


def only_word(line):
    rule = re.compile(r"[^a-zA-Z\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


def remove_regex(string):
    regex = ['(', ')', '?', '[', ']', '{', '}', '|', '.', '&', '*', '$']
    for c in regex:
        string = string.replace(c, '\\' + c)

    return string


def surrounded_by_strings(tag):
    return (isinstance(tag.next_element, NavigableString)
            and isinstance(tag.previous_element, NavigableString))


def excludeSpecial(string):
    pattern = "\t|\r|\n"
    string = re.sub(pattern, "", string)
    return html.unescape(string)


#Main
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='main.log',
                    filemode='w')



urls = []
with open('F:\\Documents\\Project\\Html_analysis\\package\\url_2.txt') as rfile:
    for f in rfile:
        # f = f.replace("\"", "")
        url = f.strip()
        urls.append(url)

# path = "F:\\Documents\\Project\\analysis_html\\package\\url.txt"
# for root, dirs, files in os.walk(path):
#     for file in files:
#         name = file.replace('.html', '')
#         filename = root + '\\' + file
k = 0
for url in urls:

    page = requests.get(url)


    # page = "E:\\BaiduNetdiskDownload\\apps\\data\\air.com.arcadefest.jigsawpuzzles.html"
    # soup = BeautifulSoup(open(filename, encoding="ISO-8859-1"), "lxml")
    soup = BeautifulSoup(page.text, "lxml")


    html_nodes = soup.body
    p_tag = html_nodes.find_all('p')

    result = []
    j = 0
    for i in p_tag:

        s = i.get_text().strip().replace('<p>', '').replace('<\p>', '').replace('\n', '')

        result.append([j, 1, s])
        j = j+1

    name = k

    with open('F:\\Documents\\Project\\Html_analysis\\'+str(k)+'.tsv', 'w+', newline='', encoding="utf-8") as tsvfile:
        # fieldnames = ['id', 'sentiment', 'reviews']
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerows(result)
    k = k + 1

