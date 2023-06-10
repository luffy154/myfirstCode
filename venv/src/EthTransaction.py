from web3 import Web3
import json

# 连接到以太坊节点
# endpoint = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1e7dd9bcc537448fa50a14f60ed3cbec'))

isTestNet = True
wss = "https://goerli.infura.io/v3/1e7dd9bcc537448fa50a14f60ed3cbec" if isTestNet else "wss://proud-wider-sponge.discover.quiknode.pro/700cf84ed019777ba23c95c754089411ce3de184/"
endpoint = Web3(Web3.WebsocketProvider(wss, websocket_timeout=60))


# 定义一个回调函数，用于处理新的交易事件
def handle_new_transaction(transaction):
    print("New transaction:", json.dumps(transaction))


# 监听最新的交易
def listen_for_new_transactions():
    filter = endpoint.eth.filter('pending')
    filter.watch(handle_new_transaction)


# 启动监听
listen_for_new_transactions()
