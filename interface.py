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

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.CONNECTED = False

        HOST = '192.168.149.126'  # Substitua pelo IP real do Pico W2
        PORT = 12345

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(100)  # Define um tempo limite de 5 segundos para a conexão
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
        self.gasto_energetico.set(0)

        self.title("UI que Delícia")
        self.geometry("1280x800")

        self.font_size = 22

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
        self.voice_button = ctk.CTkButton(self.entry_frame, width = 220, text="🎤 Falar", command=self.voice_input, font=ctk.CTkFont(size=self.font_size))
        self.voice_button.pack(side="left", padx=(10, 0), pady=10)

        # Indicador visual do consumo de energia
        self.energy_label = ctk.CTkLabel(self, text="Consumo de energia:", font=ctk.CTkFont(size=self.font_size))
        self.energy_label.pack(pady=(10, 0), anchor="w", padx=20)
        self.energy_led_limits = {"led": 0.75, "laptop": 1.0, "microwave": 8.33, "cellphone": 40,"house_1min": 19.44, "toaster": 80, "eletric_car": 250.0, "AC": 750, "dishwasher":1200.0, "house_1day": 28000.0}
        self.energy_bar = ctk.CTkProgressBar(self, width=400)
        self.energy_bar.set(0)
        self.energy_bar.pack(pady=5, padx=20, anchor="w")
        self.cliente = inicializar_cliente()

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.entry.delete(0, ctk.END)
        self.display_message(user_input, is_user=True)

        # Placeholder da resposta da IA
        (resposta_da_ia, input_tokens, output_tokens) = gerar_resposta(self.cliente, user_input)
        self.gasto_energetico = calculate_cost(input_tokens, output_tokens)
        print(self.gasto_energetico)      #calculate_cost retorna em Wh
        
        consumo_energia = 0.4

        self.display_message(resposta_da_ia, is_user=False)
        self.energy_bar.set(consumo_energia)
        numero = int(self.gasto_energetico * 100)  # Multiplica por 10000 para enviar como inteiro
        self.enviar_numero(self.s, numero)  # Envia o consumo de energia multiplicado por 10000

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
        self.after(100, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

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
