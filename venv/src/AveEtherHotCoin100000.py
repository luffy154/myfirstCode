import requests
import base64
from urllib.parse import unquote
import json
from cron_lite import cron_task, start_all

authCode = "c905f094c965996cc53a2f7eb44d46951687443733688671254"
headers = {"User-Agent": "PostmanRuntime/7.31.3",
           "Accept": "*/*",
           "Accept-Encoding": "gzip, deflate, br",
           "X-Auth": f"{authCode}"}
contract_address_list_has_add = []


@cron_task("30 0/1 * * * 0")
def favriteContract():
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
        contractAddress = obj["token"]
        if queryContractTransMessage(contractAddress):
            deleteContract(contractAddress)
            addSelfList(contractAddress)
            print("转换新的合约地址", contractAddress)

def queryContractTransMessage(contractAddress):
    try:
        url = f"https://api.hserpcvice.com/v1api/v3/tokens/{contractAddress}-eth"  # 要访问的网站 URL
        response = requests.get(url, headers=headers)
        reponseMessage = response.text
        response.close()
        if reponseMessage.__contains__("Fail"):
            return False
        responseDataJson = json.loads(response.text)

        tokenInfo = responseDataJson["data"]["token"]
        marketInfo = responseDataJson["data"]["pairs"][0]
        mCap = (float(tokenInfo["total"]) - tokenInfo["burn_amount"]) * tokenInfo["current_price_usd"]
        print(mCap)
        liquidity = marketInfo["reserve1"] * marketInfo["token1_price_usd"]
        print(liquidity)
        # 市值小于50万的币添加自选
        if mCap < 100000:
            return True
    except:
        print(contractAddress, "查询市值失败")
    return False


def addSelfList(contractAddress):
    addUrl = "https://api.hserpcvice.com/v1api/v2/tokens/favorite/add"
    #  将合约地址加入自选
    params = {
        "address": "0x3cbd3b92608fa8a14574762718ba85bf0857fa86",
        "token_id": f"{contractAddress}-eth",
        "group": 1104436,
        "remark": ""
    }
    json_payLoad = json.dumps(params)
    response = requests.post(addUrl, data=json_payLoad, headers=headers)


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

favriteContract()
