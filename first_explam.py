import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/69.0.3497.100 Safari/537.36"
}
response = requests.get("http://bj.xiaozhu.com",headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())
