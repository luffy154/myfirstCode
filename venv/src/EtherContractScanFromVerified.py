import requests
from bs4 import BeautifulSoup
import json

headers = {"User-Agent": "PostmanRuntime/7.31.3", "Accept": "*/*", "Accept-Encoding": "gpt"}
contract_address_list = []
authCode = "cfb32d7272c853a33da945d3e5c102641685285465940938643"
for i in range(6):
    url = f"https://etherscan.io/contractsVerified/{i + 1}?ps=100"  # 要访问的网站 URL
    # 发送 GET 请求并获取网站内容
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 示例分析：获取标题和所有链接
    # title = soup.title.text
    print(i)

    trHtmls = soup.find_all(name='tr')
    s = ""
    for trHtml in trHtmls:
        needPrint = True
        address = ""
        for index, tdhtml in enumerate(trHtml.children):
            if tdhtml.name is None:
                continue
            if "th" == tdhtml.name:
                needPrint = False
                break
            if index == 0:
                addressHtml = tdhtml.find('a', attrs={'class': 'me-1', 'data-bs-trigger': 'hover',
                                                      'data-bs-toggle': 'tooltip'})
                address = addressHtml["title"]
                s += address + "\t"
            elif index == 5:
                if int(tdhtml.text) < 100:
                    needPrint = False
                else:
                    contract_address_list.append(address)
                s += tdhtml.text + "\t"
            else:
                s += tdhtml.text + "\t"
        if needPrint:
            s = s.replace("\n", "")
            # print(s)
        s = ""

# print(contract_address_list)
headers = {"User-Agent": "PostmanRuntime/7.31.3",
           "Accept": "*/*",
           "Accept-Encoding": "gzip, deflate, br",
           "X-Auth": f"{authCode}"}
for contractAddress in contract_address_list:
    url = f"https://api.hserpcvice.com/v1api/v2/tokens/contract?token_id={contractAddress}-eth&type=token&user_address="  # 要访问的网站 URL
    # 发送 GET 请求并获取网站内容
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if data['data']['token_contract']['contract_data']['risk_score'] <= 60:
        riskData = data['data']['token_contract']['contract_data']
        print(
            f"{contractAddress}*{riskData.get('risk_score')}*{riskData.get('owner')}*{riskData.get('cannot_sell_all')}*{riskData.get('is_honeypot')}*{riskData.get('is_proxy')} * {riskData.get('slippage_modifiable')} * {riskData.get('can_take_back_ownership')}")
