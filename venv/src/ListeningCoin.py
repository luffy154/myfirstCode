from web3 import Web3
import json
import time

# 以太坊新池子监听
# 连接到以太坊节点
web3 = Web3(Web3.HTTPProvider('https://proud-wider-sponge.discover.quiknode.pro/700cf84ed019777ba23c95c754089411ce3de184/'))

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
    # {'args': AttributeDict({'token0': '0xbC1363a40aF7Ee8B266ceDf54Df396b2E7aE2f12', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'pair': '0x1A66be956F5BF3AD4Eaa76EB030e938687BD3eDa', '': 196947}), 'event': 'PairCreated', 'logIndex': 227, 'transactionIndex': 127, 'transactionHash': HexBytes('0xe0ea00bd68cc300231a175daba3f0da91b8021c08bfc7d7beb89de94ca98d680'), 'address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', 'blockHash': HexBytes('0xf2bb52d55f3c80765a6f7b44f4ffa53835968326d68f4c2368a5399e2765435a'), 'blockNumber': 17449134}
    token0_address = event['args']['token0']
    print(f'New pair created: {token0_address}')



# 监听事件
while True:
    events = event_filter.get_new_entries()
    # print(events)
    for event in events:
        # 将不可序列化对象转化为字典
        event_dict = dict(event)
        handle_event(event_dict)
    time.sleep(60)
