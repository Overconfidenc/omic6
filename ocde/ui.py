import customtkinter as ctk
import threading
from main import SystemApp  # Импорт вашей системы из предыдущего шага
from entities import User
from gui_adapter import GUIAdapter

# Настройка темы (цвета как на макетах - фиолетовый/синий)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class SettingsWindow(ctk.CTkToplevel):
    """Окно настроек (Соответствует Source 6, 7, 8)"""
    def __init__(self, parent, pers_ctrl, user_id):
        super().__init__(parent)
        self.geometry("400x500")
        self.title("Настройки системы")
        self.pers_ctrl = pers_ctrl
        self.user_id = user_id
        
        # Получаем текущие настройки
        self.current_profile = self.pers_ctrl.get_settings(self.user_id)

        # Табы (Source 6)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_general = self.tabview.add("Основные")
        self.tab_style = self.tabview.add("Стиль")
        self.tab_commands = self.tabview.add("Спец. команды")

        self._build_general_tab()
        self._build_style_tab() # (Source 7)
        self._build_commands_tab() # (Source 8)

    def _build_general_tab(self):
        # Макет из Source 6
        self.sw_noise = ctk.CTkSwitch(self.tab_general, text="Подавление шума")
        self.sw_noise.pack(pady=10, anchor="w")
        self.sw_noise.select() # Включено по умолчанию для теста

        self.sw_emergency = ctk.CTkSwitch(self.tab_general, text="Экстренные команды")
        self.sw_emergency.pack(pady=10, anchor="w")
        self.sw_emergency.select()

    def _build_style_tab(self):
        # Макет из Source 7 (Персонализация)
        ctk.CTkLabel(self.tab_style, text="Скорость речи").pack(pady=(10,0), anchor="w")
        self.slider_speed = ctk.CTkSlider(self.tab_style, from_=50, to=300, command=self._update_speed)
        self.slider_speed.set(self.current_profile.voice_speed)
        self.slider_speed.pack(pady=5, fill="x")

        ctk.CTkLabel(self.tab_style, text="Громкость").pack(pady=(10,0), anchor="w")
        self.slider_vol = ctk.CTkSlider(self.tab_style, from_=0, to=1.0, command=self._update_volume)
        self.slider_vol.set(self.current_profile.voice_volume)
        self.slider_vol.pack(pady=5, fill="x")

    def _build_commands_tab(self):
        # Макет из Source 8
        self.entry_cmd = ctk.CTkEntry(self.tab_commands, placeholder_text="Новое служебное слово")
        self.entry_cmd.pack(pady=10, fill="x")
        ctk.CTkButton(self.tab_commands, text="Добавить слово").pack(pady=5)

    def _update_speed(self, value):
        # Обновление через контроллер персонализации
        self.current_profile.voice_speed = int(value)
        self.pers_ctrl.repo.save(self.current_profile)
        print(f"Speed updated to {int(value)}")

    def _update_volume(self, value):
        self.current_profile.voice_volume = float(value)
        self.pers_ctrl.repo.save(self.current_profile)

