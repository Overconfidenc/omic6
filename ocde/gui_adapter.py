from entities import IView
from typing import Any

class GUIAdapter(IView):
    """
    Мост между backend-системой и графическим интерфейсом.
    Позволяет контроллерам 'печатать' сообщения прямо в чат окна.
    """
    def __init__(self, ui_app):
        self.ui_app = ui_app

    def display(self, data: Any) -> None:
        # data может быть текстом или словарем с результатами
        if isinstance(data, str):
            self.ui_app.add_message(data, "System")
        else:
            # Для сложных объектов (например, AnalysisResult)
            self.ui_app.add_message(str(data), "Debug")

    def update(self, data: Any) -> None:
        self.ui_app.show_notification(f"Статус: {data}")