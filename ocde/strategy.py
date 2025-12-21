import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

# Данные для обмена между слоями
@dataclass
class AnalysisResult:
    intent: str
    confidence: float
    entities: Dict[str, Any]

# --- Интерфейс Стратегии (Source 57) ---
class IAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, text: str) -> AnalysisResult:
        pass

# --- Реализация 1: Статистический анализ (ключевые слова) ---
class StatisticalAnalysisStrategy(IAnalysisStrategy):
    """
    Анализирует текст на основе жестких правил и регулярных выражений.
    Подходит для простых команд (Сценарий 1: Температура [cite: 43]).
    """
    def analyze(self, text: str) -> AnalysisResult:
        text = text.lower()
        result = AnalysisResult(intent="unknown", confidence=0.0, entities={})

        # Логика поиска температуры (Source 45)
        if "температур" in text:
            result.intent = "control_climate"
            result.confidence = 0.7
            # Извлечение числа
            temp_match = re.search(r'\d+', text)
            if temp_match:
                result.entities["target_temp"] = int(temp_match.group())
                result.confidence = 0.9 # Уверенность выше, если нашли параметр
            
            if "уменьш" in text or "пониз" in text:
                result.entities["action"] = "decrease"
            elif "увелич" in text or "повыс" in text:
                result.entities["action"] = "increase"
        
        return result

# --- Реализация 2: Стратегия Машинного Обучения (Эмуляция) ---
class MLAnalysisStrategy(IAnalysisStrategy):
    """Эмуляция ML-модели (ЛР 4, Направление 1)"""
    def analyze(self, text: str) -> AnalysisResult:
        text = text.lower()
        
        # Сценарий: Чай (ЛР 2, Image 10)
        if "чай" in text:
            # Имитируем извлечение сущностей нейросетью
            tea_type = "зеленый" if "зелен" in text else "черный"
            return AnalysisResult(
                intent="order_drink", 
                confidence=0.95, 
                entities={"item": "tea", "type": tea_type}
            )
        
        # Сценарий: Климат (ЛР 2, Image 8)
        if "температур" in text or "градус" in text:
            return AnalysisResult(
                intent="control_climate",
                confidence=0.9,
                entities={"target_temp": 22} 
            )

        return AnalysisResult(intent="unknown", confidence=0.1, entities={})
    
class MachineLearningStrategy(IAnalysisStrategy):
    def analyze_data(self, data: List[str]) -> None:
        print("ml анализ")

class StatisticalAnalysisStrategy(IAnalysisStrategy):
    def analyze_data(self, data: List[str]) -> None:
        print("анализ стат методами")