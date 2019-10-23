from bs4 import BeautifulSoup
from bs4 import NavigableString
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import re
import json
import os
import sys
import html
import logging


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



url = "https://pages.trip.com/service-guideline/privacy-policy-en-us.html"
page = requests.get(url)


# page = "E:\\BaiduNetdiskDownload\\apps\\data\\air.com.arcadefest.jigsawpuzzles.html"
# soup = BeautifulSoup(open(filename, encoding="ISO-8859-1"), "lxml")
soup = BeautifulSoup(page.text, "lxml")

for s in soup('script'):
    s.extract()
for s in soup('footer'):
    s.extract()
# footer = soup.div.find_all(class_=re.compile('.*footer.*'))
# header = soup.div.find_all(class_=re.compile('.*header.*'))
# for s in footer:
#     s.extract()
# for s in header:
#     s.extract()

html_nodes = excludeSpecial(str(soup.body))

#寻找标题
result = list()
temp_stack = list()
title_set = set()
#h标题
h_nodes = soup.find_all(re.compile("^h[1-9]$"))

for h_node in h_nodes:
    title_set.add(excludeSpecial(str(h_node)))

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
                print(str(i))
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

        # if son_text.title() == son_text and son_text.isalpha():
        #     title_node = i
        #     flag = True
        #
        # if son_text.upper() == son_text and son_text.isalpha():
        #     title_node = i
        #     flag = True

        if flag and len(excludeSpecial(son_text)) > 0:
            # logging.
            # print(type(title_node))

            title_set.add(excludeSpecial(str(title_node)))
if len(title_set) <= 2:
    # print("haha")
    str_nodes = html_nodes.split('<br/>')

    for ele in str_nodes:
        flag = False
        # print(ele)
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
            # print(only_word(title_str).isalpha())

            flag = True

        if ele.upper() == ele and only_word(ele).isalpha():

            # print(title_str)
            flag = True

        if flag and len(only_word(ele).strip()) > 0:

            # print(ele + str(len(ele)))
            # logging.
            # print(type(title_node))
            title_set.add(excludeSpecial(ele))
temp_set = []
for title in list(title_set):
    temp_set.append(remove_regex(title))

# title_set = set(temp_set)




# # 按照标题分割字符串
if len(title_set) > 0:
    split_str = '|'.join(temp_set)
    # print(split_str)
    paragraph = re.split(r'(' + split_str + ')', html_nodes)

    for word in paragraph:
        ele = dict()
        ele['value'] = word

        if word in title_set:
            if len(temp_stack) > 0:
                result.append(temp_stack)

            check_level = word[0:3]
            if re.match("^<h[1-9]$", check_level) is not None:
                ele['level'] = 10 - int(word[2])
            else:
                ele['level'] = 1
            temp_stack = [ele]
        else:
            if len(temp_stack) > 0:
                ele['level'] = 0
                temp_stack.append(ele)
    result.append(temp_stack)

name = remove_punctuation(url)
# print(name)
# fo = open("./set_6/" + name + ".json", "w")
# fo.write(json.dumps(result))
# fo.close()
