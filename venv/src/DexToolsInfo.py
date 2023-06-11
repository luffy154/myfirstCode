import asyncio
import websockets
import json

async def handle_message(message):
    # 在这里处理接收到的消息
    print(f"Received message: {message}")


async def connect_to_remote_websocket():
    uri = "wss://ws.dextools.io/"  # 替换为实际的远程WebSocket服务器的URL
    params = {"jsonrpc": "2.0",
              "method": "subscribe",
              "params": {
                  "chain": "ether",
                  "channel": "uni:common"
              },
              "id": 1
              } # 要发送的参数
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Connection":"Upgrade",
        "Sec-Websocket-Key":"or4VezeBBusYkxzRXO01eQ=="
    }
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        print(f"Connected to {uri}")
        await websocket.send(json.dumps(params))
        while True:
            print("messqage handle")
            message = await websocket.recv()  # 接收来自服务器的消息
            await handle_message(message)

async def reconnect_websocket():
    while True:
        try:
            print("jinlai")
            await connect_to_remote_websocket()
        except websockets.exceptions.ConnectionClosedError :
            print("Error: 连接断了")
            # 连接关闭时，等待一段时间后进行重连
            await asyncio.sleep(5)
        except Exception as e:
            # 其他异常处理
            print(f"Error: {str(e)}")



# 运行WebSocket客户端
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(reconnect_websocket())
