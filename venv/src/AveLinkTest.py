import requests
import base64
from urllib.parse import unquote
import json

authCode = "cfb32d7272c853a33da945d3e5c102641685285465940938643"
headers = {"User-Agent": "PostmanRuntime/7.31.3",
           "Accept": "*/*",
           "Accept-Encoding": "gzip, deflate, br",
           "X-Auth": f"{authCode}"}


def deleteContract(contractAddess):
    print("开始删除合约：", contractAddess)
    url = "https://api.hserpcvice.com/v1api/v2/tokens/favorite/delete"  # 要访问的网站 URL
    params = {
        "address": "0x3cbd3b92608fa8a14574762718ba85bf0857fa86",
        "token_id": f"{contractAddess}-eth"
    }
    jsonData = json.dumps(params)
    response = requests.post(url, data=jsonData, headers=headers)
    print(response.text)
    response.close()


def favriteContract():
    contractList = []
    url = "https://api.hserpcvice.com/v1api/v2/tokens/favorite?address=0x3cbd3b92608fa8a14574762718ba85bf0857fa86&group=-1"  # 要访问的网站 URL
    response = requests.get(url, headers=headers)
    responseDataJson = json.loads(response.text)
    response.close()
    # 进行 Base64 解码
    decoded_message = base64.b64decode(responseDataJson["encode_data"].encode('utf-8'))
    messageStr = unquote(decoded_message.decode('utf-8').replace("/\+/g", " "))
    # 将 JSON 字符串转换为 JSON 对象（Python 列表）
    json_obj = json.loads(messageStr)
    for obj in json_obj:
        print(obj["token"], obj.get("price_change"), obj["risk_score"])
        contractList.append(obj["token"])
    return contractList



def queryContractTransMessage(contractAddress):
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


contractList = favriteContract()
for contractAddress in contractList:
    if queryContractTransMessage(contractAddress):
        deleteContract(contractAddress)
