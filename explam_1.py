from bs4 import BeautifulSoup
import requests
import time
import comm

"""
    案例1：爬取小猪短租网北京地区短租房信息
"""


def judgment_sex(class_name):
    return '女' if class_name == ['member_ico1'] else '男'


def get_links(url):
    """
        获取详细页面URL
    :param url:
    :return:
    """
    wb_data = requests.get(url, headers=comm.headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    # 获取a标签中的链接
    links = soup.select('#page_list > ul > li > a')
    for link in links:
        link_href = link.get("href")
        get_info(link_href)


def get_info(url):
    """
        抓取详细子页面中的数据
    :param url:
    :return:
    """
    wb_data = requests.get(url, headers=comm.headers)
    soup = BeautifulSoup(wb_data.text, "lxml")
    # 标题
    titles = soup.select('div.pho_info > h4')
    # 地址
    addresss = soup.select("span.pr5")
    # 价格
    prices = soup.select("#pricePart > div.day_l > span")
    # 图片
    imgs = soup.select("#floatRightBox > div.js_box.clearfix > div.member_pic > a > img")
    # 名称
    names = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a")
    # 性别
    sexs = soup.select("#floatRightBox > div.js_box.clearfix > div.member_pic > div")

    for title, address, price, img, name, sex in zip(titles, addresss, prices, imgs, names, sexs):
        data = {
            'title': title.get_text().strip(),
            'address': address.get_text().strip(),
            'price': price.get_text(),
            'img': img.get("src"),
            'name': name.get_text().strip(),
            'sex': judgment_sex(sex.get("class"))
        }
        print("结果：", data)


if __name__ == '__main__':
    url_def = "http://bj.xiaozhu.com/search-duanzufang-p{}-0/"
    for i in range(1, 14):
        url = url_def.format(i)
        get_links(url)
        time.sleep(2)
