# thread_manager.py
# agents注册和心跳检测
import threading
import time
import sys

# 存活状态：{线程名: bool}
alive = {}
threads = {}

def register(name, thread):
    threads[name] = thread
    alive[name] = True

def _heartbeat():
    for name, thread in threads.items():
        if thread.is_alive():
            alive[name] = True
        else:
            alive[name] = False

def keep_alive(t=10):
    while True:
        _heartbeat()
        if not any(alive.values()):
            sys.exit()
        time.sleep(t)
