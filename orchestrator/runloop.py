from .planner import Planner

async def main():
    print("=" * 50)
    print("MeteorAgent Starting...")
    print("=" * 50)

    # 1. 初始化 Planner
    planner = Planner()

    # 2. 模拟一次规划
    goal = "Train a ResNet on CIFAR-10"
    print(f"\n[GOAL] {goal}")
    print(f"\n[PLANNER] Thinking...")

    action = await planner.plan(goal, history=[])

    # 3. 打印结果
    print(f"\n{'=' * 50}")
    print(f"[ACTION] Tool: {action.tool}")
    print(f"[ACTION] Thought: {action.thought}")
    print(f"[ACTION] Args: {action.args}")
    print(f"{'=' * 50}")

    print("\n✅ MeteorAgent runloop completed successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())