import asyncio
import websockets

async def handle_client(websocket, path):
    # 这里处理来自客户端的消息和发送消息给客户端的逻辑
    while True:
        message = await websocket.recv()  # 接收来自客户端的消息
        print(f"Received message from client: {message}")

        response = f"Server received message: {message}"
        await websocket.send(response)  # 发送消息给客户端

# 启动WebSocket服务
async def start_websocket_server():
    server = await websockets.serve(handle_client, "localhost", 8765)  # 监听本地主机的8765端口

    print("WebSocket server started")
    await server.wait_closed()

# 运行WebSocket服务
asyncio.run(start_websocket_server())