from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
import time
import random
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# 存储任务结果
task_results = {}
active_connections = {}

# 创建线程池执行器
executor = ThreadPoolExecutor(max_workers=16)  # 限制最大并发任务数为 10

# 模拟耗时任务（5分钟）
def long_task(task_id: str):
    """模拟一个耗时的任务（5分钟）"""
    task_results[task_id] = {"status": "processing", "result": f"Task {task_id} is being processed."}
    time.sleep(300)  # 模拟 5 分钟的任务
    # 模拟随机错误：断线重连、超时
    if random.random() < 0.2:
        task_results[task_id] = {"status": "failed", "result": "Task failed due to network error."}
    else:
        task_results[task_id] = {"status": "completed", "result": f"Task {task_id} completed successfully."}
    
    # 任务完成后通知 WebSocket 客户端
    if task_id in active_connections:
        asyncio.create_task(notify_websocket(active_connections[task_id], task_id))

# WebSocket 连接
async def notify_websocket(connection: WebSocket, task_id: str):
    """通过 WebSocket 向客户端推送任务结果"""
    try:
        await connection.send_json({
            "task_id": task_id,
            "status": task_results[task_id]
        })
    except WebSocketDisconnect:
        active_connections.pop(task_id, None)
        print(f"WebSocket disconnected for task {task_id}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 处理客户端连接"""
    await websocket.accept()
    task_id = str(uuid.uuid4())  # 生成唯一任务 ID
    active_connections[task_id] = websocket
    
    # 客户端连接成功后，启动一个后台任务进行处理
    # 使用线程池来处理长时间运行的任务
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, long_task, task_id)
    
    # 发送任务的初始状态
    await websocket.send_json({
        "task_id": task_id,
        "status": {"status": "processing", "result": "Task is being processed."}
    })

@app.get("/process/{task_id}")
async def process_item(task_id: str):
    """HTTP 接口启动后台任务"""
    # 使用线程池来处理长时间任务
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, long_task, task_id)
    return {"message": f"Task {task_id} is being processed in the background."}
