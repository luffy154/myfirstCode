import requests
import base64
from urllib.parse import unquote
import json
import traceback
from cron_lite import cron_task, start_all

authCode = "54699113ddb23e4e641d996c85713dfe1699419771701628985"
headers = {"User-Agent": "PostmanRuntime/7.31.3",
           "Accept": "*/*",
           "Accept-Encoding": "gzip, deflate, br",
           "Signature":"0x123952b6c2473e0870f895c617e84fd1b719fad5da501de60124d91c0b5fa97e354a9d2fa0430a654db2a8989396055e73761912aa3ee1c6ed93ac3eda6501291c",
           "X-Auth": f"{authCode}"}
contract_address_list_has_add = []


@cron_task("30 * * * * 0")
def queryHotCoin():
    myheaders = {"User-Agent": "PostmanRuntime/7.31.3",
                 "Accept": "*/*",
                 "Accept-Encoding": "gzip, deflate, br"}
    url = "https://api.fgsasd.org/v1api/v2/discover/token_list?pageNO=2&pageSize=1000&sort=&direction=desc&chain=bsc&category=sniper"  # 要访问的网站 URL
    response = requests.get(url, headers=myheaders)
    responseDataJson = json.loads(response.text)
    response.close()
    # 进行 Base64 解码
    decoded_message = base64.b64decode(responseDataJson["encode_data"].encode('utf-8'))
    messageStr = unquote(decoded_message.decode('utf-8').replace("/\+/g", " "))
    json_obj = json.loads(messageStr)
    for obj in json_obj:
        contractAddress = obj["token"]
        if contract_address_list_has_add.__contains__(contractAddress):
            continue
        if queryContractTransMessage(contractAddress):
            addSelfList(contractAddress)
            print("添加的新的合约地址", contractAddress)
            contract_address_list_has_add.append(contractAddress)


def queryContractTransMessage(contractAddress):
    try:
        url = f"https://api.hserpcvice.com/v1api/v3/tokens/{contractAddress}-bsc"  # 要访问的网站 URL
        response = requests.get(url, headers=headers)
        reponseMessage = response.text
        response.close()
        if reponseMessage.__contains__("Fail"):
            return False
        responseDataJson = json.loads(response.text)
        data = json.loads(responseDataJson["data"])
        tokenInfo = data["token"]
        marketInfo = data["pairs"][0]
        mCap = (float(tokenInfo["total"]) - tokenInfo["burn_amount"]) * tokenInfo["current_price_usd"]
        print(mCap)
        liquidity = marketInfo["reserve1"] * marketInfo["token1_price_usd"]
        print(liquidity)
        print(contractAddress)
        # 持币人数
        holders = tokenInfo['holders']
        # 交易次数
        txCount = marketInfo['tx_count']
        logoUrl = tokenInfo.get('logo_url')

        print(logoUrl)
        # 市值小于50万的币添加自选
        if logoUrl != None and logoUrl != '' and mCap < 1000000:
            return True
    except Exception as e:
        print(contractAddress, "查询市值失败")
        traceback.print_exc()
    return False


def addSelfList(contractAddress):
    addUrl = "https://api.fgsasd.org/v1api/v3/tokens/favorite/add"
    #  将合约地址加入自选
    params = {
        "address": "0x3cbd3b92608fa8a14574762718ba85bf0857fa86",
        "token_id": f"{contractAddress}-bsc",
        "group": 154067,
        "remark": ""
    }
    json_payLoad = json.dumps(params)
    response = requests.post(addUrl, data=json_payLoad, headers=headers)


queryHotCoin()
