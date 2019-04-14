"""
案例4:使用正则表达式爬取糗事百科网的段子信息,并把爬取的数据存储在本地文件中
1:爬取的内容为棋事百科网“文字”专题中的信息

"""
import requests
import re
from comm import headers

info_list = []


def judgment_sex(class_name):
    return '女' if class_name == 'womenIcon' else '男'


def get_info(url):
    response = requests.get(url)
    content_text = response.text
    # print(content_text)
    ids = re.findall('<h2>(.*?)</h2>', content_text, re.S)
    levels = re.findall('<div class="articleGender \D+Icon">(.*?)</div>', content_text, re.S)
    sexs = re.findall('<div class="articleGender (.*?)>', content_text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', content_text, re.S)
    laughs = re.findall('<span class="stats-vote"><i class="number">(\d+)</i>', content_text, re.S)
    comments = re.findall('<i class="number">(\d+)</i> 评论', content_text, re.S)
    for id, level, sex, content, laugh, comment in zip(ids, levels, sexs, contents, laughs, comments):
        info = {
            "id": id,
            "level": level,
            "sex": judgment_sex(sex),
            "content": content,
            "laugh": laugh,
            "comment": comment
        }
        info_list.append(info)


if __name__ == '__main__':
    urls = ["http://www.qiushibaike.com/text/page/{}/".format(str(i)) for i in range(1, 2)]
    for url in urls:
        get_info(url)

    with open("./qiushi.txt", "a+", encoding="utf-8") as text_io:
        for info in info_list:
            try:
                text_io.write(info["id"] + '\n')
                text_io.write(info["level"] + '\n')
                text_io.write(info["sex"] + '\n')
                text_io.write(info["content"] + '\n')
                text_io.write(info["laugh"] + '\n')
                text_io.write(info["comment"] + '\n')
            except Exception as ex:
                print("异常：", ex)
