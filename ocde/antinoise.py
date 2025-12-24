from entities import IAdaptiveAlgorithm

class SpectralSubtractionAlgorithm(IAdaptiveAlgorithm):
    """Алгоритм спектрального вычитания для шумных производств"""
    def apply_algorithm(self, audio_data: bytes) -> bytes:
        # Эмуляция сложной обработки сигнала
        print("   [NoiseFilter] Применение спектрального вычитания...")
        return b'cleaned_audio_data'

class DeepNoiseSuppressionAlgorithm(IAdaptiveAlgorithm):
    """Алгоритм на основе глубокого обучения"""
    def apply_algorithm(self, audio_data: bytes) -> bytes:
        print("   [NoiseFilter] Применение AI шумоподавления...")
        return b'ai_cleaned_data'