from time import sleep, strftime
import time
import datetime
from gpiozero import CPUTemperature
import board
import neopixel
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 17 # Select relay GPIO Pin
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # Start GPIO off mode 

pixel_pin = board.D18 # Select Strip GPIO 
num_pixels = 3
ORDER = neopixel.RGB # Options RGB, GRB or RGBW, GRBW
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.04, auto_write=False, pixel_order=ORDER
)
# Comment this line out if you have RGBW/GRBW NeoPixels
pixels.fill((0, 0, 0)) # Seting off the strip for reset previus configuration
# Uncomment this line if you have RGBW/GRBW NeoPixels
# pixels.fill((0, 0, 0, 0))
pixels.show() # Run Leds config

cpu = CPUTemperature() # Call GPIO sensor Temp
# cpu.temperature # Get GPIO sensor data
# datetime.datetime.now() # Get current time

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
    for g in range(6):
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

def breath_color(color, actual_time):
    # Preset color set
    # ALERT! BRG in my Led Strip
    red = (0,255,34)
    orange = (0, 255, 157)
    ilde = (0,0,0)

    if color == "red":
        color_picker = red
    elif color == "orange":
        color_picker = orange
    else:
        color_picker = ilde

    # Night mode 12AM to 7AM turning off ligths
    if actual_time >= 0 and actual_time < 7 and color != "red":
        pixels.fill(ilde)
        pixels.show()

    # Turn ON ligths 
    else:
        # Range +
        for x in range(0, 100, 1):
            pixels.fill(color_picker)
            pixels.brightness = x/1000
            pixels.show()
            time.sleep(0.015)
        time.sleep(5)
        # Range -
        for x in range(100, 0,-1):
            pixels.fill(color_picker)
            pixels.brightness = x/1000
            pixels.show() 
            time.sleep(0.015)
        time.sleep(0.5)


rainbow_cycle(0.001)  # StarUp system Led Effect

while True:
    # Get current time
    now = datetime.datetime.now()

    #check GPIO CPU temperature
    if cpu.temperature > 45:
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
        breath_color("red", now.hour)
        time.sleep(10)
    else:
        print(now)
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) 
        breath_color("orange", now.hour)
        time.sleep(5)
