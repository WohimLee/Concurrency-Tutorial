from locust import HttpUser, task, between
import websocket
import threading
import json
import time
import random

class UserBehavior(HttpUser):
    wait_time = between(0.1, 0.5)  # 模拟请求间隔
    task_id = None  # 存储任务ID

    @task
    def start_task(self):
        """向 FastAPI 服务端发起 HTTP 请求，启动任务"""
        self.client.get("/process/1")
        self.task_id = "1"  # 假设任务 ID 是 1
        # 启动一个线程来通过 WebSocket 连接服务端
        threading.Thread(target=self.connect_websocket, args=(self.task_id,)).start()

    def connect_websocket(self, task_id):
        """WebSocket 连接到 FastAPI 服务端，接收任务结果"""
        ws = websocket.create_connection("ws://localhost:8000/ws")
        print(f"Connecting to WebSocket for task {task_id}")
        
        # 重试机制：模拟断线重连、超时
        retries = 0
        while retries < 5:
            try:
                # 等待 WebSocket 发送任务结果
                response = ws.recv()
                data = json.loads(response)
                if data["task_id"] == task_id:
                    print(f"Received result for task {task_id}: {data['status']['result']}")
                    ws.close()  # 任务完成，关闭连接
                    break
            except websocket.WebSocketConnectionClosedException:
                print(f"WebSocket connection closed unexpectedly, retrying... ({retries+1}/5)")
                retries += 1
                time.sleep(2)  # 重试间隔
                ws = websocket.create_connection("ws://localhost:8000/ws")  # 重新连接 WebSocket

            if retries == 5:
                print(f"Task {task_id} failed due to WebSocket connection issues.")

    def on_start(self):
        """Locust 客户端启动时的初始化行为"""
        print("Client started.")

    def on_stop(self):
        """Locust 客户端停止时的清理行为"""
        print("Client stopped.")
