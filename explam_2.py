"""
案例2：爬取酷狗网榜单中酷狗TOP500的信息
"""
from bs4 import BeautifulSoup
import requests
import time
import comm


def get_info(url):
    wb_data = requests.get(url, headers=comm.headers)
    soup = BeautifulSoup(wb_data.text, "lxml")
    ranks = soup.select("span.pc_temp_num")
    titles = soup.select("div.pc_temp_songlist > ul > li >a")
    times = soup.select("span.pc_temp_tips_r > span")
    for rank, title, time in zip(ranks, titles, times):
        data = {
            "rank": rank.get_text().strip(),
            "singer": get_song(title.get_text().split('-'), 0),
            "song": get_song(title.get_text().split('-'), 1),
            "time": time.get_text().strip()
        }
        print("结果：", data)


def get_song(str, index):
    if len(str) > 0 and len(str) > index:
        return str[index]
    else:
        return 'NULL'


if __name__ == "__main__":
    urls = ["http://www.kugou.com/yy/rank/home/{}-8888.html".format(str(i)) for i in range(1, 24)]
    for url in urls:
        get_info(url)
        time.sleep(1)
