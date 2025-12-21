from entities import *
from repositories import *
from command import PersonalizationCommand
from inf import DeviceManager
import time
import pyttsx3
import speech_recognition as sr

class Subject:
    def __init__(self):
        self._observers = []
    def attach(self, observer):
        if observer not in self._observers: self._observers.append(observer)
    def notify(self, message):
        for observer in self._observers:
            for obs in self._observers: obs.update(message)

class RequestController:
    def __init__(self, sound_repo: SoundRepository, req_repo: RequestRepository):
        self.sound_repo = sound_repo
        self.req_repo = req_repo
        self.recognizer = sr.Recognizer()

    def capture_audio(self) -> SoundData:
        print("\nскажите запрос")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5)
        
        sound_data = SoundData(id=int(time.time()), audio_source=audio, noise_level="Low")
        self.sound_repo.save(sound_data)
        return sound_data

    def create_request_from_audio(self, user: User, sound: SoundData) -> Request:
        try:
            text = self.recognizer.recognize_google(sound.audio_source, language="ru-RU")
            req = Request(id=str(time.time()), raw_text=text, language="ru", accuracy=90, user_id=user.id)
            self.req_repo.save(req)
            return req
        except sr.UnknownValueError:
            return Request(id="err", raw_text="", language="ru", accuracy=0, user_id=user.id)

class AnalysisController:
    def __init__(self, req_repo, strategy):
        self.req_repo = req_repo
        self.strategy = strategy

    def analyze_request(self, request: Request) -> dict:
        result = self.strategy.analyze(request.raw_text)
        return {
            "intent": result.intent,
            "confidence": result.confidence,
            "params": result.entities
        }

class OperationController(Subject):
    def __init__(self, repo, view):
        super().__init__()
        self.repo = repo
        self.attach(view)

    def execute_critical_check(self, intent: str) -> bool:
        if intent in ["stop", "emergency_stop", "пауза"]:
            self.notify("крит. ошибка")
            return True
        return False

class DecisionController:
    def __init__(self, decision_repo: DecisionRepository, device_manager: DeviceManager):
        self.decision_repo = decision_repo
        self.devices = device_manager

    def make_decision(self, analysis_data: dict) -> Decision:
        intent = analysis_data.get("intent")
        params = analysis_data.get("params", {})
        
        # Реализация логики BPMN (Image 10 из ЛР 2)
        if intent == "order_drink":
            kettle = self.devices.get_device("kettle")
            # Проверка ресурсов (Gateway в BPMN)
            if kettle and kettle.get_water_level() < 0.1:
                return self._save_decision("error", "User", "нет воды")
            
            if kettle: kettle.execute_command("boil", {"temp": 95})
            return self._save_decision("brew_tea", "Kettle", "чайник включен")
        
        # Логика климата (Image 8 из ЛР 2)
        elif intent == "control_climate":
            ac = self.devices.get_device("ac_living_room")
            target = params.get("target_temp", 22)
            if ac: ac.execute_command("set_temp", {"temp": target})
            return self._save_decision("set_climate", "AC", f"температура установлена на {target} градусов.")

        return self._save_decision("unknown", "none", "команда не распознана.")

    def _save_decision(self, action, target, message):
        decision = Decision(id=str(time.time()), action_type=action, target_device=target, parameters={}, message=message)
        self.decision_repo.save(decision)
        return decision

class ResponseController:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) 

    def execute_feedback(self, decision: Decision):
        print(f"\n команда отправлена на {decision.target_device} -> {decision.action_type}")
        print(f"аудио ответ: {decision.message}")
        try:
            self.engine.say(decision.message)
            self.engine.runAndWait()
        except:
            pass # Если TTS не инициализирован

class PersonalizationController:
    def __init__(self, repo: PersonalizationRepository):
        self.repo = repo
        self.current_settings = {}

    def load_settings_for_user(self, user_id: int):
        profile = self.repo.get_profile(user_id)
        self.current_settings = {"speed": profile.voice_speed, "volume": profile.voice_volume}
        print(f"профиль пользователя {user_id} применен.")

    def update_setting(self, key: str, value: any):
        cmd = PersonalizationCommand(self.current_settings, key, value)
        cmd.execute()