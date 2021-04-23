#!/usr/bin/python3

from gpiozero import LED, Button
from pathlib import Path
from threading import Timer
import os

led = LED(5)
button = Button(13)

def touch_imalive_file():
    print("touching .rpi_roaster")
    p = Path(".rpi_roaster")
    p.touch()
    t = Timer(60.0, touch_imalive_file) # after 60s the file will be touched again
    t.start()

def on_button_press():
    led.on()
    # get_and_upload_roast_files
    t = Timer(2.0, led.off)
    t.start() # after 2 seconds, the led will be turned off

touch_imalive_file()
while True:
    if button.is_pressed and not led.is_lit:
            on_button_press()
