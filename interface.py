import customtkinter as ctk
from openai_utils import gerar_resposta, inicializar_cliente, gerar_resposta_com_historico
from OpenAI.energy_calculation import calculate_cost
from audio_rec import interpretador_audio, microfone, transcreve_audio
import threading
import socket
import itertools

DEFAULT_MESSAGE_ARRAY = [{"role": "system", "content": "Envie suas respostas em texto plano, NÃO utilize negrito e outras decorações de texto"}]
RESET = -1
CONTEXT_LIMIT = 6  # número de mensagens anteriores

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UI que Delícia")
        self.geometry("1280x850")

        self.font_size = 22
        self.CONNECTED = False

        HOST = '192.168.79.126'
        PORT = 12345

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        try:
            self.s.connect((HOST, PORT))
            self.CONNECTED = True
        except:
            print("Erro ao conectar ao servidor.")

        self.gasto_energetico_total = 0.0
        self.gasto_energetico = 0.0

        self.energy_led_limits = {
            "Acenda um LED por 5min: ": 0.75,
            "Use um Notebook por 5min: ": 1.0,
            "Use um Microondas por 30s: ": 8.33,
            "Ligue uma Casa por 1min: ": 19.44,
            "Carregue um Celular até 100%: ": 40,
            "Use uma Torradeira por 3min: ": 80,
            "Use um Carro Elétrico por 1.6km: ": 250.0,
            "Use um Ar Condicionado por 1h: ": 750,
            "Use uma Lava-louças: ": 1200.0,
            "Ligue uma casa por 1 dia: ": 28000.0,
            "Gaste toda a energia do mundo: ": 1000000.0
        }

        self.limits_sum = [sum(list(self.energy_led_limits.values())[:i+1]) for i in range(len(self.energy_led_limits))]
        self.labels = list(self.energy_led_limits.keys())
        self.milestones = self.limits_sum.copy()

        self.messages = DEFAULT_MESSAGE_ARRAY.copy()
        self.memory_on = True
        self.cliente = inicializar_cliente()

        self.chat_frame = ctk.CTkScrollableFrame(self, width=1200, height=500)
        self.chat_frame.pack(padx=20, pady=(20, 10), fill="both", expand=True)

        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(padx=20, pady=(0, 10), anchor="w")

        self.entry = ctk.CTkEntry(self.entry_frame, width=800, placeholder_text="Digite sua pergunta...", font=ctk.CTkFont(size=self.font_size))
        self.entry.pack(side="left", padx=(0, 10), pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.entry_frame, text="Enviar", command=self.send_message, font=ctk.CTkFont(size=self.font_size))
        self.send_button.pack(side="left", pady=10)

        self.voice_button = ctk.CTkButton(self.entry_frame, width=150, text="🎤 Falar", command=self.voice_input, font=ctk.CTkFont(size=self.font_size))
        self.voice_button.pack(side="left", padx=(10, 0), pady=10)

        self.people_var = ctk.StringVar(value="1")
        self.people_selector = ctk.CTkOptionMenu(
            self.entry_frame,
            values=["1", "10", "100", "1000"],
            variable=self.people_var,
            width=100,
            font=ctk.CTkFont(size=self.font_size)
        )
        self.people_selector.pack(side="left", padx=(10, 10), pady=10)

        self.reset_button = ctk.CTkButton(self.entry_frame, text="Reiniciar", command=self.reset, font=ctk.CTkFont(size=self.font_size))
        self.reset_button.pack(side="left", padx=(10, 0), pady=10)

        self.mem_switch = ctk.CTkSwitch(self.entry_frame, text="Memória ligada", command=self.toggle_memory, font=ctk.CTkFont(size=self.font_size))
        self.mem_switch.pack(side="left", padx=(10,0), pady=10)
        self.mem_switch.select()

        energy_bar_frame = ctk.CTkFrame(self)
        energy_bar_frame.pack(pady=(0, 10), padx=20, anchor="w", fill="x")

        self.left_milestone_label = ctk.CTkLabel(energy_bar_frame, text="Início", font=ctk.CTkFont(size=self.font_size))
        self.left_milestone_label.pack(side="left")

        self.energy_bar = ctk.CTkProgressBar(energy_bar_frame, width=1000)
        self.energy_bar.set(0)
        self.energy_bar.pack(side="left", expand=True, padx=(10, 10))

        self.right_milestone_label = ctk.CTkLabel(energy_bar_frame, text=list(self.energy_led_limits.keys())[0], font=ctk.CTkFont(size=self.font_size))
        self.right_milestone_label.pack(side="left")

        consume_frame = ctk.CTkFrame(self)
        consume_frame.pack(pady=(10, 0), padx=20, anchor="w")

        self.energy_total_consume_label = ctk.CTkLabel(consume_frame, text=f"Gasto Energético Total: {self.gasto_energetico_total:.4f}", font=ctk.CTkFont(size=self.font_size))
        self.energy_total_consume_label.pack(side="left", padx=(0, 30))

        self.energy_consume_label = ctk.CTkLabel(consume_frame, text=f"Gasto Energético da Última Mensagem: {self.gasto_energetico:.4f}", font=ctk.CTkFont(size=self.font_size))
        self.energy_consume_label.pack(side="left")

    def toggle_memory(self):
        self.memory_on = self.mem_switch.get()
        self.mem_switch.configure(text="Memória ligada" if self.memory_on else "Memória desligada")
        if not self.memory_on:
            self.messages = DEFAULT_MESSAGE_ARRAY.copy()

    def animate_progress(self, start: float, end: float, duration_ms: int = 500, callback=None):
        steps = int(duration_ms / 20)
        delta = (end - start) / steps if steps else 0
        def step(i=0, valor=start):
            if i >= steps:
                self.energy_bar.set(end)
                if callback:
                    callback()
                return
            valor += delta
            self.energy_bar.set(valor)
            self.after(20, lambda: step(i+1, valor))
        step()

    def update_energy_bar(self, gasto):
        prev_total = self.gasto_energetico_total - gasto
        new_total = self.gasto_energetico_total

        def get_stage_and_rel(total):
            for idx, m in enumerate(self.milestones):
                if total <= m:
                    prev = 0 if idx == 0 else self.milestones[idx-1]
                    rel = (total - prev) / (m - prev)
                    return idx, max(0.0, min(rel, 1.0))
            return len(self.milestones), 1.0

        old_stage, old_rel = get_stage_and_rel(prev_total)
        new_stage, new_rel = get_stage_and_rel(new_total)

        label_index = new_stage
        self.left_milestone_label.configure(text="Início" if label_index == 0 else self.labels[label_index - 1])
        self.right_milestone_label.configure(text=self.labels[label_index] if label_index < len(self.labels) else "Fim")

        segments = []
        for stage in range(old_stage, new_stage + 1):
            if stage == old_stage and stage == new_stage:
                segments.append((old_rel, new_rel))
            elif stage == old_stage:
                segments.append((old_rel, 1.0))
            elif stage == new_stage:
                segments.append((0.0, new_rel))
            else:
                segments.append((0.0, 1.0))

        def run_segment(i=0):
            if i >= len(segments): return
            start, end = segments[i]
            duration = int(abs(end - start) * 500) or 200
            self.animate_progress(start, end, duration_ms=duration, callback=lambda: run_segment(i + 1))

        run_segment()

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input: return
        self.entry.delete(0, ctk.END)
        self.display_message(user_input, is_user=True)

        if self.memory_on:
            context = self.messages[-CONTEXT_LIMIT*2:]
        else:
            context = DEFAULT_MESSAGE_ARRAY.copy()

        context.append({"role":"user","content":user_input})

        loading_label = ctk.CTkLabel(self.chat_frame, text="●", font=ctk.CTkFont(size=self.font_size+10), text_color="green")
        loading_label.pack(anchor="w", pady=5, padx=10)

        colors = itertools.cycle(["green", "yellow", "red", "yellow"])
        def pulse():
            try:
                loading_label.configure(text_color=next(colors))
                loading_label.after(400, pulse)
            except: pass
        pulse()

        threading.Thread(target=self._process_message, args=(context, loading_label), daemon=True).start()

    def _process_message(self, context, loading_label):
        resposta_da_ia, inp, outp = gerar_resposta_com_historico(self.cliente, context)
        if self.memory_on:
            self.messages.append({"role":"user","content":context[-1]["content"]})
            self.messages.append({"role":"assistant","content":resposta_da_ia})
        self.gasto_energetico = calculate_cost(inp, outp) * int(self.people_var.get())
        self.gasto_energetico_total += self.gasto_energetico

        loading_label.destroy()
        self.display_message(resposta_da_ia, is_user=False)
        self.energy_total_consume_label.configure(text=f"Gasto Energético Total: {self.gasto_energetico_total:.4f} Wh.")
        self.energy_consume_label.configure(text=f"Gasto Energético da Última Mensagem: {self.gasto_energetico:.4f} Wh.")
        self.update_energy_bar(self.gasto_energetico)
        self.enviar_numero(self.s, float(self.gasto_energetico))

    def display_message(self, text, is_user=False):
        bg_color = "#0078D7" if is_user else "#E0E0E0"
        fg_color = "white" if is_user else "black"
        anchor = "e" if is_user else "w"

        msg_label = ctk.CTkLabel(self.chat_frame, text=text, font=ctk.CTkFont(size=self.font_size), text_color=fg_color, fg_color=bg_color, corner_radius=15, justify="left", wraplength=800, anchor="w", padx=10, pady=8)
        msg_label.pack(anchor=anchor, pady=5, padx=10)
        self.after(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except: pass

    def voice_input(self):
        def run_voice():
            self.entry.delete(0, ctk.END)
            r = interpretador_audio()
            with microfone() as source:
                r.adjust_for_ambient_noise(source)
                self.voice_button.configure(text="🎤 Fale agora...", state="disabled")
                audio = r.listen(source)
                self.voice_button.configure(text="⏳ Processando...", state="disabled")
            texto = transcreve_audio(r, audio)
            if texto:
                self.entry.insert(0, texto)
                self.send_message()
            self.voice_button.configure(text="🎤 Falar", state="normal")
        threading.Thread(target=run_voice, daemon=True).start()

    def reset(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.messages = DEFAULT_MESSAGE_ARRAY.copy()
        self.gasto_energetico = 0
        self.gasto_energetico_total = 0
        self.energy_total_consume_label.configure(text=f"Gasto Energético Total: {self.gasto_energetico_total:.4f} Wh.")
        self.energy_consume_label.configure(text=f"Gasto Energético da Última Mensagem: {self.gasto_energetico:.4f} Wh.")
        self.update_energy_bar(self.gasto_energetico)
        self.enviar_numero(self.s, RESET)

    def enviar_numero(self, sock, numero):
        if not self.CONNECTED:
            print("Não há dispositivo conectado.")
            return
        dados = str(numero).encode()
        sock.sendall(dados)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
