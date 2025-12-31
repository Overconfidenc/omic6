# container.py
from repositories import (
    SoundRepository, RequestRepository, DecisionRepository, 
    OperationRepository, PersonalizationRepository
)
from strategy import MLAnalysisStrategy
from inf import DeviceManager
from antinoise import SpectralSubtractionAlgorithm
from view import ConsoleStatusView
from controllers import (
    AnalysisController, OperationController, ResponseController, 
    PersonalizationController, DecisionController, RequestControllerWithNoiseCanceling
)
from state_manager import SystemStateManager 

class SystemConfigurator:
    def configure(self, ui_callback=None):
        state_manager = SystemStateManager(ui_callback)
        device_mgr = DeviceManager()
        view = ConsoleStatusView() 
        sound_repo = SoundRepository()
        req_repo = RequestRepository()
        dec_repo = DecisionRepository()
        op_repo = OperationRepository()
        pers_repo = PersonalizationRepository()
        noise_algo = SpectralSubtractionAlgorithm()
        analysis_strategy = MLAnalysisStrategy()
        req_ctrl = RequestControllerWithNoiseCanceling(state_manager, noise_algo, view)
        req_ctrl.sound_repo = sound_repo 
        req_ctrl.req_repo = req_repo
        ana_ctrl = AnalysisController(state_manager, req_repo, analysis_strategy)
        op_ctrl = OperationController(op_repo, view)
        dec_ctrl = DecisionController(state_manager, dec_repo, device_mgr)
        pers_ctrl = PersonalizationController(state_manager, pers_repo)
        res_ctrl = ResponseController(state_manager, pers_repo)
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
            "state_manager": state_manager,
            "device_manager": device_mgr
        }