import os
import errno
from loguru import logger


log_path = './logs'

# 替换原来的 os.makedirs(log_path, exist_ok=True)
try:
    os.makedirs(log_path, exist_ok=True)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
    # 如果是目录已存在，检查是否为目录而非文件
    if not os.path.isdir(log_path):
        raise RuntimeError(f"'{log_path}' is a file, not a directory!")

# 配置 logger
logger.add(
    os.path.join(log_path, "{time:YYYY-MM-DD}.log"),  # 日志文件名格式
    rotation="30 MB",  # 每个日志文件最大 30MB，超过后创建新文件
    retention="90 days",  # 保留最近90天的日志
    compression="zip",  # 旧日志压缩格式
    encoding="utf-8",  # 编码
    enqueue=True,  # 多进程安全
    backtrace=True,  # 记录异常堆栈
    diagnose=True,  # 显示变量值以帮助调试
    level="INFO",  # 日志级别
)

import logging
# 设置 autogen_core 的日志级别
logging.getLogger('autogen_core').setLevel(logging.ERROR)
