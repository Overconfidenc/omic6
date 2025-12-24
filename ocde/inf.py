from entities import IDevice

class SmartKettle(IDevice):
    def __init__(self):
        self._id = "Kettle_01"
        self.water_level = 0.5 
    
    @property
    def device_id(self): return self._id

    def execute_command(self, command: str, params: dict) -> bool:
        if command == "boil":
            print(f"   [Device] Чайник: Нагрев до {params.get('temp', 100)}°C")
            return True
        return False

class DeliveryRobot(IDevice):
    def __init__(self):
        self._id = "Robot_X5"
        self._location = "Dock"

    @property
    def device_id(self): return self._id

    def execute_command(self, command: str, params: dict) -> bool:
        if command == "deliver":
            dest = params.get("destination", "LivingRoom")
            print(f"   [Device] Робот: Доставка предмета в {dest}")
            self._location = dest
            return True
        return False

class AirConditioner(IDevice):
    def __init__(self):
        self._id = "AC_LivingRoom"
    
    @property
    def device_id(self): return self._id

    def execute_command(self, command: str, params: dict) -> bool:
        if command == "set_temp":
            temp = params.get("temp")
            print(f"   [Device] Кондиционер: Установка температуры {temp}°C")
            return True
        return False

class DeviceManager:
    def __init__(self):
        self._devices = {
            "kettle": SmartKettle(),
            "robot": DeliveryRobot(),
            "ac": AirConditioner()
        }

    def get_device(self, alias: str) -> IDevice:
        return self._devices.get(alias)