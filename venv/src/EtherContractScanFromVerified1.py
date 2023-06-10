import requests
from bs4 import BeautifulSoup
import json
from cron_lite import cron_task, start_all
import time
contract_address_list_has_add = []
addUrl = "https://api.hserpcvice.com/v1api/v2/tokens/favorite/add"

@cron_task("* * * * 0/2 0")
def addLatestContract():
    print("addLatestContract start ", time.strftime("%Y-%m_%d %H:%M:%S", time.localtime(time.time())))
    headers = {"User-Agent": "PostmanRuntime/7.31.3", "Accept": "*/*", "Accept-Encoding": "gpt"}
    contract_address_list = []
    authCode = "cfb32d7272c853a33da945d3e5c102641685285465940938643"
    for i in range(6):
        url = f"https://etherscan.io/contractsVerified/{i + 1}?ps=100"  # 要访问的网站 URL
        # 发送 GET 请求并获取网站内容
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        response.close()
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
                    if int(tdhtml.text) < 10:
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
        try:
            if contract_address_list_has_add.__contains__(contractAddress):
                continue
            url = f"https://api.hserpcvice.com/v1api/v2/tokens/contract?token_id={contractAddress}-eth&type=token&user_address="  # 要访问的网站 URL
            # 发送 GET 请求并获取网站内容
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
            response.close()
            #判断合约风险
            if data['data']['token_contract']['contract_data']['risk_score'] <= 60:
                riskData = data['data']['token_contract']['contract_data']
                print(
                    f"{contractAddress}*{riskData.get('risk_score')}*{riskData.get('owner')}*{riskData.get('cannot_sell_all')}*{riskData.get('is_honeypot')}*{riskData.get('is_proxy')} * {riskData.get('slippage_modifiable')} * {riskData.get('can_take_back_ownership')}")
                if not queryContractTransMessage(contractAddress):
                    #  将合约地址加入自选
                    params = {
                        "address": "0x3cbd3b92608fa8a14574762718ba85bf0857fa86",
                        "token_id": f"{contractAddress}-eth",
                        "group": 0,
                        "remark": ""
                    }
                    json_payLoad = json.dumps(params)
                    response = requests.post(addUrl,data=json_payLoad,headers=headers)
                    contract_address_list_has_add.append(contractAddress)
        except Exception  as e:
            print(contractAddress,e)
    print("addLatestContract end ", time.strftime("%Y-%m_%d %H:%M:%S", time.localtime(time.time())))

def queryContractTransMessage(contractAddress):
    authCode = "cfb32d7272c853a33da945d3e5c102641685285465940938643"
    headers = {"User-Agent": "PostmanRuntime/7.31.3",
               "Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "X-Auth": f"{authCode}"}
    try:
        url = f"https://api.hserpcvice.com/v1api/v3/tokens/{contractAddress}-eth"  # 要访问的网站 URL
        response = requests.get(url, headers=headers)
        reponseMessage = response.text
        response.close()
        if reponseMessage.__contains__("Fail"):
            return True
        responseDataJson = json.loads(response.text)

        tokenInfo = responseDataJson["data"]["token"]
        marketInfo = responseDataJson["data"]["pairs"][0]
        mCap = (float(tokenInfo["total"]) - tokenInfo["burn_amount"]) * tokenInfo["current_price_usd"]
        print(mCap)
        liquidity = marketInfo["reserve1"] * marketInfo["token1_price_usd"]
        print(liquidity)
        if mCap < 10000 or liquidity < 5000:
            return True
    except:
        print(contractAddress, "查询市值失败")
    return False

start_all()

while True:
    pass