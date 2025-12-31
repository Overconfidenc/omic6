import time
import threading
import random
import pyttsx3
import speech_recognition as sr
from entities import *
from repositories import *
from state_manager import SystemStateManager

class BaseController:
    def __init__(self, state_manager: SystemStateManager):
        self.sm = state_manager

class PersonalizationController(BaseController):

    def __init__(self, state_manager, repo: PersonalizationRepository):
        super().__init__(state_manager) 
        self.repo = repo
        self.current_settings = {}

    def load_settings_for_user(self, user_id: int):
        profile = self.repo.get_profile(user_id)
        self.current_settings = {
            "speed": profile.voice_speed,
            "volume": profile.voice_volume,
            "voice_id": getattr(profile, "voice_id", "default"),
            "temp": profile.preferred_temp
        }
        print(f"Профиль пользователя {user_id} применен: {self.current_settings}")

    def update_setting(self, user_id: int, key: str, value: Any):
        profile = self.repo.get_profile(user_id)
        
        # Обновляем поля профиля
        if key == "speed":
            profile.voice_speed = int(value)
        elif key == "volume":
            profile.voice_volume = float(value)
        elif key == "voice_id":
            profile.voice_id = str(value)
        elif key == "temp":
            profile.preferred_temp = int(value)
            
        self.repo.save_profile(profile)
        
        self.load_settings_for_user(user_id)
        print(f" Настройка '{key}' изменена на '{value}'")

class RequestController(BaseController):
    def __init__(self, state_manager, sound_repo: SoundRepository, req_repo: RequestRepository, noise_algo=None):
        super().__init__(state_manager)
        self.sound_repo = sound_repo
        self.req_repo = req_repo
        self.recognizer = sr.Recognizer()
        self.noise_algo = noise_algo
        self._is_listening = False

    def start_listening_loop(self, on_speech_captured):
        self._is_listening = True
        threading.Thread(target=self._listen, args=(on_speech_captured,), daemon=True).start()

    def _listen(self, callback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self._is_listening:
                if self.sm.current_state not in [UIState.PROCESSING, UIState.SPEAKING]:
                    self.sm.change_state(UIState.LISTENING)
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        self.sm.change_state(UIState.PROCESSING)
                        if self.noise_algo:
                            pass

                        sound_data = SoundData(id=int(time.time()), audio_source=audio, noise_level="Medium")
                        self.sound_repo.save(sound_data)
                        try:
                            text = self.recognizer.recognize_google(audio, language="ru-RU")
                            callback(text) 
                        except sr.UnknownValueError:
                            self.sm.change_state(UIState.IDLE, "Речь не распознана")
                        
                    except sr.WaitTimeoutError:
                        self.sm.change_state(UIState.IDLE)
                    except Exception as e:
                        self.sm.change_state(UIState.ERROR, str(e))

    def stop_listening(self):
        self._is_listening = False

class RequestControllerWithNoiseCanceling(BaseController):
    def __init__(self, state_manager, noise_algo, view):
        super().__init__(state_manager) 
        self.algorithm = noise_algo
        self.view = view
        self.recognizer = sr.Recognizer()
        self.sound_repo = None
        self.req_repo = None

    def capture_audio(self):
        with sr.Microphone() as source:
            self.sm.change_state(UIState.LISTENING, "Настройка фильтров")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.sm.change_state(UIState.LISTENING, "Слушаю")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                return audio
            except Exception:
                return None

    def process_to_text(self, audio):
        if not audio: return None
        try:
            self.sm.change_state(UIState.PROCESSING, "Распознавание")
            return self.recognizer.recognize_google(audio, language="ru-RU")
        except:
            return None

class AnalysisController(BaseController):
    def __init__(self, state_manager, req_repo, strategy):
        super().__init__(state_manager) 
        self.req_repo = req_repo
        self.strategy = strategy

    def analyze_request(self, request: Request) -> dict:
        self.sm.change_state(UIState.PROCESSING, "Анализ текста")
        result = self.strategy.analyze(request.raw_text)
        return {
            "intent": result.intent,
            "confidence": result.confidence,
            "params": result.entities
        }

class DecisionController(BaseController):
    def __init__(self, state_manager, decision_repo, device_manager):
        super().__init__(state_manager)
        self.repo = decision_repo
        self.devices = device_manager

    def make_decision(self, analysis_data: dict) -> Decision:
        intent = analysis_data.get("intent")
        params = analysis_data.get("params", {})
        
        action = "none"
        target = "system"
        msg = "Команда не понятна"

        if intent == "order_drink":
            kettle = self.devices.get_device("kettle")
            if kettle:
                kettle.execute_command("boil", {"temp": 95})
                action = "boil"
                target = "Kettle"
                msg = f"Чайник включен. {analysis_data['params'].get('type', '')} чай будет готов скоро."

        elif intent == "control_climate":
            ac = self.devices.get_device("ac_living_room")
            temp = params.get("target_temp", 22)
            if ac:
                ac.execute_command("set_temp", {"temp": temp})
                action = "set_temp"
                target = "AC"
                msg = f"Устанавливаю температуру на {temp} градусов."
        
        elif intent == "stop":
             action = "stop_all"
             msg = "Экстренная остановка всех устройств."
        
        decision = Decision(str(time.time()), action, target, params, msg)
        self.repo.save(decision)
        return decision

class ResponseController(BaseController):
    def __init__(self, state_manager, pers_repo):
        super().__init__(state_manager)
        self.pers_repo = pers_repo
        self.engine = pyttsx3.init()

    def execute_feedback(self, decision: Decision, user_id: int = 1):
        profile = self.pers_repo.get_profile(user_id)
        self.engine.setProperty('rate', profile.voice_speed)
        self.engine.setProperty('volume', profile.voice_volume)
        self.sm.change_state(UIState.SPEAKING, decision.message)
    
        print(f"\nсинтез: {decision.message}")
        try:
            self.engine.say(decision.message)
            self.engine.runAndWait()
        except:
            pass
    
        self.sm.change_state(UIState.IDLE)

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class OperationController(Subject):
    def __init__(self, repo, view):
        super().__init__()
        self.repo = repo
        self.view = view
        self.attach(view)

    def execute_critical_check(self, intent: str) -> bool:
        if intent in ["emergency_stop", "stop", "pause", "стоп", "пауза"]:
            self.view.display("крит. остановка")
            self._interrupt_all()
            return True
        return False

    def _interrupt_all(self):
        active_ops = self.repo.get_active_operations()
        for op in active_ops:
            op.status = "Stopped"
            print(f"Операция {op.record_id} прервана пользователем.")
        
        if not active_ops:
            print("Активных операций для остановки не найдено.")

    def register_operation(self, description: str):
        entry = OperationLogEntry(
            record_id=str(random.randint(1000, 9999)),
            record=description,
            status="Running",
            result="In Progress"
        )
        self.repo.add_entry(entry)