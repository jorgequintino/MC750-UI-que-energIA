'''
user_input -> variavel que recebe a entrada do usuário
resposta_da_ia -> variavel que recebe a resposta da IA
consumo_energia -> variavel que recebe o consumo de energia da IA (dá pra tirar)

500 token = 375 words
'''


import customtkinter as ctk
from openai_utils import gerar_resposta, inicializar_cliente
from OpenAI.energy_calculation import calculate_cost
from audio_rec import interpretador_audio, microfone, transcreve_audio
import threading
import socket
import itertools

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UI que Delícia")
        self.geometry("1280x800")

        self.font_size = 22

        self.CONNECTED = False

        HOST = '192.168.149.126'  # Substitua pelo IP real do Pico W2
        PORT = 12345

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)  # Define um tempo limite de 5 segundos para a conexão
        print("Tentando conectar ao servidor no IP:", HOST, "e porta:", PORT)
        try:
            self.s.connect((HOST, PORT))
            self.CONNECTED = True
            print("Conectado ao servidor no IP:", HOST, "e porta:", PORT)
        except KeyboardInterrupt:
            print("Obrigado por usar o UI, que energIA!")
        except Exception:
            print("Erro ao conectar ao servidor. Verifique o IP e a porta.")

        self.gasto_energetico = ctk.DoubleVar()
        self.gasto_energetico_total = ctk.DoubleVar()
        self.gasto_energetico = 0
        self.gasto_energetico_total = 0

        self.title("UI que Delícia")
        self.geometry("1280x800")

        self.font_size = 22
        self.energy_led_limits = {"Acenda um LED por 5min: ": 0.75, 
                                  "Use um Notebook por 5min: ": 1.0, 
                                  "Use um Microondas por 30s: ": 8.33, 
                                  "Ligue uma Casa por 1min: ": 19.44, 
                                  "Carregue um Celular até 100%: ": 40, 
                                  "Use uma Torradeira por 3min: ": 80, 
                                  "Use um Carro Elétrico por 1.6km: ": 250.0,
                                  "Use um Ar Condicionado por 1h: ": 750, 
                                  "Use uma Lava-louças: ": 1200.0, 
                                  "Ligue uma casa por 1 dia: ": 28000.0,
                                  "Gaste toda a energia do mundo: ": 1000000.0}


        self.cliente = inicializar_cliente()

        # Área de mensagens rolável (estilo WhatsApp)
        self.chat_frame = ctk.CTkScrollableFrame(self, width=1200, height=500)
        self.chat_frame.pack(padx=20, pady=(20, 10), fill="both", expand=True)

        # Container inferior (entrada de texto + botão)
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(padx=20, pady=(0, 10), anchor="w")

        self.entry = ctk.CTkEntry(self.entry_frame, width=800, placeholder_text="Digite sua pergunta...", font=ctk.CTkFont(size=self.font_size))
        self.entry.pack(side="left", padx=(0, 10), pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(self.entry_frame, text="Enviar", command=self.send_message, font=ctk.CTkFont(size=self.font_size))
        self.send_button.pack(side="left", pady=10)

        # Botão de voz
        self.voice_button = ctk.CTkButton(self.entry_frame, width = 150, text="🎤 Falar", command=self.voice_input, font=ctk.CTkFont(size=self.font_size))
        self.voice_button.pack(side="left", padx=(10, 0), pady=10)

        # Adiciona o selecionador de quantidade de pessoas
        self.people_var = ctk.StringVar(value="1")
        self.people_selector = ctk.CTkOptionMenu(
            self.entry_frame,
            values=["1", "10", "100", "1000"],
            variable=self.people_var,
            width=100,
            font=ctk.CTkFont(size=self.font_size)
        )
        self.people_selector.pack(side="left", padx=(10, 10), pady=10)

        # Indicador visual do consumo de energia (barra)
        self.energy_stage = 0  # Índice do estágio atual
        self.consumo_energia = 0  # Consumo acumulado
        self.energy_label = ctk.CTkLabel(self, text=f"{list(self.energy_led_limits.keys())[self.energy_stage]}", font=ctk.CTkFont(size=self.font_size))

        self.energy_bar = ctk.CTkProgressBar(self, width=1250)
        self.energy_bar.set(0)
        self.energy_bar.pack(pady=5, padx=20, anchor="w")
        self.energy_label.pack(pady=(10, 0), anchor="w", padx=20)

        # Linha 2: Gasto energético total + da última mensagem
        consume_frame = ctk.CTkFrame(self)
        consume_frame.pack(pady=(10, 0), padx=20, anchor="w")

        self.energy_total_consume_label = ctk.CTkLabel(consume_frame, text=f"Gasto Energético Total: {round(self.gasto_energetico_total, 2)}", font=ctk.CTkFont(size=self.font_size))
        self.energy_total_consume_label.pack(side="left", padx=(0, 30))

        self.energy_consume_label = ctk.CTkLabel(consume_frame, text=f"Gasto Energético da Última Mensagem: {round(self.gasto_energetico, 2)}", font=ctk.CTkFont(size=self.font_size))
        self.energy_consume_label.pack(side="left")


    def update_energy_bar(self, gasto):
        self.consumo_energia += gasto
        chaves = list(self.energy_led_limits.keys())
        limite = list(self.energy_led_limits.values())[self.energy_stage]
        progresso = min(self.consumo_energia / limite, 1.0)
        self.energy_bar.set(progresso)
        # Atualiza o texto do label conforme o estágio
        self.energy_label.configure(text=f"{chaves[self.energy_stage]}")

        if self.consumo_energia >= limite:
            self.consumo_energia = 0
            self.energy_stage = min(self.energy_stage + 1, len(self.energy_led_limits) - 1)
            self.energy_bar.set(0)
            # Atualiza o texto do label para o próximo estágio
            self.energy_label.configure(text=f"{chaves[self.energy_stage]}")

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        prompt = user_input

        self.entry.delete(0, ctk.END)
        self.display_message(user_input, is_user=True)

        # Adiciona bolinha animada de carregando
        loading_label = ctk.CTkLabel(
            self.chat_frame,
            text="●",
            font=ctk.CTkFont(size=self.font_size + 10),
            text_color="green"
        )
        loading_label.pack(anchor="w", pady=5, padx=10)
        self.after(100, self.scroll_to_bottom)

        def animate_loading():
            colors = itertools.cycle(["green", "yellow", "red", "yellow"])
            def pulse():
                loading_label.configure(text_color=next(colors))
                loading_label.after(400, pulse)
            pulse()
        animate_loading()



        def process():
            resposta_da_ia, input_tokens, output_tokens = gerar_resposta(self.cliente, prompt)
            self.gasto_energetico = calculate_cost(input_tokens, output_tokens) * int(self.people_var.get())
            self.gasto_energetico_total += self.gasto_energetico
            self.energy_total_consume_label.configure(text=f"Gasto Energético Total: {round(self.gasto_energetico_total, 2)} Wh.")
            self.energy_consume_label.configure(text=f"Gasto Energético da Última Mensagem: {round(self.gasto_energetico, 2)} Wh.")

            loading_label.destroy()
            self.display_message(resposta_da_ia, is_user=False)
            self.update_energy_bar(self.gasto_energetico)
            self.enviar_numero(self.s, int(self.gasto_energetico))

        threading.Thread(target=process, daemon=True).start()

    def display_message(self, text, is_user=False):
        bg_color = "#0078D7" if is_user else "#E0E0E0"
        fg_color = "white" if is_user else "black"
        anchor = "e" if is_user else "w"

        msg_label = ctk.CTkLabel(
            self.chat_frame,
            text=text,
            font=ctk.CTkFont(size=self.font_size),
            text_color=fg_color,
            fg_color=bg_color,
            corner_radius=15,
            justify="left",
            wraplength=800,
            anchor="w",
            padx=10,
            pady=8
        )
        msg_label.pack(anchor=anchor, pady=5, padx=10)

        # Scroll automático após inserção
        self.after(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def voice_input(self):
        def run_voice():
            self.entry.delete(0, ctk.END)
            r = interpretador_audio()
            with microfone() as source:
                r.adjust_for_ambient_noise(source)
                self.voice_button.configure(text="🎤 Fale agora...", state="disabled")
                print("Fale algo...")
                audio = r.listen(source)
                self.voice_button.configure(text="⏳ Processando...", state="disabled")
            texto = transcreve_audio(r, audio)
            if texto:
                self.entry.insert(0, texto)
                self.send_message()
            self.voice_button.configure(text="🎤 Falar", state="normal")
        threading.Thread(target=run_voice, daemon=True).start()
    
    def enviar_numero(self, sock, numero):
        """
        Envia um número inteiro via socket como uma string codificada em bytes.
        """
        if self.CONNECTED == False:
            print("Não há dispositivo conectado.")
            return
        dados = str(numero).encode()  # Converte o número para string e depois para bytes
        sock.sendall(dados)


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
