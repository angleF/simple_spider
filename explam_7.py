"""
案例7：爬取PEXELS（https://www.pexels.com）网站的图片
    调用搜索PEXELS页面，保存搜索结果图片
"""
from bs4 import BeautifulSoup
import requests
from comm import header_accept

url_path = "https://www.pexels.com/search/"
word = input("请输入你要下载的图片：")
# url_tra = 'http://howtospeak.org:443/api/e2c?user_key=dfcacb6404295f9ed9e430f67b641a8e &notrans=0&text=' + word
#
# english_data = requests.get(url_tra)
# js_data = json.loads(english_data.text)
# english_content = js_data['english']

pexels_url = url_path + word + '/'

response = requests.get(pexels_url)
soup = BeautifulSoup(response.text, "lxml")
imgs = soup.select("article > a > img")
list_image = [img.get("src") for img in imgs]

# 图片下载
out_url = './out_file/img/'
for image in list_image:
    requests_get = requests.get(image, headers=header_accept)
    print(image)
    index = image.index('?')
    up_index = image[: index].rfind("/")
    with open(out_url + image[up_index + 1:index], "wb") as img_io:
        img_io.write(requests_get.content)

