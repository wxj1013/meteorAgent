from config import Config
from utils import MessageCenter

host = Config.get("env").get("queues").get("host")

@assign_to(Coder, Planner)
def 