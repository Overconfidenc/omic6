from dataclasses import dataclass
from datetime import datetime
from view import IPresentation
import random

@dataclass
class OperationLogEntry:
    record_id: str
    record: str  
    status: str  
    result: str
    timestamp: datetime = datetime.now()

class OperationRepository:
    def __init__(self):
        self._journal = []

    def add_entry(self, entry: OperationLogEntry):
        self._journal.append(entry)
        print(f"запись операции: {entry.record} [{entry.status}]")

    def get_active_operations(self):
        return [op for op in self._journal if op.status == "Running"]

class OperationController:
    def __init__(self, repo: OperationRepository, view: IPresentation):
        self.repo = repo
        self.view = view

    def execute_critical_check(self, intent: str) -> bool:
        if intent in ["emergency_stop", "stop", "pause"]:
            self.view.update("стоп")
            self._interrupt_all()
            return True
        return False

    def _interrupt_all(self):
        active_ops = self.repo.get_active_operations()
        for op in active_ops:
            op.status = "Stopped"
            op.result = "Interrupted by user"
            print(f"стоп по запросу: {op.record}")
            self.repo.add_entry(op)
        
        if not active_ops:
            print("нет операций")

    def register_operation(self, description: str):
        entry = OperationLogEntry(
            record_id=str(random.randint(1000, 9999)),
            record=description,
            status="Running",
            result="In Progress"
        )
        self.repo.add_entry(entry)