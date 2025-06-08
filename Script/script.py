from flask import Flask, request, render_template
import openai
import serial
import re



# === CONFIGURAÇÃO DO FLASK PARA ACESSAR ROTAS DO SERVIDOR WEB ===

app = Flask(__name__)

### CHAVE DE ACESSO A LLM ###

openai.api_key = "UI, que delicIA"

# Porta serial (ajustar conforme necessário)
try:
    serial_port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Linux/macOS
    # serial_port = serial.Serial('COM3', 9600, timeout=1)         # Windows
except serial.SerialException:
    serial_port = None
    print("⚠️ Porta serial indisponível.")

# === FLUXO DO SISTEMA EM FUNÇÕES CLARAS ===

# 1. Recebe mensagem da interface
def receber_comando_interface(req):
    return req.form.get('comando')

# 2. Envia a mensagem ao LLM
def enviar_llm(mensagem_usuario):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": mensagem_usuario}]
        )
        return resposta['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro ao acessar LLM: {str(e)}"

# 3. Processa resposta da LLM para extrair número
def extrair_numero_da_resposta(resposta_llm):
    nova_mensagem = {"Qual o valor em uma escala de 0 a 10 regulando a corrente em 10A,  vocẽ daria para essa mensagem?", resposta_llm}
    
    return float(enviar_llm(nova_mensagem))

# 4. Envia número ao circuito elétrico
def enviar_para_circuito(valor):
    if serial_port and serial_port.is_open:
        comando_serial = f"{valor}\n"
        serial_port.write(comando_serial.encode('utf-8'))
        print(f"✅ Enviado ao circuito: {comando_serial.strip()}")
    else:
        print("⚠️ Porta serial não conectada.")

# 5. Prepara os dados para mostrar na interface
def preparar_resposta_interface(resposta_llm):
    return render_template(
        'index.html',
        resposta=resposta_llm
    )

# === ROTAS DO FLASK ===

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    comando = receber_comando_interface(request)
    resposta_llm = enviar_llm(comando)
    valor_extraido = extrair_numero_da_resposta(resposta_llm)

    if valor_extraido is not None:
        enviar_para_circuito(valor_extraido)

    return preparar_resposta_interface(resposta_llm)

# === EXECUÇÃO ===

if __name__ == '__main__':
    app.run(debug=True)
