from utime import sleep_ms
from machine import Pin

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
    while True:
        inp = input().split()
        energy = int(inp[0])

        if energy == -1:
            LedTurnOff()
            return

        LedTurnOff()
        if energy >= 1:
            LedSelect(LED.LED0)
        sleep_ms(200)
        if energy >= 2:
            LedSelect(LED.LED1)
        sleep_ms(200)
        if energy >= 3:
            LedSelect(LED.LED2)
        sleep_ms(200)
        if energy >= 4:
            LedSelect(LED.LED3)
        sleep_ms(200)
        if energy >= 5:
            LedSelect(LED.LED4)
        sleep_ms(200)
        if energy >= 6:
            LedSelect(LED.LED5)
        sleep_ms(200)
        if energy >= 7:
            LedSelect(LED.LED6)
        sleep_ms(200)
        if energy >= 8:
            LedSelect(LED.LED7)
        sleep_ms(200)
        if energy >= 9:
            LedSelect(LED.LED8)
        sleep_ms(200)
        if energy >= 10:
            LedSelect(LED.LED9)

if __name__ == "__main__":
    main()