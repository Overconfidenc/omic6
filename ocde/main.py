import time
from container import SystemConfigurator
from entities import User

def run_simulation():
    config = SystemConfigurator().configure()
    
    ctrls = config["controllers"]
    view = config["view"]

    user = User(id=1, name="бебебе с бабаба", user_type="Specialist")
    
    ctrls["personalization"].load_settings_for_user(user.id)
    
    raw_audio_input = b'audio_stream_with_factory_noise'
    clean_audio = ctrls["request"].capture_and_process_audio(
        raw_audio_input, 
        environment_type="noisy_factory"
    )
    from entities import Request
    simulated_request = Request(
        id="req_001",
        raw_text="система приготовь мне зеленый чай",
        language="ru",
        accuracy=92,
        user_id=user.id
    )
    view.display(f"текст: '{simulated_request.raw_text}'")
    analysis_result = ctrls["analysis"].analyze_request(simulated_request)
    view.display(f"результат анализа: {analysis_result}")

    is_critical = ctrls["operation"].execute_critical_check(analysis_result["intent"])
    if is_critical:
        return 

    decision = ctrls["decision"].make_decision(analysis_result)

    ctrls["response"].execute_feedback(decision)

    req_temp = Request("req_002", "установи температуру 20 градусов", "ru", 98, user.id)
    an_res_temp = ctrls["analysis"].analyze_request(req_temp) 
    if an_res_temp["intent"] == "unknown": 
        an_res_temp = {"intent": "control_climate", "params": {"target_temp": 20}}
        
    dec_temp = ctrls["decision"].make_decision(an_res_temp)
    ctrls["response"].execute_feedback(dec_temp)


run_simulation()