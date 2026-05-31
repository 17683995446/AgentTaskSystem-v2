import asyncio
import time
from AgentTaskSystem import AgentTaskSystem, TaskStatusEnum


async def example_business_logic(task_id: str, context: dict):
    step = context.get("step", 0) + 1
    print(f"Task {task_id} - Step {step} executing...")
    await asyncio.sleep(1)
    context["step"] = step
    
    if step >= 5:
        return (f"Completed after {step} steps", False)
    return (f"Step {step} done", True)


async def main():
    system = AgentTaskSystem()
    
    print("=== Agent Task System Example ===\n")
    
    task_id = system.task_define.create_task(
        task_type="example_task",
        priority=1,
        params={"data": "test"}
    )
    print(f"Created task: {task_id}")
    
    info = system.task_define.get_task_info(task_id)
    print(f"Task info: {info}")
    
    print("\nStarting task...")
    success = await system.task_runner.start_task(task_id, example_business_logic)
    print(f"Task started: {success}")
    
    await asyncio.sleep(6)
    
    info = system.task_define.get_task_info(task_id)
    print(f"\nFinal task info: {info}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
