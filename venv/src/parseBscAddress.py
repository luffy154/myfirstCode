import requests
from bs4 import BeautifulSoup

with open('bscAddress', 'a') as file:
    for i in range(118, 400):
        url = "https://bscscan.com/accounts/" + str(i + 1)  # 要访问的网站 URL
        headers = {"User-Agent": "PostmanRuntime/7.31.3", "Accept": "*/*", "Accept-Encoding": "gpt"}
        # 发送 GET 请求并获取网站内容
        response = requests.get(url, headers=headers)

        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 示例分析：获取标题和所有链接
        title = soup.title.text
        links = soup.find_all('a')

        # 输出结果

        for link in links:
            address = link.text
            if address is not None and address.startswith("0x"):
                file.write(f"{address}\n")
                print(address)
