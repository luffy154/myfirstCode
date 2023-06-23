# 自动买币机器人

from web3 import Web3, IPCProvider
import time
import urllib.request, json
import traceback

routers = [
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",
    # "0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b",
    # "0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B",
    # "0x1111111254EEB25477B68fb85Ed929f73A960582",
    # "0x1111111254eeb25477b68fb85ed929f73a960582",
    # "0xe66B31678d6C16E9ebf358268a790B763C133750",
    # "0xe66b31678d6c16e9ebf358268a790b763c133750",
    # "0x881D40237659C251811CEC9c364ef91dC08D300C",
    # "0x881d40237659c251811cec9c364ef91dc08d300c",
    # "0xA88800CD213dA5Ae406ce248380802BD53b47647",
    # "0xa88800cd213da5ae406ce248380802bd53b47647",
    # "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",
    # "0xdef1c0ded9bec7f1a1670819833240f027b25eff",
    # "0x1111111254fb6c44bAC0beD2854e76F90643097d",
    # "0x1111111254fb6c44bac0bed2854e76f90643097d",
    # "0xA88800CD213dA5Ae406ce248380802BD53b47647",
    # "0xa88800cd213da5ae406ce248380802bd53b47647",
    # "0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57",
    # "0xdef171fe48cf0115b1d80b88dc8eab59176fee57",
    # "0xA88800CD213dA5Ae406ce248380802BD53b47647",
    # "0xa88800cd213da5ae406ce248380802bd53b47647",
    # "0xDEF171Fe48CF0115B1d80b88dc8eAB59176FEe57",
    # "0xdef171fe48cf0115b1d80b88dc8eab59176fee57",
    # "0x84D99Aa569D93a9CA187D83734c8C4a519c4e9b1",
    # "0x84d99aa569d93a9ca187d83734c8c4a519c4e9b1",
    # "0xe8eA8bAE250028a8709A3841E0Ae1a44820d677b",
    # "0xe8ea8bae250028a8709a3841e0ae1a44820d677b",
    # "0xD1742B3C4fBB096990C8950fA635Aec75B30781A",
    # "0xd1742b3c4fbb096990c8950fa635aec75b30781a",
    # "0x11111112542D85B3EF69AE05771c2dCCff4fAa26",
    # "0x11111112542d85b3ef69ae05771c2dccff4faa26",
    "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD",
    "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad"
]

print(routers.__contains__("0x3Fc91a3afd70395cd496c647d5a6cc9d4b2b7fad".lower()))
print("0x3Fc91a3afd70395cd496c647d5a6cc9d4b2b7fad".lower())
# with urllib.request.urlopen("https://api.etherscan.io/api?module=contract&action=getabi&address=0xC12D1c73eE7DC3615BA4e37E4ABFdbDDFA38907E ") as url:
#     ABI = json.loads(url.read())
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactETHForTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactETHForTokensSupportingFeeOnTransferTokens",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapETHForExactTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
]
private_key = '0x6c9233c282d8fd944520fdd69884f73f82403182d47f5aa9a8a0b0d45653784b'
blackAddress = "0x7CF7BdFc81b1f5E04c6FfD80014E3374F97278dF"

# instantiate Web3 instance
# wss://proud-wider-sponge.discover.quiknode.pro/700cf84ed019777ba23c95c754089411ce3de184/
# w3 = Web3(
#     Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/1e7dd9bcc537448fa50a14f60ed3cbec",websocket_timeout=60))

w3 = Web3(
    Web3.HTTPProvider("https://proud-wider-sponge.discover.quiknode.pro/700cf84ed019777ba23c95c754089411ce3de184/"))
contract = w3.eth.contract(address=w3.to_checksum_address("0x7a250d5630b4cf539739df2c5dacb4c659f2488d"),
                           abi=contract_abi)


def handle_event(event):
    block_hash = event.hex()
    try:
        transaction = w3.eth.get_transaction(block_hash)
        # AttributeDict({'blockHash': None, 'blockNumber': None, 'from': '0x3cD751E6b0078Be393132286c442345e5DC49699', 'gas': 21000, 'gasPrice': 30000000000, 'maxFeePerGas': 30000000000, 'maxPriorityFeePerGas': 1000000000, 'hash': HexBytes('0x4199cb370192617a3bc948cf029c4557e2edb33911ff62bac26e6a598b335d30'), 'input': '0x', 'nonce': 9064900, 'to': '0x011A29Ea9d4eFE709858b7Ba1F602CC22e15eD29', 'transactionIndex': None, 'value': 1083279500000000, 'type': 2, 'accessList': [], 'chainId': 1, 'v': 1, 'r': HexBytes('0x620a5eb0daacf5f2cfb12a3c36079a6350c9607267959a4e24651b94eda53aac'), 's': HexBytes('0x6d227e2dba579805e26169b20106583c2d386fb41c2ae139701a83920570a4af')})
        if transaction is not None and routers.__contains__(transaction.get('to').lower()) and transaction.get(
                'from') != blackAddress:
            value = transaction['value']
            gasPrice = transaction['gasPrice']
            gasLimit = transaction.get('gasLimit')
            functionBean = None
            try:
                # (<Function swapExactETHForTokens(uint256,address[],address,uint256)>, {'amountOutMin': 129911559008973122175595361200, 'path': ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', '0x6Ee9742d17B527e682248DCA85952e4Fe190061d'], 'to': '0x84Ab9C3AA3518c4f67837712d8E87011ba89B0E5', 'deadline': 1686622461})
                func_obj, func_params = contract.decode_function_input(transaction['input'])
            except Exception as e1:
                pass
                # print("方法解码失败", e1)
                # traceback.print_exc()
            if functionBean is not None:
                print(func_obj)
                tokenAddress = func_params['path'][1]
                print("tokenAddress", tokenAddress)
            print(value, gasPrice, gasLimit)
            print(transaction)
    except Exception as e:
        print(block_hash, e)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)


def main():
    block_filter = w3.eth.filter('pending')
    log_loop(block_filter, 2)


if __name__ == '__main__':
    main()
