import asyncio
import logging
from typing import Dict, Any, Callable, Optional, Tuple
from ..interfaces.ITaskRunner import ITaskRunner
from .TaskContextDto import TaskContextDto
from ....TaskCore.TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum

logger = logging.getLogger(__name__)


class _TaskRunnerImpl(ITaskRunner):
    def __init__(self, task_define_impl, task_state_impl, task_schedule_impl):
        logger.debug("[TaskRunner] __init__ start")
        self._task_define = task_define_impl
        self._task_state = task_state_impl
        self._task_schedule = task_schedule_impl
        self._business_logics: Dict[str, Callable] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._contexts: Dict[str, TaskContextDto] = {}
        logger.debug("[TaskRunner] __init__ complete")

    def register_business_logic(self, task_type: str, logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]):
        logger.debug(f"[TaskRunner] register_business_logic: task_type={task_type}")
        self._business_logics[task_type] = logic

    def _get_business_logic(self, task_type: str) -> Optional[Callable]:
        result = self._business_logics.get(task_type)
        logger.debug(f"[TaskRunner] _get_business_logic: task_type={task_type}, found={result is not None}")
        return result

    def _create_context(self, task_id: str) -> TaskContextDto:
        logger.debug(f"[TaskRunner] _create_context: task_id={task_id}")
        return TaskContextDto(task_id=task_id, step=0, context={})

    async def start_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        logger.info(f"[TaskRunner] start_task: task_id={task_id}")
        task = self._task_define.get_task_dto(task_id)
        if not task:
            logger.error(f"[TaskRunner] start_task FAILED: task not found, task_id={task_id}")
            return False
        logger.debug(f"[TaskRunner] start_task: current_status={task.status.value}")
        if not self._task_state.update_status(task_id, TaskStatusEnum.RUNNING):
            logger.error(f"[TaskRunner] start_task FAILED: status transition rejected, task_id={task_id}")
            return False
        logger.debug(f"[TaskRunner] start_task: status updated to RUNNING")
        return await self._launch_task(task_id, business_logic)

    async def _launch_task(self, task_id: str, business_logic: Callable) -> bool:
        logger.debug(f"[TaskRunner] _launch_task: task_id={task_id}")
        ctx = self._create_context(task_id)
        self._contexts[task_id] = ctx
        async_task = asyncio.create_task(self._execute_task(task_id, business_logic), name=f"task_{task_id}")
        async_task.add_done_callback(self._on_task_done)
        self._running_tasks[task_id] = async_task
        logger.info(f"[TaskRunner] _launch_task: task launched, task_id={task_id}")
        return True

    def _on_task_done(self, async_task: asyncio.Task):
        """任务完成回调，捕获未处理的异常"""
        try:
            async_task.result()
        except asyncio.CancelledError:
            logger.debug("[TaskRunner] _on_task_done: task cancelled")
        except Exception as e:
            logger.error(f"[TaskRunner] _on_task_done: unhandled exception: {e}")

    async def resume_task(self, task_id: str, business_logic: Callable[[str, Dict[str, Any]], Tuple[Any, bool]]) -> bool:
        logger.info(f"[TaskRunner] resume_task: task_id={task_id}")
        task = self._task_define.get_task_dto(task_id)
        if not task:
            logger.error(f"[TaskRunner] resume_task FAILED: task not found, task_id={task_id}")
            return False
        if not self._task_state.update_status(task_id, TaskStatusEnum.RUNNING):
            logger.error(f"[TaskRunner] resume_task FAILED: status transition rejected, task_id={task_id}")
            return False
        return await self._restore_and_launch(task_id, business_logic)

    async def _restore_and_launch(self, task_id: str, business_logic: Callable) -> bool:
        logger.debug(f"[TaskRunner] _restore_and_launch: task_id={task_id}")
        latest_ctx = self._task_state.get_latest_snapshot(task_id)
        ctx = self._build_context_from_snapshot(task_id, latest_ctx)
        self._contexts[task_id] = ctx
        logger.debug(f"[TaskRunner] _restore_and_launch: restored context, step={ctx.step}")
        async_task = asyncio.create_task(self._execute_task(task_id, business_logic), name=f"task_{task_id}")
        self._running_tasks[task_id] = async_task
        logger.info(f"[TaskRunner] _restore_and_launch: task resumed, task_id={task_id}")
        return True

    def _build_context_from_snapshot(self, task_id: str, latest_ctx: Dict[str, Any]) -> TaskContextDto:
        logger.debug(f"[TaskRunner] _build_context_from_snapshot: task_id={task_id}, snapshot_keys={list(latest_ctx.keys())}")
        return TaskContextDto(
            task_id=task_id,
            step=latest_ctx.get("step", 0),
            context=latest_ctx.get("context", {})
        )

    async def stop_task(self, task_id: str) -> bool:
        logger.info(f"[TaskRunner] stop_task: task_id={task_id}")
        if task_id not in self._running_tasks:
            logger.warning(f"[TaskRunner] stop_task FAILED: task not running, task_id={task_id}")
            return False
        return self._cancel_and_cleanup(task_id, TaskStatusEnum.CANCELLED)

    def _cancel_and_cleanup(self, task_id: str, final_status) -> bool:
        logger.debug(f"[TaskRunner] _cancel_and_cleanup: task_id={task_id}, final_status={final_status.value}")
        self._running_tasks[task_id].cancel()
        del self._running_tasks[task_id]
        self._task_state.update_status(task_id, final_status)
        logger.info(f"[TaskRunner] _cancel_and_cleanup: task cancelled, task_id={task_id}")
        return True

    async def _execute_task(self, task_id: str, business_logic: Callable):
        logger.info(f"[TaskRunner] _execute_task START: task_id={task_id}")
        try:
            await self._run_task_loop(task_id, business_logic)
        except asyncio.CancelledError:
            logger.warning(f"[TaskRunner] _execute_task CANCELLED: task_id={task_id}")
            raise
        except Exception as e:
            logger.exception(f"[TaskRunner] _execute_task EXCEPTION: task_id={task_id}, error={e}")
            self._handle_error(task_id, e)
        else:
            logger.info(f"[TaskRunner] _execute_task SUCCESS: task_id={task_id}, setting COMPLETED")
            self._task_state.update_status(task_id, TaskStatusEnum.COMPLETED)
        finally:
            logger.debug(f"[TaskRunner] _execute_task FINALLY: task_id={task_id}")
            self._cleanup_task(task_id)

    async def _run_task_loop(self, task_id: str, business_logic: Callable):
        logger.info(f"[TaskRunner] _run_task_loop START: task_id={task_id}")
        ctx = self._contexts[task_id]
        should_continue = True
        loop_count = 0
        while should_continue:
            loop_count += 1
            logger.debug(f"[TaskRunner] _run_task_loop ITERATION #{loop_count}: task_id={task_id}")
            try:
                result, should_continue = await business_logic(task_id, ctx.context)
            except Exception as e:
                logger.exception(f"[TaskRunner] _run_task_loop BUSINESS_LOGIC_EXCEPTION: task_id={task_id}, error={e}")
                raise
            ctx.step += 1
            ctx.context["step_result"] = result
            self._task_state.create_snapshot(task_id, {
                "step": ctx.step,
                "context": ctx.context
            })
            logger.debug(f"[TaskRunner] _run_task_loop SNAPSHOT: task_id={task_id}, step={ctx.step}, should_continue={should_continue}")
            if ctx.is_paused:
                logger.info(f"[TaskRunner] _run_task_loop PAUSED: task_id={task_id}, step={ctx.step}")
                self._task_state.update_status(task_id, TaskStatusEnum.PAUSED)
                break
        logger.info(f"[TaskRunner] _run_task_loop END: task_id={task_id}, total_iterations={loop_count}")

    def _cleanup_task(self, task_id: str) -> None:
        logger.debug(f"[TaskRunner] _cleanup_task: task_id={task_id}")
        if task_id in self._running_tasks:
            del self._running_tasks[task_id]
            logger.debug(f"[TaskRunner] _cleanup_task: removed from running_tasks, task_id={task_id}")
        if task_id in self._contexts:
            del self._contexts[task_id]
            logger.debug(f"[TaskRunner] _cleanup_task: removed from contexts, task_id={task_id}")

    def _handle_error(self, task_id: str, error: Exception = None) -> None:
        logger.error(f"[TaskRunner] _handle_error: task_id={task_id}, error={error}")
        # 先检查任务当前状态，确保可以转换到FAILED
        task = self._task_define.get_task_dto(task_id)
        if not task:
            logger.error(f"[TaskRunner] _handle_error: task not found, task_id={task_id}")
            return
        logger.debug(f"[TaskRunner] _handle_error: current_status={task.status.value}, retry_count={task.retry_count}")
        
        # 检查是否可以重试（不增加计数，只检查条件）
        can_retry = self._task_schedule._check_retry_conditions(task_id)
        logger.debug(f"[TaskRunner] _handle_error: can_retry={can_retry}")
        
        if can_retry:
            # 先尝试转换到PENDING，成功后再增加retry_count
            result = self._task_state.update_status(task_id, TaskStatusEnum.PENDING)
            logger.debug(f"[TaskRunner] _handle_error: PENDING transition result={result}")
            if result:
                # 状态转换成功，现在增加retry_count并入队
                self._task_schedule._do_retry(task_id)
                logger.info(f"[TaskRunner] _handle_error: retry scheduled, task_id={task_id}")
            else:
                # 状态转换失败（如RUNNING不能直接转PENDING），直接标记为FAILED
                logger.warning(f"[TaskRunner] _handle_error: PENDING transition failed, setting FAILED")
                self._task_state.update_status(task_id, TaskStatusEnum.FAILED)
        else:
            logger.error(f"[TaskRunner] _handle_error: max retries exceeded or not retryable, task_id={task_id}, setting FAILED")
            result = self._task_state.update_status(task_id, TaskStatusEnum.FAILED)
            logger.debug(f"[TaskRunner] _handle_error: FAILED status update result={result}")


def create_task_runner(task_define_impl, task_state_impl, task_schedule_impl):
    logger.debug("[TaskRunner] create_task_runner called")
    return _TaskRunnerImpl(task_define_impl, task_state_impl, task_schedule_impl)
