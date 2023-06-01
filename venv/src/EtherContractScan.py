import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "PostmanRuntime/7.31.3", "Accept": "*/*", "Accept-Encoding": "gpt"}
for i in range(10000):
    url = "https://etherscan.io/txs?ps=50&p=" + str(i + 1)  # 要访问的网站 URL
    # 发送 GET 请求并获取网站内容
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 示例分析：获取标题和所有链接
    # title = soup.title.text
    print(i)

    trHtmls = soup.find_all(name='tr')
    s = ""
    for trHtml in trHtmls:
        needPrint = False
        for tdhtml in trHtml.children:
            s += tdhtml.text
            if s.__contains__("Create"):
                needPrint = True
        if needPrint:
            s = s.replace("\n", " ")
            print(s)
        s = ""
