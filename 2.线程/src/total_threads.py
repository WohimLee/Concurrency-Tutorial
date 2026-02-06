import psutil

# # 获取所有进程的线程数
# total_threads = sum(p.num_threads() for p in psutil.process_iter())
# print(f"Total number of threads: {total_threads}")



# # 获取所有进程的线程数，跳过系统进程（pid = 0 或其他受保护进程）
# total_threads = sum(p.num_threads() for p in psutil.process_iter() if p.info['pid'] > 1)
# print(f"Total number of threads: {total_threads}")


# 如果你想进一步控制哪些进程的信息需要被访问，可以使用 psutil.Process() 对象获取特定进程的线程数，并捕获异常。

total_threads = 0

for p in psutil.process_iter(['pid', 'name']):
    try:
        total_threads += p.num_threads()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        # 处理无法访问的进程
        pass

print(f"Total number of threads: {total_threads}")