from web3 import Web3
import json
import time

# 以太坊新池子监听
# 连接到以太坊节点
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1e7dd9bcc537448fa50a14f60ed3cbec'))

# Uniswap 工厂合约地址和 ABI
uniswap_factory_address = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_factory_abi = [
    # ABI 定义，可根据 Uniswap 的合约 ABI 进行更新
    # 这里仅包含一个事件示例
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "token0",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "token1",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "pair",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "PairCreated",
        "type": "event"
    }
]

# 获取 Uniswap 工厂合约实例
uniswap_factory_contract = web3.eth.contract(address=uniswap_factory_address, abi=uniswap_factory_abi)

# 订阅 PairCreated 事件
event_filter = uniswap_factory_contract.events.PairCreated.create_filter(fromBlock='latest')


# 处理事件回调函数
def handle_event(event):
    # 在这里处理新交易对事件
    pair_address = event['args']['pair']
    print(json.dumps(event))
    print(f'New pair created: {pair_address}')


# 监听事件
while True:
    events = event_filter.get_new_entries()
    # print(events)
    for event in events:
        # 将不可序列化对象转化为字典
        event_dict = dict(event)
        handle_event(event_dict)
    time.sleep(60)
