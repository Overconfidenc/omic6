import random
from abc import ABC, abstractmethod
from view import IPresentation

class IAdaptiveAlgorithm(ABC):

    @abstractmethod
    def apply_algorithm(self, audio_data: bytes) -> bytes:
        pass



class SpectralSubtractionAlgorithm(IAdaptiveAlgorithm):

    def apply_algorithm(self, audio_data: bytes) -> bytes:

        return b'cleaned_audio_data'

class DeepNoiseSuppressionAlgorithm(IAdaptiveAlgorithm):

    def apply_algorithm(self, audio_data: bytes) -> bytes:
        return b'ai_cleaned_data'

class RequestControllerWithNoiseCanceling:

    def __init__(self, noise_algo: IAdaptiveAlgorithm, view: IPresentation):
        self.algorithm = noise_algo
        self.view = view

    def capture_and_process_audio(self, raw_input: bytes, environment_type: str):
        self.view.display("получение аудиосигналаlog")
        
        if environment_type == "noisy_factory":
            print("высокий уровень шума")
            cleaned_audio = self.algorithm.apply_algorithm(raw_input)
        else:
            cleaned_audio = raw_input
            print("шумоподавление не требуется")
            
        return cleaned_audio