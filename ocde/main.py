import time
from container import SystemConfigurator
from entities import User, Request

def run_simulation():
    def ui_feedback(state, meta):
        print(f"\n[UI State: {state}] {meta}")

    config = SystemConfigurator().configure(ui_callback=ui_feedback)
    
    ctrls = config["controllers"]
    view = config["view"] 
    
    user = User(id=1, name="Специалист", user_type="Specialist")
    ctrls["personalization"].load_settings_for_user(user.id)
    
    raw_audio = b'noisy_factory_signal'
    view.display("Ожидание команды...")
    
    clean_audio = ctrls["request"].capture_and_process_audio(
        raw_audio, 
        environment_type="noisy_factory"
    )
    
    sim_req = Request(id="001", raw_text="Приготовь зеленый чай", language="ru", accuracy=95, user_id=user.id)
    
    analysis_res = ctrls["analysis"].analyze_request(sim_req)
    view.display(f"Распознан интент: {analysis_res['intent']}")

    if ctrls["operation"].execute_critical_check(analysis_res["intent"]):
        return

    decision = ctrls["decision"].make_decision(analysis_res)

    # 7. Вывод результата с учетом тембра и скорости (Персонализация)
    ctrls["response"].execute_feedback(decision)

if __name__ == "__main__":
    run_simulation()