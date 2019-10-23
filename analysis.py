from bs4 import BeautifulSoup
import requests
import re
import json
import os
import sys
import html


def isTitle(ndoe):
    pass


path = "E:\\BaiduNetdiskDownload\\apps\\data"
for root, dirs, files in os.walk(path):
    for file in files:
        name = file.replace('.html', '')
        filename = root + '\\' + file
        # filename = root + '\\' + "air.com.arcadefest.jigsawpuzzles.html"

        # html=requests.get("https://www.google.com/intl/en/chrome/privacy/")
        bsObj = BeautifulSoup(open(filename, encoding="ISO-8859-1"), "lxml")
        bsObj = html.unescape(bsObj)
        for s in bsObj('script'):
            s.extract()
        if (1):

            # 识别标题标签集合，用来判断标签是否为标题
            tag_set = set()
            temp_set = bsObj.find_all(re.compile("^h[1-9]$"))
            for tag in temp_set:
                tag_set.add(tag.name)

            # 删除标签
            # bsObj.option.decompose()
            try:
                bsObj.footer.decompose()
            except:
                pass
            try:
                bsObj.script.decompose()
            except:
                pass

            # 遍历html

            html_root = bsObj.find(re.compile("^h[1-9]$"))

            # temp_list
            temp = {'result': [str(html_root)], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}

            try:
                all_nodes = html_root.find_all_next()
                cur_temp_stack = "result"
                for node in all_nodes:
                    del node['class']
                    del node['id']
                    del node['value']
                    del node['href']
                    del node['disabled']
                    del node['hidden']
                    del node['selected']
                    del node['for']
                    del node['src']
                    del node['name']
                    del node['style']
                    del node['title']
                    del node['target']
                    node.string = node.text.replace('\n', '')
                    # 如果标签不在tag_set里面，把元素文字部分加入result,否则嵌套加入
                    # 变量存储前一个栈的标签，判断与当前标签？？？
                    if node.name not in tag_set:
                        if len(node.text.strip()) > 0:
                            temp[cur_temp_stack].append(str(node))
                    else:
                        # 清除temp栈，并把内容给result
                        if cur_temp_stack != "result":
                            temp['result'].append(temp[cur_temp_stack])
                            temp[cur_temp_stack] = []
                        # 更改当前栈
                        cur_temp_stack = node.name
                        temp[cur_temp_stack].append(str(node))
                        pass
                for ele in temp:
                    if (len(temp[ele]) > 0) and (ele != "result"):
                        temp['result'].append(temp[ele])
                # 写入文件
                fo = open("./set/" + name + ".json", "w")
                fo.write(json.dumps(temp['result']))
                fo.close()
            except:
                print("没有h标签，文件名为 " + file)
        # except:
        #     print("不知道哪个鬼地方发生了错误，文件名为 " + file)
