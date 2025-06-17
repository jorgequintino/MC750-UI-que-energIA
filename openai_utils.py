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
        instructions="Envie suas respostas em texto plano, NÃO utilize negrito e outras decorações de texto",
        input=input
    )
    return (response.output_text, response.usage.input_tokens, response.usage.output_tokens)

def gerar_resposta_com_historico(cliente, messages):
    response = cliente.chat.completions.create(
        model="gpt-4.1-nano",  # ou "gpt-4", "gpt-3.5-turbo"
        messages=messages
    )
    resposta_assistente = response.choices[0].message.content
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    return resposta_assistente, prompt_tokens, completion_tokens


def main():
    cliente = inicializar_cliente()
    output = gerar_resposta(cliente, "Olá, tudo bem?")
    print(output)

if __name__ == "__main__":
    main()