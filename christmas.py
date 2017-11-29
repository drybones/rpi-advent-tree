import datetime
import os
from signal import pause
from random import random
from gpiozero import LEDBoard

tree = LEDBoard(*[4, 15, 13, 21, 25, 8, 5, 10, 16, 17, 27, 26, 24, 9, 12, 6, 20, 19, 14, 18, 11, 7, 23, 22, 2], pwm=True, initial_value=False)

def twinkle(led_day):
    while True:

        now = datetime.datetime.now()
        month = int(os.getenv('ADVENT_MONTH') or now.month)
        day = int(os.getenv('ADVENT_DAY') or now.day)
        hour = int(os.getenv('ADVENT_HOUR') or now.hour)
        minute = int(os.getenv('ADVENT_MINUTE') or now.minute)

        value = random() if led_day <= day else 0

        if month == 12:
            if day >= 25:
                if led_day == 25:
                    value = 1.0 # Light the star constantly
                else:
                    value *= 0.3 # Dim the brighter red LEDs to allow the star to shine
            else:
                value *= 0.6 # Dim the LEDs somewhat even when the start isn't lit

            # Turn the lights off overnight, fading in and out
            if hour <= 5 or hour >= 22:
                value = 0
            elif hour <= 6:
                value *= 0.3 ** ((60-minute)/10.0)
            elif hour >= 21:
                value *= 0.3 ** (minute/10.0)
        else:
            value = 0

        yield value

for index, led in enumerate(tree):
    led.source_delay = 0.1
    led.source = twinkle(index+1)

pause()
