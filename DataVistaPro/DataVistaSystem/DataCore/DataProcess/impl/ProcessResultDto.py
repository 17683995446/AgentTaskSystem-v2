from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ProcessResultDto:
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    errors: List[str] = None
    warnings: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}
