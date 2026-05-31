import asyncio
import uuid
from typing import Dict, Any, Callable, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


# ==============================
# TaskDefine Module (Level 2)
# ==============================

class TaskStatusEnum(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskDataDto:
    task_id: str
    task_type: str
    priority: int
    status: TaskStatusEnum
    params: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 3600


class _TaskDefineImpl:
    def __init__(self):
        self._task_storage: Dict[str, TaskDataDto] = {}

    def create_task(self, task_type: str, priority: int, params: Dict[str, Any]) -> str:
        task_id = str(uuid.uuid4())
        now = datetime.now()
        task = TaskDataDto(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            status=TaskStatusEnum.PENDING,
            params=params,
            created_at=now,
            updated_at=now
        )
        self._task_storage[task_id] = task
        return task_id

    def validate_params(self, task_type: str, params: Dict[str, Any]) -> bool:
        return isinstance(params, dict)

    def get_task_info(self, task_id: str) -> Dict[str, Any]:
        task = self._task_storage.get(task_id)
        if not task:
            return {}
        return {
            "task_id": task.task_id,
            "task_type": task.task_type,
            "priority": task.priority,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "retry_count": task.retry_count
        }

    def get_task_dto(self, task_id: str) -> Optional[TaskDataDto]:
        return self._task_storage.get(task_id)

    def update_task(self, task: TaskDataDto) -> None:
        task.updated_at = datetime.now()
        self._task_storage[task.task_id] = task


# ==============================
# TaskState Module (Level 2)
# ==============================

class _TaskStateImpl:
    def __init__(self, task_define_impl: _TaskDefineImpl):
        self._task_define = task_define_impl
        self._snapshots: Dict[str, list] = {}
        self._status_transitions = self._init_transitions()

    def _init_transitions(self):
        return {
            TaskStatusEnum.PENDING: [TaskStatusEnum.RUNNING, TaskStatusEnum.CANCELLED],
            TaskStatusEnum.RUNNING: [TaskStatusEnum.PAUSED, TaskStatusEnum.COMPLETED, TaskStatusEnum.FAILED, TaskStatusEnum.CANCELLED],
            TaskStatusEnum.PAUSED: [TaskStatusEnum.RUNNING, TaskStatusEnum.CANCELLED],
            TaskStatusEnum.COMPLETED: [],
            TaskStatusEnum.FAILED: [TaskStatusEnum.RUNNING, TaskStatusEnum.CANCELLED],
            TaskStatusEnum.CANCELLED: []
        }

    def _validate_transition(self, current, new_status):
        allowed = self._status_transitions.get(current, [])
        return new_status in allowed

    def update_status(self, task_id: str, new_status: TaskStatusEnum) -> bool:
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if not self._validate_transition(task.status, new_status):
            return False
        task.status = new_status
        self._task_define.update_task(task)
        return True

    def create_snapshot(self, task_id: str, context: Dict[str, Any]) -> str:
        snapshot_id = str(uuid.uuid4())
        snapshot = {
            "snapshot_id": snapshot_id,
            "task_id": task_id,
            "context": context,
            "created_at": datetime.now().isoformat()
        }
        if task_id not in self._snapshots:
            self._snapshots[task_id] = []
        self._snapshots[task_id].append(snapshot)
        return snapshot_id

    def get_latest_snapshot(self, task_id: str) -> Dict[str, Any]:
        snapshots = self._snapshots.get(task_id, [])
        if snapshots:
            return snapshots[-1]["context"].copy()
        return {}


# ==============================
# TaskSchedule Module (Level 2)
# ==============================

class _TaskScheduleImpl:
    def __init__(self, task_define_impl: _TaskDefineImpl):
        self._task_define = task_define_impl
        self._queue: list = []
        self._task_start_times: Dict[str, datetime] = {}

    def _sort_queue(self):
        def get_priority(task_id):
            task = self._task_define.get_task_dto(task_id)
            return task.priority if task else 0
        self._queue.sort(key=get_priority, reverse=True)

    def enqueue_task(self, task_id: str) -> bool:
        if task_id not in self._queue:
            self._queue.append(task_id)
            self._sort_queue()
            return True
        return False

    def dequeue_task(self) -> Optional[str]:
        if self._queue:
            task_id = self._queue.pop(0)
            self._task_start_times[task_id] = datetime.now()
            return task_id
        return None

    def check_retry(self, task_id: str) -> bool:
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if task.retry_count < task.max_retries:
            task.retry_count += 1
            self._task_define.update_task(task)
            return True
        return False


# ==============================
# TaskRunner Module (Level 2)
# ==============================

@dataclass
class TaskContextDto:
    task_id: str
    step: int
    context: Dict[str, Any]
    is_paused: bool = False


class _TaskRunnerImpl:
    def __init__(self, task_define_impl, task_state_impl, task_schedule_impl):
        self._task_define = task_define_impl
        self._task_state = task_state_impl
        self._task_schedule = task_schedule_impl
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._contexts: Dict[str, TaskContextDto] = {}

    def _create_context(self, task_id: str) -> TaskContextDto:
        return TaskContextDto(task_id=task_id, step=0, context={})

    async def start_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if not self._task_state.update_status(task_id, TaskStatusEnum.RUNNING):
            return False
        ctx = self._create_context(task_id)
        self._contexts[task_id] = ctx
        async_task = asyncio.create_task(self._execute_task(task_id, business_logic))
        self._running_tasks[task_id] = async_task
        return True

    async def _execute_task(self, task_id: str, business_logic: Callable):
        try:
            ctx = self._contexts[task_id]
            should_continue = True
            while should_continue:
                result, should_continue = await business_logic(task_id, ctx.context)
                ctx.step += 1
                ctx.context["step_result"] = result
                self._task_state.create_snapshot(task_id, {
                    "step": ctx.step,
                    "context": ctx.context
                })
                if ctx.is_paused:
                    self._task_state.update_status(task_id, TaskStatusEnum.PAUSED)
                    break
        except Exception as e:
            self._handle_error(task_id)
        else:
            self._task_state.update_status(task_id, TaskStatusEnum.COMPLETED)
        finally:
            if task_id in self._running_tasks:
                del self._running_tasks[task_id]

    def _handle_error(self, task_id: str):
        if self._task_schedule.check_retry(task_id):
            self._task_state.update_status(task_id, TaskStatusEnum.PENDING)
            self._task_schedule.enqueue_task(task_id)
        else:
            self._task_state.update_status(task_id, TaskStatusEnum.FAILED)


# ==============================
# Main System
# ==============================

class AgentTaskSystem:
    def __init__(self):
        self._task_define = _TaskDefineImpl()
        self._task_state = _TaskStateImpl(self._task_define)
        self._task_schedule = _TaskScheduleImpl(self._task_define)
        self._task_runner = _TaskRunnerImpl(self._task_define, self._task_state, self._task_schedule)

    def create_task(self, task_type: str, priority: int, params: Dict[str, Any]) -> str:
        return self._task_define.create_task(task_type, priority, params)

    def get_task_info(self, task_id: str) -> Dict[str, Any]:
        return self._task_define.get_task_info(task_id)

    async def start_task(self, task_id: str, business_logic: Callable) -> bool:
        return await self._task_runner.start_task(task_id, business_logic)


# ==============================
# Example Usage
# ==============================

async def example_business_logic(task_id: str, context: dict) -> Tuple[Any, bool]:
    step = context.get("step", 0) + 1
    print(f"Task {task_id} - Step {step} executing...")
    await asyncio.sleep(1)
    context["step"] = step
    
    if step >= 5:
        return (f"Completed after {step} steps", False)
    return (f"Step {step} done", True)


async def main():
    print("=== Agent Task System - Binary Tree Architecture ===\n")
    
    system = AgentTaskSystem()
    
    task_id = system.create_task(
        task_type="example_agent_task",
        priority=1,
        params={"data": "test_input"}
    )
    print(f"Created task: {task_id}")
    
    info = system.get_task_info(task_id)
    print(f"Task info: {info}\n")
    
    print("Starting task execution...")
    success = await system.start_task(task_id, example_business_logic)
    print(f"Task started: {success}\n")
    
    await asyncio.sleep(6)
    
    info = system.get_task_info(task_id)
    print(f"Final task info: {info}\n")
    
    print("=== System Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
