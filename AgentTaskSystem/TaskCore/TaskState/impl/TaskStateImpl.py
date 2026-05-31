import uuid
from typing import Dict, Any, List
from datetime import datetime
from ..interfaces.ITaskState import ITaskState
from ...TaskDefine.interfaces.TaskStatusEnum import TaskStatusEnum


class _TaskStateImpl(ITaskState):
    def __init__(self, task_define_impl):
        self._task_define = task_define_impl
        self._snapshots: Dict[str, List[Dict[str, Any]]] = {}
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

    def update_status(self, task_id: str, new_status) -> bool:
        task = self._task_define.get_task_dto(task_id)
        if not task:
            return False
        if not self._validate_transition(task.status, new_status):
            return False
        return self._apply_status_update(task, new_status)

    def _apply_status_update(self, task, new_status) -> bool:
        task.status = new_status
        self._task_define.update_task(task)
        return True

    def create_snapshot(self, task_id: str, context: Dict[str, Any]) -> str:
        snapshot_id = self._generate_snapshot_id()
        snapshot = self._build_snapshot(task_id, snapshot_id, context)
        self._store_snapshot(task_id, snapshot)
        return snapshot_id

    def _generate_snapshot_id(self) -> str:
        return str(uuid.uuid4())

    def _build_snapshot(self, task_id: str, snapshot_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "snapshot_id": snapshot_id,
            "task_id": task_id,
            "context": context,
            "created_at": datetime.now().isoformat()
        }

    def _store_snapshot(self, task_id: str, snapshot: Dict[str, Any]) -> None:
        if task_id not in self._snapshots:
            self._snapshots[task_id] = []
        self._snapshots[task_id].append(snapshot)

    def restore_snapshot(self, task_id: str, snapshot_id: str) -> Dict[str, Any]:
        snapshots = self._snapshots.get(task_id, [])
        return self._find_snapshot_context(snapshots, snapshot_id)

    def _find_snapshot_context(self, snapshots: List[Dict[str, Any]], snapshot_id: str) -> Dict[str, Any]:
        for snap in snapshots:
            if snap["snapshot_id"] == snapshot_id:
                return snap["context"].copy()
        return {}

    def get_latest_snapshot(self, task_id: str) -> Dict[str, Any]:
        snapshots = self._snapshots.get(task_id, [])
        return self._extract_latest_context(snapshots)

    def _extract_latest_context(self, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
        if snapshots:
            return snapshots[-1]["context"].copy()
        return {}


def create_task_state(task_define_impl):
    return _TaskStateImpl(task_define_impl)
