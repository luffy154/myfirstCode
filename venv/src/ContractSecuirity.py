import json
import requests

headers = {"User-Agent": "PostmanRuntime/7.31.3",
           "Accept": "*/*",
           "Accept-Encoding": "gzip, deflate, br",
           "X-Auth":"cfb32d7272c853a33da945d3e5c102641685285465940938643"}
contradtAddress = "0x996a358854dd77fb75aec15fb5b1a337b020cb06"
url = f"https://api.hserpcvice.com/v1api/v2/tokens/contract?token_id={contradtAddress}-eth&type=token&user_address="  # 要访问的网站 URL
# 发送 GET 请求并获取网站内容
response = requests.get(url, headers=headers)
data = json.loads(response.text)

print(f"{data['data']['token_contract']}")