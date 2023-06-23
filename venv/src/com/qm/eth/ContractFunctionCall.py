from web3 import Web3
from eth_account import Account

# Connect to the Ethereum network
w3 = Web3(
    Web3.HTTPProvider('https://proud-wider-sponge.discover.quiknode.pro/700cf84ed019777ba23c95c754089411ce3de184/'))

modifyFlag = False

# Contract address and ABI
contract_address = '0x3bb1c03e4ed495acd60476211859729dc579502f'
contract_checksum_address = w3.to_checksum_address(contract_address)
contract_abi = [
    # Contract ABI definitions
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "getExactTransferAmount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "setExactTransferAmount",
        "outputs": [

        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    # Add more method definitions if needed
]

# Create contract instance
contract = w3.eth.contract(address=contract_checksum_address, abi=contract_abi)

address_list = ["0x19100a24b2c4bff4ea912dd56288f46d14f8f555", "0x0bb763566600e530a9f3510e62407e0191d214ca"]

private_key = '0x6c9233c282d8fd944520fdd69884f73f82403182d47f5aa9a8a0b0d45653784b'

# 创建账户对象
account = Account.from_key(private_key)
if modifyFlag:
    for address in address_list:
        address_argument = Web3.to_checksum_address(address)
        # contract.functions.setExactTransferAmount(address_argument, 0).call()
        # 构建交易
        transaction = contract.functions.setExactTransferAmount(address_argument, 0).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.to_wei('10', 'gwei'),
        })
        # 签名交易
        signed_txn = account.sign_transaction(transaction)
        # 发送交易
        transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        transaction = w3.eth.get_transaction(transaction_hash)
        print(transaction)

for address in address_list:
    address_argument = Web3.to_checksum_address(address)

    # Call the contract method
    result = contract.functions.getExactTransferAmount(address_argument).call()

    # Access the returned value
    print("Result:", result/1000000000000000000)
