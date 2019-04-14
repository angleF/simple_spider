"""
案例6:爬取七点中文网小说信息，存入excel
    解决自定义反爬字体
"""
from requests import get
from lxml import etree, html
import xlwt
import re
from time import sleep
from fontTools.ttLib import TTFont
from io import BytesIO

all_info_list = []

# 在fontcreator中查看此ttf文件中英文单词与阿拉伯数字的映射关系，写入字典
python_font_relation = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'zero': 0,
    'period': '.'
}

font_ = None


def get_font(urls):
    """
        返回自定义字体组装字典

    :param urls:  字体文件url
    :return:
    """
    dict_ = dict()
    for url in urls:
        response = get(url)
        text = response.content
        tt_font = TTFont(BytesIO(text))
        dict_.update(tt_font.getBestCmap())
    return dict_


def get_encode_font(numberlist, web_font_relation):
    """
     把源代码中的数字信息进行2次解码
     :param numberlist: <list> 需要解码的一维数字信息
     :return:
     """
    data = ''
    # 示例：&#100064;&#100069;&#100071;
    words = numberlist.split(';')
    # 示例：["100064","100069","100071"]
    words_ = [k.strip('&#') for k in words]
    # 通过对应的字体文件获取
    words__ = [web_font_relation.get(int(w)) for w in words_ if w.isdigit()]

    for word in words__:
        data += str(python_font_relation.get(word))

    return data


def get_info(url):
    response = get(url)
    etree_selector = etree.HTML(response.text)
    parent_tag_list_selector = etree_selector.xpath('//ul[@class="all-img-list cf"]/li')
    for tag_selector in parent_tag_list_selector:
        title = tag_selector.xpath('div[2]/h4/a/text()')[0]
        author = tag_selector.xpath('div[2]/p[1]/a[1]/text()')[0]
        style_1 = tag_selector.xpath('div[2]/p[1]/a[2]/text()')[0]
        style_2 = tag_selector.xpath('div[2]/p[1]/a[3]/text()')[0]
        style = style_1 + "·" + style_2
        complete = tag_selector.xpath('div[2]/p[1]/span/text()')[0]
        introduce = tag_selector.xpath('div[2]/p[2]/text()')[0].strip()
        word = tag_selector.xpath('div[2]/p[3]/span/span')[0]

        # 获取字体style文本
        font_style_ = tag_selector.xpath('div[2]/p[3]/span/style/text()')[0]
        # 抓取当前标签对应的woff字体文件
        woff = re.findall("\); src: url\('(.*?)'\) format\('woff'\)", font_style_)[0]
        # 抓取当前标签对应的ttf字体文件
        ttf = re.findall("format\('woff'\), url\('(.*?)'\) format\('truetype'\)", font_style_)[0]
        # 获取节点的html文本
        word__decode = html.tostring(word).decode('utf-8')
        text = re.findall('<span class=".*">(.*)</span>', word__decode)[0]

        global font_
        if not font_:
            font_ = get_font([woff, ttf])

        word = get_encode_font(text, font_)

        info_list = [title, author, style, complete, introduce, word + "万字"]
        all_info_list.append(info_list)
    sleep(1)


if __name__ == '__main__':
    url_list = ["http://a.qidian.com/?page={}".format(str(i)) for i in range(1, 2)]
    for url in url_list:
        get_info(url)

    # 存储
    # 定义excel表头
    header = ["title", "author", "style", "complete", "introduce", "word"]

    # 创建工作簿
    xlwt_workbook = xlwt.Workbook(encoding="utf-8")
    # 创建sheet表
    sheet = xlwt_workbook.add_sheet("起点中文小说信息")
    for h in range(len(header)):
        sheet.write(0, h, header[h])

    i = 1
    for all_info in all_info_list:
        j = 0
        for info in all_info:
            sheet.write(i, j, info)
            j += 1
        i += 1
    xlwt_workbook.save('./out_file/起点小说.xls')
