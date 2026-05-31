import asyncio
from typing import Dict, Any, Callable, Optional, Tuple
from ..interfaces.ITaskRunner import ITaskRunner
from .TaskContextDto import TaskContextDto


class _TaskRunnerImpl(ITaskRunner):
    def __init__(self, task_define_impl, task_state_impl, task_schedule_impl):
        self._task_define = task_define_impl
        self._task_state = task_state_impl
        self._task_schedule = task_schedule_impl
        self._business_logics: Dict[str, Callable] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._contexts: Dict[str, TaskContextDto] = {}

    def register_business_logic(self, task_type: str, logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]):
        self._business_logics[task_type] = logic

    def _get_business_logic(self, task_type: str) -> Optional[Callable]:
        return self._business_logics.get(task_type)

    def _create_context(self, task_id: str) -> TaskContextDto:
        return TaskContextDto(task_id=task_id, step=0, context={})

    async def start_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        from ...TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if not self._task_state.update_status(task_id, TaskStatusEnum.RUNNING):
            return False
        return await self._launch_task(task_id, business_logic)

    async def _launch_task(self, task_id: str, business_logic: Callable) -> bool:
        ctx = self._create_context(task_id)
        self._contexts[task_id] = ctx
        async_task = asyncio.create_task(self._execute_task(task_id, business_logic))
        self._running_tasks[task_id] = async_task
        return True

    async def resume_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        from ...TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if not self._task_state.update_status(task_id, TaskStatusEnum.RUNNING):
            return False
        return await self._restore_and_launch(task_id, business_logic)

    async def _restore_and_launch(self, task_id: str, business_logic: Callable) -> bool:
        latest_ctx = self._task_state.get_latest_snapshot(task_id)
        ctx = self._build_context_from_snapshot(task_id, latest_ctx)
        self._contexts[task_id] = ctx
        async_task = asyncio.create_task(self._execute_task(task_id, business_logic))
        self._running_tasks[task_id] = async_task
        return True

    def _build_context_from_snapshot(self, task_id: str, latest_ctx: Dict[str, Any]) -> TaskContextDto:
        return TaskContextDto(
            task_id=task_id,
            step=latest_ctx.get("step", 0),
            context=latest_ctx.get("context", {})
        )

    async def stop_task(self, task_id: str) -> bool:
        from ...TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        if task_id not in self._running_tasks:
            return False
        return self._cancel_and_cleanup(task_id, TaskStatusEnum.CANCELLED)

    def _cancel_and_cleanup(self, task_id: str, final_status) -> bool:
        self._running_tasks[task_id].cancel()
        del self._running_tasks[task_id]
        self._task_state.update_status(task_id, final_status)
        return True

    async def _execute_task(self, task_id: str, business_logic: Callable):
        from ...TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        try:
            await self._run_task_loop(task_id, business_logic)
        except Exception as e:
            self._handle_error(task_id)
        else:
            self._task_state.update_status(task_id, TaskStatusEnum.COMPLETED)
        finally:
            self._cleanup_task(task_id)

    async def _run_task_loop(self, task_id: str, business_logic: Callable):
        from ...TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
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

    def _cleanup_task(self, task_id: str) -> None:
        if task_id in self._running_tasks:
            del self._running_tasks[task_id]

    def _handle_error(self, task_id: str) -> None:
        from ...TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum
        if self._task_schedule.check_retry(task_id):
            self._task_state.update_status(task_id, TaskStatusEnum.PENDING)
            self._task_schedule.enqueue_task(task_id)
        else:
            self._task_state.update_status(task_id, TaskStatusEnum.FAILED)


def create_task_runner(task_define_impl, task_state_impl, task_schedule_impl):
    return _TaskRunnerImpl(task_define_impl, task_state_impl, task_schedule_impl)
