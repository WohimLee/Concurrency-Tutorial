# 启动 FastAPI 服务端（server.py）：
uvicorn server:app --reload

# 启动 Locust 压力测试：
locust -f client.py


# 打开 Locust Web 界面：
http://localhost:8089

# 配置并发用户数、启动速率等，点击 Start swarming 开始测试。