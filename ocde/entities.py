from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List
from abc import ABC, abstractmethod

# --- Data Models (Source 12, 21, 23) ---

@dataclass
class UserProfile:
    user_id: int
    voice_speed: int = 150
    voice_volume: float = 1.0
    preferred_temp: int = 22

@dataclass
class User:
    id: int
    name: str
    user_type: str  # "Specialist", "SmartHomeUser", "Disabled" (Source 30)

@dataclass
class SoundData:
    id: int
    audio_source: bytes  
    noise_level: str
    environment_type: str = "normal"

@dataclass
class Request:
    id: str
    raw_text: str
    language: str
    accuracy: int
    user_id: int

@dataclass
class Decision:
    id: str
    action_type: str
    target_device: str
    parameters: dict
    message: str

@dataclass
class OperationLogEntry:
    record_id: str
    record: str  
    status: str  # "Running", "Stopped", "Completed"
    timestamp: datetime = datetime.now()

@dataclass
class AnalysisResult:
    intent: str
    confidence: float
    entities: Dict[str, Any]

# --- Interfaces (Source 15, 19) ---

class IRepository(ABC):
    @abstractmethod
    def save(self, item): pass
    @abstractmethod
    def get_all(self): pass

class IView(ABC):
    @abstractmethod
    def display(self, data: Any): pass
    @abstractmethod
    def update(self, data: Any): pass

class IDevice(ABC):
    @property
    @abstractmethod
    def device_id(self) -> str: pass
    @abstractmethod
    def execute_command(self, command: str, params: dict) -> bool: pass

class IAdaptiveAlgorithm(ABC): # (Source 19)
    @abstractmethod
    def apply_algorithm(self, audio_data: bytes) -> bytes: pass

class IAnalysisStrategy(ABC): # (Source 13)
    @abstractmethod
    def analyze(self, text: str) -> AnalysisResult: pass

class ICommand(ABC): # (Source 13)
    @abstractmethod
    def execute(self) -> None: pass
    @abstractmethod
    def undo(self) -> None: pass