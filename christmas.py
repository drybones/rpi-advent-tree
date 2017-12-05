import datetime
import os
from signal import pause
from random import random
from gpiozero import LEDBoard

tree = LEDBoard(*[4, 15, 13, 21, 25, 8, 5, 10, 16, 17, 27, 26, 24, 9, 12, 6, 20, 19, 14, 18, 11, 7, 23, 22, 2], pwm=True, initial_value=False)

turn_on_time = datetime.time(hour=5, minute=30)
turn_off_time = datetime.time(hour=21, minute=30)
fade_duration = datetime.timedelta(minutes=30)

def fader(x, total):
    fraction = x / total
    return 0.01 ** (1-fraction) # Exponential fader from 0.01 to 1.0

def twinkle(led_day):
    while True:

        now = datetime.datetime.now()
        month = int(os.getenv('ADVENT_MONTH') or now.month)
        day = int(os.getenv('ADVENT_DAY') or now.day)

        on = datetime.datetime.combine(now.date(), turn_on_time)
        off = datetime.datetime.combine(now.date(), turn_off_time)

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
            if now < on or now > off:
                value = 0.0
            elif now < (on+fade_duration):
                value *= fader((now-on).total_seconds(), fade_duration.total_seconds())
            elif now > (off-fade_duration):
                value *= fader((off-now).total_seconds(), fade_duration.total_seconds())

        else:
            value = 0.0

        yield value

for index, led in enumerate(tree):
    led.source_delay = 0.1
    led.source = twinkle(index+1)

pause()
