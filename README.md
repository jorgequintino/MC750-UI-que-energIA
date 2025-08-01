# MC750-UI-que-energIA

O **UI que energIA!** integra uma LLM com uma calculadora de consumo baseada em tamanho dos prompts em respostas para indicar o gasto energético da sua interação. Será que aquele "Bom dia, chat!" vale a pena? Instale e descubra!

A proposta nasceu é um projeto da disciplina [MC750 - Construção de Interfaces Homem-Computador](https://www.dac.unicamp.br/portal/caderno-de-horarios/2025/1/S/G/IC/MC750) da Unicamp, em que o programa é integrado com uma maquete que indica de maneira interativa o gasto acumulado.

**Foto do projeto (pendente).**

## Autores
- [Ainaras Marão](https://github.com/MaraoLT)  (182338)
- [Douglas Henrique R. A. Pereira](https://github.com/Dourialp)  (245202)
- [Jorge Felipe L. Pereira](https://github.com/jorgequintino)  (251771)
- [Rafael Carro Gaudim](https://github.com/RafaelCarro)  (240879)
- [Yan Oliveira da Silva](https://github.com/Cl4nyz)  (236363)

## Como instalar

Instale as bibliotecas caso necessário:
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-tk
```

Abra o terminal e navegue até a pasta do seu projeto.
Crie a venv:
```bash
python3 -m venv .venv
```
Ative a venv:
```bash
source .venv/bin/activate
```
Instale os pacotes necessários:
```bash
pip3 install -r requirements.txt
```
Alternativamente, use:
```bash
pip3 install customtkinter python-dotenv numpy openai pyaudio pyttsx3 SpeechRecognition

```

### Configurando a API da OpenAI

1. Crie uma conta em [https://platform.openai.com/signup](https://platform.openai.com/signup).
2. Após criar sua conta, acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) e gere uma nova chave de API.
3. Copie o arquivo `.example.env` para `.env`:
   ```bash
   cp example.env .env
   ```
4. Abra o arquivo `.env` e cole sua chave de API no campo apropriado, por exemplo:
   ```
   OPENAI_API_KEY=sua-chave-aqui
   ```
5. Salve o arquivo `.env`. O programa irá carregar automaticamente sua chave ao rodar.

Pronto! Agora é só executar o programa `interface.py`!

### Configurando o PicoW2

1. Instale a extensão Raspberry Pi Pico
   1. Instale-a pela aba de extensões ou faça:
   ```bash
   ext install raspberry-pi.raspberry-pi-pico
   ```
   2. Alternativamente, use outa IDE com suporte a MicroPython da sua escolha
2. Flashe o firmware do Raspberry Pico W2:
   1. Aperte o botão de reset no Pico W2 e o mantenha pressionado
   2. Conecte-o ao computador via USB
   3. Solte o botão para habilitar o modo flash de firmware
   4. Abra o armazenamento interno do W2 e coloque o arquivo 'mp_firmware_unofficial_latest.uf2'
   5. O pico ira fechar a interface com o armazeno interno e ira flashar o firmware
3. Abra a pasta Pico W2 para rodar os codigos em MicroPython
4. Rode os arquivos necessários clicando em Run no menu inferior