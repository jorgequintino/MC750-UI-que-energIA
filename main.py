import socket
<<<<<<< HEAD
from flask import Flask, request, render_template

def gerar_resposta():
	return

# 5. Prepara os dados para mostrar na interface
def preparar_resposta_interface(resposta_llm):
    return render_template(
        'index.html',
        resposta=resposta_llm
    )
=======
import OpenAI
#import OpenAI.energy_calculation
import interface

def enviar_numero(sock, numero):
    """
    Envia um número inteiro via socket como uma string codificada em bytes.
    """
    dados = str(numero).encode()  # Converte o número para string e depois para bytes
    sock.sendall(dados)
>>>>>>> 77e30f05534464d4b439025d7b459b986164475d

def main():
    HOST = '192.168.15.16'  # Substitua pelo IP real do Pico W2
    PORT = 12345

    # Cria o socket cliente
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                user_input = input("Digite sua pergunta: ")
                if user_input == "sair":
                    break

                # Aqui você processa com OpenAI e obtém a resposta
                resposta = user_input[::-1]
                print("Resposta:", resposta)
                #tamanho = len(resposta)

<<<<<<< HEAD
				# Envia o tamanho da resposta para o Pico W2
				s.sendall(str(tamanho).encode())
	except KeyboardInterrupt:
		print("Obrigado por usar o UI, que energIA!")
	
	

	
=======
                # Usa a função para enviar o número
                numero = interface.ChatApp().gasto_energetico.get()
                enviar_numero(s, numero)

    except KeyboardInterrupt:
        print("Obrigado por usar o UI, que energIA!")
>>>>>>> 77e30f05534464d4b439025d7b459b986164475d

if __name__ == '__main__':
    main()
