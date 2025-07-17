from utime import sleep_ms
from machine import Pin
import network
import socket
import time

SSID = "RafaelCarro"
PASSWORD = "26112001"

class LED(enumerate):
    LED0 = 0
    LED1 = 1
    LED2 = 2
    LED3 = 3
    LED4 = 4
    LED5 = 5
    LED6 = 6
    LED7 = 7
    LED8 = 8
    LED9 = 9

led0 = Pin(0, Pin.OUT)
led1 = Pin(1, Pin.OUT)
led2 = Pin(2, Pin.OUT)
led3 = Pin(3, Pin.OUT)
led4 = Pin(4, Pin.OUT)
led5 = Pin(5, Pin.OUT)
led6 = Pin(6, Pin.OUT)
led7 = Pin(7, Pin.OUT)
led8  = Pin(8, Pin.OUT)
led9  = Pin(9, Pin.OUT)
reset = Pin(10, Pin.IN, Pin.PULL_DOWN)
led_onboard = Pin("LED", Pin.OUT)

def LedSelect(_LED):
    if _LED == LED.LED0:
        led0.on()
    if _LED == LED.LED1:
        led1.on()
    elif _LED == LED.LED2:
        led2.on()
    elif _LED == LED.LED3:
        led3.on()
    elif _LED == LED.LED4:
        led4.on()
    elif _LED == LED.LED5:
        led5.on()
    elif _LED == LED.LED6:
        led6.on()
    elif _LED == LED.LED7:
        led7.on()
    elif _LED == LED.LED8:
        led8.on()
    elif _LED == LED.LED9:
        led9.on()

def LedTurnOff():
    led0.low()
    led1.low()
    led2.low()
    led3.low()
    led4.low()
    led5.low()
    led6.low()
    led7.low()
    led8.low()
    led9.low()

def main():
    # Setup inicial
    LedTurnOff()  # Desliga todos os LEDs inicialmente
    led_onboard.on()  # Liga o LED onboard para indicar que o servidor está ativo

    last_button_state = reset.value()  # Estado inicial do botão

    # Wifi Connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Conectando ao Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Conectado! IP:", wlan.ifconfig()[0])

    # Cria socket servidor
    HOST = ''  # Escuta em todas as interfaces
    PORT = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    print(f"Aguardando conexão na porta {PORT}...")

    conn, addr = s.accept()
    print("Cliente conectado:", addr)
    energy_total = float(0)
    energy = float(0)
    conn.setblocking(False)  # Configura o socket para não bloquear
    last_energy_total = float(0)

    while True:
        if not wlan.isconnected():
            print("Wi-Fi desconectado. Encerrando o programa.")
            conn.close()
            s.close()
            break

        # Tenta receber dados, mas não trava se não houver nada
        try:
            data = conn.recv(1024)
            if data:
                energy = float(data.decode())
                if energy < 0.0:
                    energy_total = 0.0
                    LedTurnOff()
                #energy_total = energy_total + float(data.decode())
                energy_total = float(data.decode())
                print("Tamanho recebido:", energy_total)
        except OSError:
            pass  # Sem dados, segue o loop normalmente

        button_state = reset.value()
        if button_state == 1 and last_button_state == 0:
            print("Botão pressionado, resetando energia.")
            energy_total = -1.0  # Reseta a energia se o botão for pressionado
            last_button_state = 0
        last_button_state = button_state

        if last_energy_total != energy_total:
            if energy_total >= 0.75:
                LedSelect(LED.LED0)
                sleep_ms(200)
            if energy_total >= 1.75:
                LedSelect(LED.LED1)
                sleep_ms(200)
            if energy_total >= 10.08:
                LedSelect(LED.LED2)
                sleep_ms(200)
            if energy_total >= 29.52:
                LedSelect(LED.LED3)
                sleep_ms(200)
            if energy_total >= 69.52:
                LedSelect(LED.LED4)
                sleep_ms(200)
            if energy_total >= 149.52:
                LedSelect(LED.LED5)
                sleep_ms(200)
            if energy_total >= 399.52:
                LedSelect(LED.LED6)
                sleep_ms(200)
            if energy_total >= 1149.52:
                LedSelect(LED.LED7)
                sleep_ms(200)
            if energy_total >= 2349.52:
                LedSelect(LED.LED8)
                sleep_ms(200)
            if energy_total >= 30349.52:
                LedSelect(LED.LED9)
            if energy_total >= 1000000.0:
                LedSelect(LED.LED9)
        last_energy_total = energy_total

if __name__ == "__main__":
    main()