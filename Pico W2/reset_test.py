import machine
import time

# Configura o pino do botão (OUT do switch no GP10)
button = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN)
# Configura o LED onboard (geralmente GP25 no Pico W)
led = machine.Pin("LED", machine.Pin.OUT)

led_state = False
last_button_state = 0

while True:
    button_state = button.value()
    # Detecta transição de 0 para 1 (borda de subida)
    if button_state == 1 and last_button_state == 0:
        led_state = not led_state
        led.value(led_state)
    last_button_state = button_state
