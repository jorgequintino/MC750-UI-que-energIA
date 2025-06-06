from openai import OpenAI
import shelve
from dotenv import get_key
import os
import time
import logging
import io

#load_dotenv("example.env")
#OPENAI_API_KEY = get_key('.env', "OPENAI_API_KEY")
#OPENAI_ASSISTANT_ID = get_key('.env', "OPENAI_ASSISTANT_ID")

#cliente2 = OpenAI(
#    api_key = OPENAI_API_KEY
#)

def inicializar_cliente():
    api_key = get_key('.env', "OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key não encontrada. Verifique seu .env.")
    return OpenAI(api_key=api_key)

def gerar_resposta(cliente, input):
    response = cliente.responses.create(
        model="gpt-4.1-nano",
        input=input
    )
    return response.output_text



def main():
    cliente = inicializar_cliente()
    output = gerar_resposta(cliente, "Olá, tudo bem?")
    print(output)

if __name__ == "__main__":
    main()