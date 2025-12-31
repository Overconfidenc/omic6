import customtkinter as ctk
import threading
from container import SystemConfigurator

class VoiceChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OCDE - Voice Control System")
        self.geometry("450x600")
        ctk.set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.chat_frame = ctk.CTkScrollableFrame(self, label_text="Лог управления устройствами")
        self.chat_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.status_label = ctk.CTkLabel(self, text="Статус: инициализация", text_color="gray")
        self.status_label.grid(row=1, column=0, pady=5)
        self.mic_button = ctk.CTkButton(self, text="🎤 Нажать и говорить", 
                                       command=self.start_voice_thread,
                                       fg_color="#2c3e50", hover_color="#34495e")
        self.mic_button.grid(row=2, column=0, padx=20, pady=20)
        self.config = SystemConfigurator().configure(ui_callback=self.update_status_callback)
        self.ctrls = self.config["controllers"]

    def update_status_callback(self, state, meta=""):

        state_name = state.name if hasattr(state, 'name') else str(state)
        
        color = "white"
        if "PROCESSING" in state_name or "LISTENING" in state_name: 
            color = "#f1c40f" 
        elif "SPEAKING" in state_name: 
            color = "#2ecc71"
        elif "ERROR" in state_name:
            color = "#e74c3c" 
            
        self.status_label.configure(text=f"Статус: {state_name} {meta}", text_color=color)

    def add_message(self, sender, text, side="left"):
        anchor = "w" if side == "left" else "e"
        color = "#3d3d3d" if side == "left" else "#1a5276"
        msg = ctk.CTkLabel(self.chat_frame, text=f"{sender}: {text}", 
                           fg_color=color, corner_radius=10, padx=10, pady=5)
        msg.pack(anchor=anchor, pady=5, padx=10)

    def start_voice_thread(self):
        self.mic_button.configure(state="disabled")
        threading.Thread(target=self.run_real_voice_session, daemon=True).start()

    def run_real_voice_session(self):
        try:
            audio_data = self.ctrls["request"].capture_audio()
            command_text = self.ctrls["request"].process_to_text(audio_data)

            if command_text:
                self.add_message("Вы", command_text, "right")
                
                from entities import Request
                req = Request(id="v1", raw_text=command_text, language="ru", accuracy=100, user_id=1)

                analysis = self.ctrls["analysis"].analyze_request(req)

                # Проверка на СТОП
                if self.ctrls["operation"].execute_critical_check(analysis.get("intent", "")):
                    self.add_message("Система", "Критическая остановка!", "left")
                    return

                decision = self.ctrls["decision"].make_decision(analysis)
                self.add_message("Система", decision.message, "left")
                self.ctrls["response"].execute_feedback(decision)
            
            else:
                self.update_status_callback("IDLE", "(Тишина)")

        except Exception as e:
            self.add_message("Система", f"Ошибка: {e}", "left")
            self.update_status_callback("ERROR")
        finally:
            self.mic_button.configure(state="normal")

if __name__ == "__main__":
    app = VoiceChatApp()
    app.mainloop()