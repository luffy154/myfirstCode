import requests
import base64
from urllib.parse import unquote
import json
from cron_lite import cron_task, start_all

authCode = "28620d1428cb82ed0a702e9cb7ccbbe61694874069472104471"
Signature = "0x123952b6c2473e0870f895c617e84fd1b719fad5da501de60124d91c0b5fa97e354a9d2fa0430a654db2a8989396055e73761912aa3ee1c6ed93ac3eda6501291c"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
           "Accept": "application/json, text/plain, */*",
           "Accept-Encoding": "gzip, deflate, br",
           "Ave-Udid":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36--1694874063047--69629aa6-ad36-4911-a604-cf28fd398cf5",
           "Signature": f"{Signature}",
           "X-Auth": f"{authCode}"}
contract_address_list_has_add = []


@cron_task("30 0/1 * * * 0")
def favriteContract():
    url = "https://api.fgsasd.org/v1api/v3/tokens/favorite?address=0x3cbd3b92608fa8a14574762718ba85bf0857fa86&group=0"  # 要访问的网站 URL
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
        deleteContract(contractAddress)
    # if queryContractTransMessage(contractAddress):
        #     deleteContract(contractAddress)
        #     addSelfList(contractAddress)
        #     print("转换新的合约地址", contractAddress)

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
