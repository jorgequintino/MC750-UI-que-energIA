from utime import sleep_ms
from machine import Pin

class LED(enumerate):
    WHITE = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    RED = 4

ledWhite = Pin(0, Pin.OUT)
ledBlue = Pin(1, Pin.OUT)
ledGreen = Pin(2, Pin.OUT)
ledYellow = Pin(3, Pin.OUT)
ledRed  = Pin(4, Pin.OUT)

def LedTurnOff():
    ledWhite.low()
    ledBlue.low()
    ledGreen.low()
    ledYellow.low()
    ledRed.low()

def LedSelect(_LED):
    if _LED == LED.WHITE:
        ledWhite.toggle()
    elif _LED == LED.BLUE:
        ledBlue.toggle()
    elif _LED == LED.GREEN:
        ledGreen.toggle()
    elif _LED == LED.YELLOW:
        ledYellow.toggle()
    elif _LED == LED.RED:
        ledRed.toggle()

def main():
    while True:
        inp = input().split()
        energy = int(inp[0])

        if energy == -1:
            return

        LedTurnOff()
        if energy >= 1:
            LedSelect(LED.WHITE)
        sleep_ms(200)
        if energy >= 2:
            LedSelect(LED.BLUE)
        sleep_ms(200)
        if energy >= 3:
            LedSelect(LED.GREEN)
        sleep_ms(200)
        if energy >= 4:
            LedSelect(LED.YELLOW)
        sleep_ms(200)
        if energy >= 5:
            LedSelect(LED.RED)

if __name__ == "__main__":
    main()