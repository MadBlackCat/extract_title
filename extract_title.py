from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Comment
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import re
import json
import os
import sys
import html
import logging
import os

def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('', line)
    return line


def only_word(string):
    rule = re.compile(r"[^a-zA-Z\u4e00-\u9fa5]")
    string = rule.sub(' ', string)
    string = re.sub('\s+', ' ', string)
    return string


def remove_regex(string):
    regex = ['(', ')', '?', '[', ']', '{', '}', '|', '.', '&', '*', '$']
    for c in regex:
        string = string.replace(c, '\\' + c)

    return string


def surrounded_by_strings(tag):
    return (isinstance(tag.next_element, NavigableString)
            and isinstance(tag.previous_element, NavigableString))


def excludeSpecial(string):
    return re.sub('\s+', ' ', string)


#Main
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='main.log',
                    filemode='w')
urls = []
urls = os.listdir("./")


for url in urls:
    # url_name = url.replace('.txt', '.html')
    try:

        soup = BeautifulSoup(open(url, "rb"), "lxml")
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        [x.extract() for x in soup.find_all('footer')]
        [x.extract() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]


        html_nodes = excludeSpecial(str(soup.body))

        #寻找标题
        result = list()
        temp_stack = list()
        title_set = set()
        #h标题
        h_nodes = soup.find_all(re.compile("^h[1-9]$"))

        # for h_node in h_nodes:
        #     title_set.add(excludeSpecial(str(h_node)))
        for h_node in h_nodes:
            title_set.add(excludeSpecial('  '.join(h_node.stripped_strings)))

        maybe_title_tag = ['strong', 'b', 'em', 'i']

        stop_words = set(stopwords.words('english'))

        for tag in maybe_title_tag:
            tag_nodes = soup.find_all(tag)


            for i in tag_nodes:
                flag = False

                son_text = i.text.strip()

                try:
                    baba_p_text = i.find_parent("p").text.strip()
                except:
                    baba_p_text = ""

                try:
                    pre_node = i.previous_sibling
                    if pre_node is None or pre_node == '\n':
                        title_node = i
                        flag = True
                    if not only_word(str(pre_node)).strip().isalpha():
                        # print(str(i))
                        title_node = i
                        flag = True
                except:
                    flag = True

                try:
                    baba_div_text = i.find_parent("div").text.strip()
                except:
                    baba_div_text = ""

                try:
                    brother_node = i.next_sibling
                    if brother_node == '\n':
                        flag = True
                        title_node = i
                except:
                    brother_node = ""

                if brother_node is not None:

                    if brother_node.name == "br":

                        flag = True
                        title_node = i


                if son_text == baba_p_text:
                    title_node = i.find_parent("p")
                    flag = True

                if son_text == baba_div_text:
                    title_node = i.find_parent("div")
                    flag = True

                word_num = son_text.count(' ')

                if word_num > 10:
                    flag = False

                try:
                    child = i.contents[0].name
                    # print(child)
                    if child in maybe_title_tag:
                        # print(child)
                        flag = False
                except:

                    pass
                if flag and len(excludeSpecial(son_text)) > 0:

                    title_set.add(excludeSpecial(' '.join(title_node.stripped_strings)))
        if len(title_set) <= 2:
            # print("haha")
            str_nodes = html_nodes.split('<br/>')
            flag = False
            for ele in str_nodes:
                flag = False
                word_num = ele.count(' ')
                word_tokens = word_tokenize(ele)
                filtered_sentence = [w for w in word_tokens if not w in stop_words]

                filtered_sentence = []

                for w in word_tokens:
                    if w not in stop_words:
                        filtered_sentence.append(w)
                title_str = (' '.join(filtered_sentence)).strip()
                if word_num > 10:
                    flag = False

                if title_str == title_str.title() and only_word(title_str).isalpha():
                    flag = True

                if ele.title() == ele and only_word(ele).isalpha():
                    flag = True

                if ele.upper() == ele and only_word(ele).isalpha():
                    # print(ele)

                    flag = True
                if flag and len(only_word(ele).strip()) > 0:
                    # print(ele + str(len(ele)))
                    # logging.
                    # print(type(title_node))
                    title_set.add(excludeSpecial(ele))
        title_list = []
        for title in list(title_set):
            if (len(only_word(title)) > 15) and (len(only_word(title)) < 100):
                title_list.append(only_word(title))

        # title_list = '\n'.join(title_list)
        with open('./no_title.txt', "a", encoding="utf8") as f:
            # print("ok")
            if len(title_list) < 3:
                f.write(url+'\n')
    except:
        print(url)


#
