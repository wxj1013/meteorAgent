from config import Config
from utils import MessageCenter
import time
from utils import Task

host = Config.get("env").get("queues").get("host")
port = Config.get("env").get("queues").get("port")

mc = MessageCenter(host, port)

@assign_to(Coder, Planner)
def assign_task(target: str, content: str) -> str:
	"""
	通过消息队列，发布任务给planner以外的其他角色。
	coder: 编码者，负责写代码
	analyst：数据分析师，负责数据处理和加工
	engineer：模型工程师，负责模型相关工作
	tester：测试，负责测试和报告编写

	Args:
        target (str): 要发布任务的对象，可选项：coder, analyst, engineer, tester
        content (str): 发布的任务具体内容
	"""
	try
		if target not in ["coder", "analyst", "engineer", "tester"]:
			return "target参数错误，支持coder, analyst, engineer, tester。请确认任务的发布对象后重填"
		task_id = mc.publish_task(target, content)
		return f"任务已发布，任务编号:{task_id}。"
    except Exception as e:
        return f"任务发布失败：{str(e)}，建议立即回报，检查任务队列配置情况。"

@assign_to(Coder, Planner)
def report_result