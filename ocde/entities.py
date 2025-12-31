from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class UIState(Enum):
    LOADING = "Загрузка"       
    IDLE = "Ожидание"           
    LISTENING = "Прослушивание"    
    PROCESSING = "Обработка"      
    SPEAKING = "Ответ"          
    ERROR = "Ошибка"           
    SETTINGS = "Настройки"       

@dataclass
class Response:
    id: str
    text: str
    language: str
    status: str = "generated"

@dataclass
class UserProfile:
    user_id: int
    voice_speed: int = 150
    voice_volume: float = 1.0
    voice_id: str = "default"   
    preferred_temp: int = 22

@dataclass
class AnalysisResult:
    intent: str
    confidence: float
    entities: Dict[str, Any]

@dataclass
class OperationLogEntry:
    record_id: str
    record: str
    status: str
    result: str
    timestamp: datetime = datetime.now()

@dataclass
class User:
    id: int
    name: str
    user_type: str

@dataclass
class SoundData:
    id: int
    audio_source: any
    noise_level: str

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

class IRepository:
    def save(self, item): raise NotImplementedError
    def get_all(self): raise NotImplementedError