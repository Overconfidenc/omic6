from entities import UIState

class SystemStateManager:
    def __init__(self, view_callback=None):
        self._state = UIState.LOADING
        self._view_callback = view_callback
        self.notify_state()

    def set_callback(self, callback):
        self._view_callback = callback

    def change_state(self, new_state: UIState, meta_data: str = ""):
        print(f"[System State] Transition: {self._state.name} -> {new_state.name} ({meta_data})")
        self._state = new_state
        self.notify_state(meta_data)

    def notify_state(self, meta=""):
        if self._view_callback:
            self._view_callback(self._state, meta)

    @property
    def current_state(self):
        return self._state