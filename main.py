# E:/MeteorAgent/main.py
import sys
from pathlib import Path

# 把项目根目录加入 sys.path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from orchestrator import main as run_agent

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_agent())