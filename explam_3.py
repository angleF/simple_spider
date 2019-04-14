"""
案例3：使用正则表达式爬取“斗破苍穹”小说，并存入txt文件
"""
import requests
import re
import time
from comm import headers

text_io = open("./out_file/doupo.txt", "a+",encoding="utf-8")


def get_info(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        decode_content = response.content.decode("utf-8")
        title = re.findall('<meta name="keywords" content="(.*?)">',decode_content , re.S)
        text_io.write(title[0] + '\n')
        contents = re.findall('<p>(.*?)</p>', decode_content, re.S)
        for content in contents:
            text_io.write(content + '\n')
    else:
        print("响应码：", response.status_code)
    response.close()


if __name__ == "__main__":
    urls = ["http://doupoxs.com/doupocangqiong/{}.html".format(i) for i in range(1, 5)]
    for url in urls:
        get_info(url)
        time.sleep(2)
text_io.close()
