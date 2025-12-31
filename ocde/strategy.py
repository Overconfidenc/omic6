import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    intent: str
    confidence: float
    entities: Dict[str, Any]

class IAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, text: str) -> AnalysisResult:
        pass

class StatisticalAnalysisStrategy(IAnalysisStrategy):
    def analyze(self, text: str) -> AnalysisResult:
        text = text.lower()
        result = AnalysisResult(intent="unknown", confidence=0.0, entities={})
        if "температур" in text:
            result.intent = "control_climate"
            result.confidence = 0.7
            temp_match = re.search(r'\d+', text)
            if temp_match:
                result.entities["target_temp"] = int(temp_match.group())
                result.confidence = 0.9 
            
            if "уменьш" in text or "пониз" in text:
                result.entities["action"] = "decrease"
            elif "увелич" in text or "повыс" in text:
                result.entities["action"] = "increase"
        
        return result

class MLAnalysisStrategy(IAnalysisStrategy):
    def analyze(self, text: str) -> AnalysisResult:
        text = text.lower()
        if "чай" in text:
            tea_type = "зеленый" if "зелен" in text else "черный"
            return AnalysisResult(
                intent="order_drink", 
                confidence=0.95, 
                entities={"item": "tea", "type": tea_type}
            )
        
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