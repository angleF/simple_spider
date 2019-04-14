"""
案例5：使用lxml xpath语法解析爬取豆瓣读书Top250的信息存入csv文件中
"""
import csv
from comm import headers
import requests
from lxml import etree

with open("./out_file/doubanbook.csv", "wt", newline="", encoding="utf-8-sig") as csv_io:
    csv_writer = csv.writer(csv_io)
    # 写入标题
    csv_writer.writerow(["name", "url", "author", "publisher", "date", "price", "rate", "comment"])

    # 构造url
    url_list = ["https://book.douban.com/top250?start={}".format(str(i)) for i in range(0, 250, 25)]

    for url in url_list:
        response = requests.get(url, headers=headers)
        etree_selector = etree.HTML(response.text)
        book_tag_list = etree_selector.xpath('//tr[@class="item"]')
        for book_tag in book_tag_list:
            name = book_tag.xpath("td/div/a/@title")[0]
            url = book_tag.xpath("td/div/a/@href")[0]
            book_info = book_tag.xpath("td/p/text()")[0]
            book_info_list = book_info.split("/")
            author = book_info_list[0]
            publisher = book_info_list[-3]
            date = book_info_list[-2]
            price = book_info_list[-1]

            rate = book_tag.xpath("td/div/span[2]/text()")[0]
            comments = book_tag.xpath("td/p/span/text()")
            comment = comments[0] if len(comments) != 0 else 'NULL'

            csv_writer.writerow([name, url, author, publisher, date, price, rate, comment])
