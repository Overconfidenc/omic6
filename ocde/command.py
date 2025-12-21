from abc import ABC, abstractmethod
class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

class ClimateControlCommand(ICommand):

    def __init__(self, device_id: str, target_temp: int):
        self.device_id = device_id
        self.target_temp = target_temp
        self._prev_temp = 24 

    def execute(self) -> None:
        print(f"прибор: {self.device_id}. установка температуры до {self.target_temp}")

    def undo(self) -> None:
        print(f"прибор {self.device_id}] снижение температуры до {self._prev_temp}")

class TeaOrderCommand(ICommand):
    def __init__(self, robot_id: str, tea_type: str):
        self.robot_id = robot_id
        self.tea_type = tea_type

    def execute(self) -> None:
        print(f"робот {self.robot_id}]. заказ получен: {self.tea_type} чай")

    def undo(self) -> None:
        print(f"робот: {self.robot_id}. отмена заказа.")

class PersonalizationCommand(ICommand):
    def __init__(self, system_settings: dict, setting_key: str, new_value: any):
        self.settings = system_settings
        self.key = setting_key
        self.value = new_value
        self._prev_value = None

    def execute(self) -> None:
        self._prev_value = self.settings.get(self.key)
        self.settings[self.key] = self.value
        print(f"настройка '{self.key}' изменена на '{self.value}'")

    def undo(self) -> None:
        if self._prev_value:
            self.settings[self.key] = self._prev_value
            print(f"настройка '{self.key}' возвращена к '{self._prev_value}'")