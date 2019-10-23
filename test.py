import re


def only_word(string):
    rule = re.compile(r"[^a-zA-Z\u4e00-\u9fa5]")
    string = rule.sub(' ', string)
    string = re.sub('\s+', ' ', string)
    return string


text = "32423.防守打法 fsdfsd fsdf"
print(only_word(text))
