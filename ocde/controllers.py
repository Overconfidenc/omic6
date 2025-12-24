import time
import re
from typing import List
# Note: pyttsx3 mock for environments without audio drivers
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

from entities import *

# --- Direction 1: Noise Canceling (Source 19) ---
class RequestController:
    def __init__(self, noise_algo: IAdaptiveAlgorithm, repo: IRepository, view: IView):
        self.algorithm = noise_algo
        self.repo = repo
        self.view = view

    def capture_and_process(self, raw_audio: bytes, env_type: str, user: User) -> Request:
        self.view.display(f"Получен аудиосигнал из среды: {env_type}")
        
        # Адаптивное применение алгоритма (Source 53)
        if env_type in ["factory", "construction", "noisy"]:
            processed_audio = self.algorithm.apply_algorithm(raw_audio)
        else:
            processed_audio = raw_audio
            print("   [Request] Шумоподавление не требуется")

        # Mock распознавания речи (т.к. нет реального микрофона)
        # Здесь мы симулируем перевод аудио в текст
        recognized_text = "система приготовь мне зеленый чай" # Default simulation
        
        req = Request(
            id=str(time.time()),
            raw_text=recognized_text, # В реальной системе здесь результат STT
            language="ru",
            accuracy=95,
            user_id=user.id
        )
        self.repo.save(req)
        return req
    
    # Метод для симуляции текстового ввода (для тестов)
    def process_text_input(self, text: str, user: User) -> Request:
         return Request(id=str(time.time()), raw_text=text, language="ru", accuracy=100, user_id=user.id)

# --- Analysis Logic (Source 13) ---
class MLAnalysisStrategy(IAnalysisStrategy):
    def analyze(self, text: str) -> AnalysisResult:
        text = text.lower()
        confidence = 0.9
        
        # Сценарий 1: Температура (Source 66)
        if "температур" in text or "градус" in text:
            intent = "control_climate"
            temp = int(re.search(r'\d+', text).group()) if re.search(r'\d+', text) else 22
            return AnalysisResult(intent, confidence, {"target_temp": temp})
            
        # Сценарий 2: Чай (Source 70)
        elif "чай" in text:
            intent = "order_drink"
            tea_type = "зеленый" if "зелен" in text else "черный"
            return AnalysisResult(intent, confidence, {"item": "tea", "type": tea_type})
        
        # Direction 2: Interrupts (Source 54)
        elif text in ["стоп", "пауза", "отмена", "stop"]:
            return AnalysisResult("emergency_stop", 1.0, {})

        return AnalysisResult("unknown", 0.0, {})

class AnalysisController:
    def __init__(self, strategy: IAnalysisStrategy):
        self.strategy = strategy
        
    def analyze(self, request: Request) -> AnalysisResult:
        return self.strategy.analyze(request.raw_text)

# --- Direction 2: Operations & Interrupts (Source 21) ---
class OperationController:
    def __init__(self, repo: IRepository, view: IView):
        self.repo = repo
        self.view = view

    def check_critical_and_log(self, analysis: AnalysisResult) -> bool:
        # Логирование операции
        op_entry = OperationLogEntry(
            record_id=str(time.time()),
            record=f"Intent: {analysis.intent}",
            status="Running"
        )
        self.repo.save(op_entry)

        # Обработка прерываний (Source 54)
        if analysis.intent == "emergency_stop":
            self.view.update("!!! ЭКСТРЕННАЯ ОСТАНОВКА !!!")
            self._stop_all_devices()
            op_entry.status = "Stopped"
            return True
            
        return False

    def _stop_all_devices(self):
        print("   [Operation] Отправка сигнала STOP всем контроллерам устройств...")

# --- Decision & Execution (BPMN Logic) ---
class DecisionController:
    def __init__(self, repo: IRepository, dev_mgr):
        self.repo = repo
        self.devices = dev_mgr

    def make_decision(self, analysis: AnalysisResult) -> Decision:
        decision = Decision("err", "none", "none", {}, "Не поняла команду")
        
        if analysis.intent == "control_climate":
            ac = self.devices.get_device("ac")
            temp = analysis.entities.get("target_temp")
            ac.execute_command("set_temp", {"temp": temp})
            decision = Decision(str(time.time()), "set_temp", "ac", {"temp": temp}, f"Устанавливаю температуру {temp} градусов")

        elif analysis.intent == "order_drink":
            kettle = self.devices.get_device("kettle")
            robot = self.devices.get_device("robot")
            
            # BPMN Logic: Check resources (Source 74)
            if kettle.water_level < 0.1:
                return Decision(str(time.time()), "error", "kettle", {}, "В чайнике мало воды")
            
            kettle.execute_command("boil", {"temp": 95})
            # Симуляция ожидания (Source 76)
            print("   [Process] Ожидание закипания...") 
            robot.execute_command("deliver", {"destination": "UserLocation"})
            
            decision = Decision(str(time.time()), "make_tea", "system", {}, "Ваш чай готовится и скоро будет доставлен")

        self.repo.save(decision)
        return decision

# --- Direction 3: Personalization (Source 23) ---
class PersonalizationController:
    def __init__(self, repo: IRepository):
        self.repo = repo
    
    def get_settings(self, user_id: int) -> UserProfile:
        profiles = self.repo.get_all()
        return profiles.get(user_id, UserProfile(user_id))

class ResponseController:
    def __init__(self, pers_ctrl: PersonalizationController):
        self.pers_ctrl = pers_ctrl
        self.engine = pyttsx3.init() if pyttsx3 else None

    def respond(self, decision: Decision, user: User):
        # Применение персонализации (Source 55)
        settings = self.pers_ctrl.get_settings(user.id)
        
        print(f"\n[АУДИО ОТВЕТ]: {decision.message}")
        print(f"   (Настройки голоса: Скорость={settings.voice_speed}, Громкость={settings.voice_volume})")

        if self.engine:
            try:
                self.engine.setProperty('rate', settings.voice_speed)
                self.engine.setProperty('volume', settings.voice_volume)
                # self.engine.say(decision.message) # Commented out to prevent blocking in non-audio envs
                # self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")