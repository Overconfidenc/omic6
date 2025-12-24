from entities import IRepository, UserProfile

class InMemoryRepository(IRepository):
    def __init__(self):
        self._data = []
    def save(self, item):
        self._data.append(item)
    def get_all(self):
        return self._data

class PersonalizationRepository(IRepository):
    def __init__(self):
        self._profiles = {
            1: UserProfile(user_id=1, voice_speed=200, voice_volume=0.8), # Быстрая речь
            2: UserProfile(user_id=2, voice_speed=100, voice_volume=1.0)  # Медленная речь
        }
    def save(self, profile): self._profiles[profile.user_id] = profile
    def get_all(self): return self._profiles