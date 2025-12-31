from container import SystemConfigurator
from entities import User, UIState

class ApplicationViewModel:
    def __init__(self):
        self.configurator = SystemConfigurator()
        self.system = self.configurator.configure(ui_callback=self.on_state_changed)
        self.controllers = self.system["controllers"]
        self.current_user = User(id=1, name="Admin", user_type="Specialist")
        self.controllers["personalization"].load_settings_for_user(self.current_user.id)

    def on_state_changed(self, state: UIState, meta: str):

        print(f"GUI UPDATE -> State: {state.value} | Info: {meta}")

    def start_voice_control(self):
        self.controllers["request"].start_listening_loop(self.process_request)

    def process_request(self, text_command: str):
        print(f"GUI: Распознано: {text_command}")
        analysis = self.controllers["analysis"].analyze(text_command, self.current_user) 
        if analysis["intent"] == "stop":
            pass
        decision = self.controllers["decision"].make_decision(analysis)
        self.controllers["response"].speak(decision, self.current_user.id)

if __name__ == "__main__":
    app_vm = ApplicationViewModel()
    
    app_vm.start_voice_control()
    
    import time
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        app_vm.controllers["request"].stop_listening()