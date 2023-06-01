import hashlib
import json


def keccak256_hash(data):
    hash_object = hashlib.sha3_256(data.encode())
    hex_hash = hash_object.hexdigest()
    return hex_hash


def keccak256_hash_hex(hex_data):
    # 将十六进制数转换为字节类型
    byte_data = bytes.fromhex(hex_data)
    hash_object = hashlib.sha3_256(byte_data)
    hex_hash = hash_object.hexdigest()
    return hex_hash


code = "4b20993bc481177ec7e8f571cecae8a9e22c02db"
hash_value = keccak256_hash_hex(code)
print("Keccak256 Hash:", hash_value)

jsonStr = '{}'
print(f"{hash_value}|{code}")
contractData = json.loads(jsonStr)
print(contractData['contract_data']['risk_score'])
