import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 定义目标网页的URL
url = "https://etherscan.io/"
headers = {"User-Agent": "PostmanRuntime/7.31.3", "Accept": "*/*", "Accept-Encoding": "gpt"}
# 发送HTTP GET请求获取网页内容
response = requests.get(url, headers=headers)

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')

# 提取网页的标题
title = soup.title.text
print("网页标题:", title)

# 提取网页中的链接
links = soup.find_all('a')
print("链接列表:")
# 遍历链接列表并打印
for link in links:
    href = link.get('href')
    if href.startswith('http') or href.startswith('https'):
        print(href)
    else:
        absolute_url = urljoin(url, href)
        print(absolute_url)
