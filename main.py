# E:/MeteorAgent/main.py
import tools
from agents import keep_alive

import coder

if __name__ == "__main__":
    print("""
===============================================
    ⚡ MeteorAgent 觉醒 ⚡
       「裁决模式已启动」
       「毁灭之锤，参上。」
===============================================
""")

    keep_alive()


# TODO
# 有多少个工人正在alive，要在queue那边搞一个心跳检测机制开给planner