

import uuid
import json
import asyncio
import requests
import websockets


async def send_request():
    uri = "ws://localhost:8000/ws"
    
    # 创建 WebSocket 连接
    async with websockets.connect(uri) as websocket:
        # 生成一个唯一的 task_id
        task_id = str(uuid.uuid4())

        # 发送任务请求
        await websocket.send(json.dumps({
            "task_id": task_id,
            "status": {"status": "processing", "result": "Task is being processed."}
        }))

        # 接收任务状态更新
        response = await websocket.recv()
        print("Received:", response)



if __name__ == "__main__":
    # 启动 WebSocket 客户端
    asyncio.run(send_request())
