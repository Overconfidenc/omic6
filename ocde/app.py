from container import SystemConfigurator
from entities import Sound
class SystemApplication:

    def __init__(self):
        configurator = SystemConfigurator()
        self.container = configurator.configure()

    def run(self):
        
        req_ctrl = self.container.resolve("RequestController")
        ana_ctrl = self.container.resolve("AnalysisController")
        dec_ctrl = self.container.resolve("DecisionController")
        res_ctrl = self.container.resolve("ResponseController")
        fake_sound = Sound(id_sound=101, noise_level="Low", frequency=440)
        request = req_ctrl.form_request({}, fake_sound)
        decision_draft = ana_ctrl.conduct_analysis(request)
        final_decision = dec_ctrl.form_decision(decision_draft)
        response = res_ctrl.form_response(final_decision)
        
        print(f"=ответ: {response.message}")

app = SystemApplication()
app.run()