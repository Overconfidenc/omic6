from entities import User
from antinoise import SpectralSubtractionAlgorithm
from inf import DeviceManager
from controllers import (
    RequestController, AnalysisController, MLAnalysisStrategy,
    OperationController, DecisionController, 
    PersonalizationController, ResponseController
)
from repositories import InMemoryRepository, PersonalizationRepository
from view import ConsoleView

class SystemApp:
    def __init__(self):
        # 1. Init Infrastructure
        self.view = ConsoleView()
        self.devices = DeviceManager()
        
        # 2. Init Repositories
        self.req_repo = InMemoryRepository()
        self.op_repo = InMemoryRepository()
        self.dec_repo = InMemoryRepository()
        self.pers_repo = PersonalizationRepository()

        # 3. Init Strategies & Algos
        self.noise_algo = SpectralSubtractionAlgorithm()
        self.analysis_strategy = MLAnalysisStrategy()

        # 4. Init Controllers (Dependency Injection)
        self.req_ctrl = RequestController(self.noise_algo, self.req_repo, self.view)
        self.ana_ctrl = AnalysisController(self.analysis_strategy)
        self.op_ctrl = OperationController(self.op_repo, self.view)
        self.dec_ctrl = DecisionController(self.dec_repo, self.devices)
        self.pers_ctrl = PersonalizationController(self.pers_repo)
        self.res_ctrl = ResponseController(self.pers_ctrl)

    def process_voice_command(self, user: User, audio_input: bytes, env_type: str, mock_text: str = None):
        print(f"\n--- Начало обработки команды для пользователя: {user.name} ---")
        
        # Шаг 1: Сбор и обработка аудио (Направление 1)
        if mock_text:
            request = self.req_ctrl.process_text_input(mock_text, user)
        else:
            request = self.req_ctrl.capture_and_process(audio_input, env_type, user)

        # Шаг 2: Анализ
        analysis_result = self.ana_ctrl.analyze(request)
        self.view.display(f"Распознано намерение: {analysis_result.intent} {analysis_result.entities}")

        # Шаг 3: Проверка безопасности и прерываний (Направление 2)
        is_stopped = self.op_ctrl.check_critical_and_log(analysis_result)
        if is_stopped:
            return # Прерываем выполнение

        # Шаг 4: Принятие решения и выполнение (BPMN Scenarios)
        decision = self.dec_ctrl.make_decision(analysis_result)

        # Шаг 5: Ответ пользователю с персонализацией (Направление 3)
        self.res_ctrl.respond(decision, user)


if __name__ == "__main__":
    app = SystemApp()

    # --- Сценарий A: Чай в шумном цеху (Демонстрация Направления 1) ---
    worker = User(id=1, name="Инженер Иванов", user_type="Specialist")
    raw_noise = b'loud_factory_noise'
    
    # Симуляция: пользователь говорит "хочу зеленый чай"
    app.process_voice_command(
        user=worker, 
        audio_input=raw_noise, 
        env_type="factory", 
        mock_text="система, принеси мне зеленый чай"
    )

    # --- Сценарий B: Экстренная остановка (Демонстрация Направления 2) ---
    app.process_voice_command(
        user=worker,
        audio_input=b'',
        env_type="normal",
        mock_text="СТОП"
    )

    # --- Сценарий C: Управление климатом с настройками голоса (Демонстрация Направления 3) ---
    home_user = User(id=2, name="Анна", user_type="SmartHomeUser") # У нее медленная скорость голоса в репозитории
    app.process_voice_command(
        user=home_user,
        audio_input=b'',
        env_type="normal",
        mock_text="установи температуру 24 градуса"
    )