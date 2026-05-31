from .TaskCore import ITaskDefine, TaskStatusEnum, create_task_define, ITaskState, create_task_state
from .AgentRuntime import ITaskSchedule, create_task_schedule, ITaskRunner, create_task_runner


class AgentTaskSystem:
    def __init__(self):
        self._task_define_impl = None
        self.task_define: ITaskDefine = None
        self.task_state: ITaskState = None
        self.task_schedule: ITaskSchedule = None
        self.task_runner: ITaskRunner = None
        self._init_system()

    def _init_system(self):
        self._task_define_impl = create_task_define()
        self.task_define = self._task_define_impl
        self.task_state = create_task_state(self._task_define_impl)
        self.task_schedule = create_task_schedule(self._task_define_impl)
        self.task_runner = create_task_runner(
            self._task_define_impl,
            self.task_state,
            self.task_schedule
        )


__all__ = [
    "AgentTaskSystem",
    "ITaskDefine",
    "TaskStatusEnum",
    "ITaskState",
    "ITaskSchedule",
    "ITaskRunner"
]
