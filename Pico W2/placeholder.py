from utime import sleep_ms
from machine import Pin
import network
import socket
import time

SSID = "Cassias"
PASSWORD = "%clave33422"

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

def LedSelect(_LED):
    if _LED == LED.LED0:
        led0.toggle()
    if _LED == LED.LED1:
        led1.toggle()
    elif _LED == LED.LED2:
        led2.toggle()
    elif _LED == LED.LED3:
        led3.toggle()
    elif _LED == LED.LED4:
        led4.toggle()
    elif _LED == LED.LED5:
        led5.toggle()
    elif _LED == LED.LED6:
        led6.toggle()
    elif _LED == LED.LED7:
        led7.toggle()
    elif _LED == LED.LED8:
        led8.toggle()
    elif _LED == LED.LED9:
        led9.toggle()

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
    energy = 0

    while True:
        data = conn.recv(1024)
        if not data:
            break
        energy = energy + int(data.decode())
        print("Tamanho recebido:", energy)

        if energy == -1:
            LedTurnOff()
            return
        # self.energy_led_limits = {"led": 0.75, "laptop": 1.0, "microwave": 8.33, "house_1min": 19.44, "eletric_car": 250.0, "dishwasher":1200.0, "house_1day": 28000.0}
        LedTurnOff()
        if energy >= 0.75:  #LED 5 min
            LedSelect(LED.LED0)
        sleep_ms(200)
        if energy >= 1.0:   #LAPTOP 5 min
            LedSelect(LED.LED1)
        sleep_ms(200)
        if energy >= 8.33:  #MICROWAVE
            LedSelect(LED.LED2)
        sleep_ms(200)
        if energy >= 19.44: #HOUSE_1MIN
            LedSelect(LED.LED3)
        sleep_ms(200)
        if energy >= 40:    #CELLPONE
            LedSelect(LED.LED4)
        sleep_ms(200)
        if energy >= 80:   #TOASTER
            LedSelect(LED.LED5)
        sleep_ms(200)
        if energy >= 250:   #ELETRIC CAR 1 MILE
            LedSelect(LED.LED6)
        sleep_ms(200)
        if energy >= 750:   #AIR CONDITIONING 1 HOUR
            LedSelect(LED.LED7)
        sleep_ms(200)
        if energy >= 1200:  #DISHWASHER 1 HOUR
            LedSelect(LED.LED8)
        sleep_ms(200)
        if energy >= 28000: #HOUSE 1 HOUR
            LedSelect(LED.LED9)

if __name__ == "__main__":
    main()