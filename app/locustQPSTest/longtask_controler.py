import time
import random
import asyncio

from fastapi import WebSocket, WebSocketDisconnect

# 存储任务结果
_task_results = {}
_active_connections = {}

# 模拟耗时任务（5分钟）
def execute_long_task(task_id: str):
    """模拟一个耗时的任务（5分钟）"""
    _task_results[task_id] = {"status": "processing", "result": f"Task {task_id} is being processed."}
    time.sleep(300)  # 模拟 5 分钟的任务
    # 模拟随机错误：断线重连、超时
    if random.random() < 0.2:
        _task_results[task_id] = {"status": "failed", "result": "Task failed due to network error."}
    else:
        _task_results[task_id] = {"status": "completed", "result": f"Task {task_id} completed successfully."}
    
    # 任务完成后通知 WebSocket 客户端
    if task_id in _active_connections:
        asyncio.create_task(notify_websocket(_active_connections[task_id], task_id))

# WebSocket 连接
async def notify_websocket(connection: WebSocket, task_id: str):
    """通过 WebSocket 向客户端推送任务结果"""
    try:
        await connection.send_json({
            "task_id": task_id,
            "status": _task_results[task_id]
        })
    except WebSocketDisconnect:
        _active_connections.pop(task_id, None)
        print(f"WebSocket disconnected for task {task_id}")


def get_active_connections():
    global _active_connections
    return _active_connections