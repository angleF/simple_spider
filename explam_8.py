"""
案例8：爬取豆瓣音乐 存储到MongoDB
"""
from requests import get
from comm import headers
import re
import pymongo
from time import sleep
from lxml import etree


class MongoConnection:

    def __init__(self, ip, port, db, collection):
        self._ip = ip
        self._port = port
        self._db = db
        self._collection = collection

    def __enter__(self):
        """
        上下文管理器入口,打开MongoDB连接
        :return:
        """
        self._mongo_client = pymongo.MongoClient(self._ip, self._port)
        self._collection_client = self._mongo_client[self._db][self._collection]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
          上下文管理器出口，关闭MongoDB连接
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self._mongo_client.close()

    def collection_client(self):
        return self._collection_client


def get_url_music(url, fuc):
    response = get(url, headers=headers)
    if response.status_code == 200:
        etree_html = etree.HTML(response.content)
        music_href_list = etree_html.xpath('//a[@class="nbg"]/@href')
        list_ = []
        for music_href in music_href_list:
            list_.append(get_music_info(music_href))
        fuc(list_)


def get_music_info(url):
    response = get(url, headers=headers)
    if response.status_code == 200:
        etree_html_selector = etree.HTML(response.text)
        response_text = response.text
        # 歌曲名称
        name = etree_html_selector.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
        # 表演者
        author = re.findall('表演者:.*?">(.*?)</a>', response_text, re.S)[0]
        # 流派
        style = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)<br />.*<span class="pl">专辑类型:</span>', response_text,
                           re.S)
        style = style[0].strip() if style else '未知'
        # 发行时间
        publish_time = re.findall('<span class="pl">发行时间:</span>&nbsp;(.*?)<br />', response_text, re.S)
        publish_time = publish_time[0].strip() if publish_time else '未知'
        # 出版者
        publisher = re.findall('<span class="pl">出版者:</span>&nbsp;(.*?)<br />', response_text, re.S)
        publisher = publisher[0].strip() if publisher else '未知'
        # 评价人数
        appraisal_number = etree_html_selector.xpath("//*[@id='interest_sectl']/div/div[2]/div/div[2]/a/span/text()")[0]
        # 评分
        score = etree_html_selector.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()")[0]
        print("".join("<>").join([name, author, style, publish_time, publisher, appraisal_number, score]))
        return {
            "name": name,
            "author": author,
            "style": style,
            "publish_time": publish_time,
            "publisher": publisher,
            "appraisal_number": appraisal_number,
            "score": score
        }


if __name__ == "__main__":
    url_list = ["https://music.douban.com/top250?start={}".format(str(i) for i in range(0, 25, 25))]
    with MongoConnection("127.0.0.1", 27017, "spider", 'musictop') as mongo_connection:
        for url in url_list:
            get_url_music(url, mongo_connection.collection_client().insert_many)
            sleep(2)
