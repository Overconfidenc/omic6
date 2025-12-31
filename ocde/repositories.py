from entities import *

class SoundRepository(IRepository):
    def __init__(self): self.sounds = []
    def save(self, sound: SoundData): self.sounds.append(sound)
    def get_all(self): return self.sounds

class OperationRepository:
    def __init__(self):
        self._journal = []

    def add_entry(self, entry: OperationLogEntry):
        self._journal.append(entry)
        print(f"запись операции: {entry.record} [{entry.status}]")

    def get_active_operations(self):
        return [op for op in self._journal if op.status == "Running"]

class RequestRepository(IRepository):
    def __init__(self): self.requests = []
    def save(self, req: Request): self.requests.append(req)
    def get_all(self): return self.requests

class DecisionRepository(IRepository):
    def __init__(self): self.decisions = []
    def save(self, decision: Decision): self.decisions.append(decision)
    def get_last(self): return self.decisions[-1] if self.decisions else None

class ResponseRepository(IRepository):
    def __init__(self): self.responses = []
    def save(self, resp: Response): self.responses.append(resp)

class PersonalizationRepository:
    def __init__(self):
        self._profiles = {
            1: UserProfile(user_id=1, voice_speed=150, voice_volume=0.9),
            2: UserProfile(user_id=2, voice_speed=100, voice_volume=1.0) 
        }

    def get_profile(self, user_id: int) -> UserProfile:
        return self._profiles.get(user_id, UserProfile(user_id=user_id))

    def save_profile(self, profile: UserProfile):
        self._profiles[profile.user_id] = profile
        print(f"профиль пользователя {profile.user_id} сохранен")