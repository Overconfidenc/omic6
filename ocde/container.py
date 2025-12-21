from repositories import *
from strategy import MLAnalysisStrategy
from controllers import *
from antinoise import SpectralSubtractionAlgorithm
from view import ConsoleStatusView

from repositories import *
from strategy import MLAnalysisStrategy
from inf import DeviceManager
from antinoise import SpectralSubtractionAlgorithm
from view import ConsoleStatusView

from controllers import (
    RequestControllerWithNoiseCanceling,
    AnalysisController,
    OperationController,
    ResponseController,
    PersonalizationController,
    DecisionController # Обновленный выше
)

class SystemConfigurator:
 
    def configure(self):
        print("проверка запуска систем")
        device_mgr = DeviceManager()
        sound_repo = SoundRepository()
        req_repo = RequestRepository()
        dec_repo = DecisionRepository()
        op_repo = OperationRepository()
        pers_repo = PersonalizationRepository()
        view = ConsoleStatusView()
        noise_algo = SpectralSubtractionAlgorithm()
        analysis_strategy = MLAnalysisStrategy()
        req_ctrl = RequestControllerWithNoiseCanceling(noise_algo, view)
        req_ctrl.sound_repo = sound_repo 
        req_ctrl.req_repo = req_repo
        ana_ctrl = AnalysisController(req_repo, analysis_strategy)
        op_ctrl = OperationController(op_repo, view)
        dec_ctrl = DecisionController(dec_repo, device_mgr)
        pers_ctrl = PersonalizationController(pers_repo)
        res_ctrl = ResponseController()

        print("конфигураци успешна")
        
        return {
            "controllers": {
                "request": req_ctrl,
                "analysis": ana_ctrl,
                "operation": op_ctrl,
                "decision": dec_ctrl,
                "personalization": pers_ctrl,
                "response": res_ctrl
            },
            "view": view,
            "device_manager": device_mgr
        }