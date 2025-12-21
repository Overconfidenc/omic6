from command import PersonalizationCommand
from strategy import *
from controllers import PersonalizationController
from repositories import PersonalizationRepository
class ControllerFactory:
    def __init__(self):
        self.personalization_repo = PersonalizationRepository()

    def create_analysis_controller(self, strategy_type: str = "ml"):
        if strategy_type == "stat":
            strategy = StatisticalAnalysisStrategy()
        else:
            strategy = MLAnalysisStrategy()
        return AnalysisWrapper(strategy)

    def create_personalization_controller(self):
        return PersonalizationController(self.personalization_repo)

class AnalysisWrapper:
    def __init__(self, strategy: IAnalysisStrategy):
        self.strategy = strategy
    
    def process(self, text: str):
        print(f"анализ запроса: '{text}'")
        result = self.strategy.analyze(text)
        print(f"Intent: {result.intent}, Confidence: {result.confidence}, Params: {result.entities}")
        return result