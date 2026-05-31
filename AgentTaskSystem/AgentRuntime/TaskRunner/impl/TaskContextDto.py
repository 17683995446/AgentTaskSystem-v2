from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TaskContextDto:
    task_id: str
    step: int
    context: Dict[str, Any]
    is_paused: bool = False
