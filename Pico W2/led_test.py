from machine import Pin
from utime import sleep_ms


ledWhite = Pin(0, Pin.OUT)
ledBlue = Pin(1, Pin.OUT)
ledGreen = Pin(2, Pin.OUT)
ledYellow = Pin(3, Pin.OUT)
ledRed  = Pin(4, Pin.OUT)

class LED(enumerate):
    WHITE = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    RED = 4

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
    # Setting LEDS to Low
    ledWhite.low()
    ledBlue.low()
    ledGreen.low()
    ledYellow.low()
    ledRed.low()

    i = 0
    print("LED Testing Started...")
    while i < 5:
        LedSelect(i)
        sleep_ms(1000)
        LedSelect(i)
        i += 1
    print("Finished.")

if __name__ == "__main__":
    main()