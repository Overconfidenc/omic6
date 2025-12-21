from abc import ABC, abstractmethod
from typing import Any

class IPresentation(ABC):
    @abstractmethod
    def display(self, data: Any) -> None:
        pass

    @abstractmethod
    def update(self, data: Any) -> None:
        pass

class ConsoleStatusView(IPresentation):
    def display(self, data: Any) -> None:
        print(f"\n дата: {data}")

    def update(self, data: Any) -> None:
        print(f"статус системы изменен: {data}")

class AudioVisualizationView(IPresentation):
    def display(self, data: Any) -> None:
        level = data.get("noise_level", "Unknown")
        print(f"уровень шума: [{'|' * 5}] ({level})")

    def update(self, data: Any) -> None:
        pass