import network
import time

SSID = "Cassias"
PASSWORD = "%clave33422"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Conectando ao Wi-Fi...")
    wlan.connect(SSID, PASSWORD)

    # Espera até conectar
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        print("Aguardando conexão...")
        time.sleep(1)
        max_wait -= 1

if wlan.isconnected():
    print("Conectado!")
    print("Endereço IP:", wlan.ifconfig()[0])
else:
    print("Falha ao conectar.")
