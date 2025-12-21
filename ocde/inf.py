from abc import ABC, abstractmethod

class IDevice(ABC):

    @property
    @abstractmethod
    def device_id(self) -> str:
        pass

    @property
    @abstractmethod
    def status(self) -> str:
        pass

    @abstractmethod
    def execute_command(self, command: str, params: dict) -> bool:
        pass


class SmartKettle:
    def __init__(self):
        self.water_level = 0.5 
    
    def get_water_level(self):
        return self.water_level

    def execute_command(self, cmd, params):
        print(f"чайник: выполнение {cmd} (параметры: {params})")
        return True

class DeliveryRobot(IDevice):
    def __init__(self, dev_id: str = "Robot_X5"):
        self._id = dev_id
        self._location = "DockingStation"
        self._battery = 85

    @property
    def device_id(self) -> str: return self._id

    @property
    def status(self) -> str:
        return "Ready" if self._battery > 10 else "Low Battery"

    def execute_command(self, command: str, params: dict) -> bool:
        if command == "deliver_from_kitchen":
            dest = params.get("destination", "LivingRoom")
            print(f"{self._id}:получена задача доставки в {dest}.")
            self._location = "Kitchen"
            return True
        return False

class AirConditioner(IDevice):
    def __init__(self, dev_id: str = "AC_LivingRoom"):
        self._id = dev_id
        self._current_temp = 26
        self._target_temp = 26

    @property
    def device_id(self) -> str: return self._id

    @property
    def status(self) -> str: return "Working"

    def execute_command(self, command: str, params: dict) -> bool:
        if command == "set_temp":
            target = params.get("temp")
            if target:
                self._target_temp = target
                print(f"{self._id}: установка температуры {target}°C.")
                return True
        return False

class DeviceManager:
    def __init__(self):
        self._devices = {
            "kettle": SmartKettle(),
            "robot": DeliveryRobot(),
            "ac_living_room": AirConditioner()
        }

    def get_device(self, alias: str) -> IDevice:
        return self._devices.get(alias)