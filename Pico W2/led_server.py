import socket

def main():
    addr = socket.getaddrinfo('0.0.0.0', 12345)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Aguardando conexão...')
    conn, _ = s.accept()
    print('Conectado!')

    while True:
        data = conn.recv(1024)
        if not data:
            break
        tamanho = int(data.decode())
        print("Tamanho recebido:", tamanho)
        # Aqui você controla os LEDs conforme o tamanho

    conn.close()
    s.close()

main()