class DevicesWindow(ctk.CTkToplevel):
    """Окно управления устройствами (Соответствует Source 9)"""
    def __init__(self, parent, device_manager):
        super().__init__(parent)
        self.geometry("350x400")
        self.title("Управление устройствами")
        self.dev_mgr = device_manager
        
        ctk.CTkLabel(self, text="Подключенные устройства", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self._refresh_devices()

    def _refresh_devices(self):
        # Динамическое создание списка из DeviceManager
        for alias, device in self.dev_mgr._devices.items():
            frame = ctk.CTkFrame(self.scroll)
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(frame, text=device.device_id).pack(side="left", padx=10)
            ctk.CTkButton(frame, text="Удалить", width=60, fg_color="red", 
                          command=lambda d=alias: self._remove_device(d)).pack(side="right", padx=5)
            # Switch эмулирует вкл/выкл
            ctk.CTkSwitch(frame, text="").pack(side="right")

    def _remove_device(self, alias):
        print(f"Удаление устройства {alias} (Simulation)")
        # В реальной системе: self.dev_mgr.remove_device(alias)

class ChatApp(ctk.CTk):
    """Главное меню (Соответствует Source 5)"""
    def __init__(self):
        super().__init__()
        self.geometry("400x700")
        self.title("Голосовой помощник")
        
        # --- Инициализация Бэкенда ---
        self.system = SystemApp()
        # Подмена View на наш GUI адаптер
        self.gui_adapter = GUIAdapter(self)
        # Внедряем GUI адаптер во все контроллеры, где нужен View
        self.system.view = self.gui_adapter
        self.system.req_ctrl.view = self.gui_adapter
        self.system.op_ctrl.view = self.gui_adapter

        # Текущий пользователь (Hardcoded for demo)
        self.user = User(id=1, name="Admin", user_type="Specialist")

        # --- UI Layout ---
        
        # 1. Header (Фиолетовый градиент эмуляция)
        self.header = ctk.CTkFrame(self, height=60, fg_color="#4B0082", corner_radius=0)
        self.header.pack(fill="x", side="top")
        
        ctk.CTkLabel(self.header, text="Голосовой помощник", font=("Arial", 18, "bold"), text_color="white").pack(side="left", padx=15, pady=15)
        
        # Кнопки настроек в хедере
        btn_settings = ctk.CTkButton(self.header, text="⚙", width=30, command=self.open_settings, fg_color="transparent", border_width=1, text_color="white")
        btn_settings.pack(side="right", padx=10)
        
        btn_devices = ctk.CTkButton(self.header, text="📱", width=30, command=self.open_devices, fg_color="transparent", border_width=1, text_color="white")
        btn_devices.pack(side="right", padx=0)

        # 2. Chat Area
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Приветственное сообщение (Source 5)
        self.add_message("Привет! Я ваш голосовой помощник. Чем могу помочь?", "System")

        # 3. Input Area
        self.input_frame = ctk.CTkFrame(self, height=60, fg_color="white")
        self.input_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        
        self.entry_msg = ctk.CTkEntry(self.input_frame, placeholder_text="Введите сообщение...")
        self.entry_msg.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.entry_msg.bind("<Return>", lambda event: self.send_text())

        self.btn_send = ctk.CTkButton(self.input_frame, text="➤", width=40, command=self.send_text)
        self.btn_send.pack(side="right", padx=5)

        self.btn_mic = ctk.CTkButton(self.input_frame, text="🎤", width=40, fg_color="#4B0082", command=self.activate_voice)
        self.btn_mic.pack(side="right", padx=5)

        # Хранение ссылок на окна
        self.settings_window = None
        self.devices_window = None

    def add_message(self, text, sender):
        """Добавляет сообщение в чат"""
        align = "e" if sender == "User" else "w"
        color = "#DCF8C6" if sender == "User" else "#EAEAEA"
        text_color = "black"
        
        bubble = ctk.CTkLabel(
            self.chat_frame, 
            text=text, 
            fg_color=color, 
            text_color=text_color,
            corner_radius=10, 
            wraplength=250,
            padx=10, pady=5
        )
        bubble.pack(anchor=align, pady=5, padx=10)
        
        # Автопрокрутка вниз
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def show_notification(self, text):
        """Всплывающее уведомление (снизу)"""
        lbl = ctk.CTkLabel(self, text=text, fg_color="#333", text_color="white", corner_radius=5)
        lbl.place(relx=0.5, rely=0.85, anchor="center")
        self.after(3000, lbl.destroy)

    def send_text(self):
        text = self.entry_msg.get()
        if not text: return
        
        self.add_message(text, "User")
        self.entry_msg.delete(0, "end")
        
        # Запуск обработки в отдельном потоке, чтобы не морозить интерфейс
        threading.Thread(target=self._process_backend, args=(text, "normal")).start()

    def activate_voice(self):
        self.show_notification("Слушаю... (Симуляция шума)")
        # Эмуляция голосового ввода с шумом
        # Проверяем настройки, если окно настроек открыто
        is_noisy = "normal"
        if self.settings_window and self.settings_window.sw_noise.get() == 1:
            is_noisy = "factory" # Симуляция: если включено подавление, значит среда шумная
        
        # Симуляция распознанного текста
        simulated_voice_text = "система включи чайник" 
        self.add_message("🎤 " + simulated_voice_text, "User")
        
        threading.Thread(target=self._process_backend, args=(simulated_voice_text, is_noisy)).start()

    def _process_backend(self, text, env_type):
        """Связь с backend логикой"""
        # Эмуляция аудио-байтов
        dummy_audio = b'audio_data'
        
        # Вызов основного метода системы
        self.system.process_voice_command(
            user=self.user,
            audio_input=dummy_audio,
            env_type=env_type,
            mock_text=text
        )

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self, self.system.pers_ctrl, self.user.id)
        self.settings_window.focus()

    def open_devices(self):
        if self.devices_window is None or not self.devices_window.winfo_exists():
            self.devices_window = DevicesWindow(self, self.system.devices)
        self.devices_window.focus()

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()