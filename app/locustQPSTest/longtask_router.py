
import uuid
import asyncio
from fastapi import WebSocket, APIRouter
from concurrent.futures import ThreadPoolExecutor

from longtask_controler import get_active_connections, execute_long_task

longtask_router = APIRouter()


# 创建线程池执行器
executor = ThreadPoolExecutor(max_workers=16)

@longtask_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 处理客户端连接"""
    await websocket.accept()
    
    task_id = str(uuid.uuid4())  # 为每个连接生成一个唯一的 task_id
    active_connections = get_active_connections()
    active_connections[task_id] = websocket
    
    # 在 WebSocket 连接建立后，立刻返回“收到请求”消息
    await websocket.send_json({
        "task_id": task_id,
        "status": {"status": "received", "result": "Request received, processing started."}
    })
    
    # 客户端连接成功后，启动后台任务进行处理
    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, execute_long_task, task_id)
    
    # 客户端接收到的初始状态
    await websocket.send_json({
        "task_id": task_id,
        "status": {"status": "processing", "result": "Task is being processed."}
    })
