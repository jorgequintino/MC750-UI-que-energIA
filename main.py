import socket
import OpenAI
#import OpenAI.energy_calculation
import interface

def enviar_numero(sock, numero):
    """
    Envia um número inteiro via socket como uma string codificada em bytes.
    """
    dados = str(numero).encode()  # Converte o número para string e depois para bytes
    sock.sendall(dados)

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

                # Usa a função para enviar o número
                numero = interface.ChatApp().gasto_energetico.get()
                enviar_numero(s, numero)

    except KeyboardInterrupt:
        print("Obrigado por usar o UI, que energIA!")

if __name__ == '__main__':
    main()
