# RaspiMonitor_Python
A small status monitor written in python for raspberry pi 4 board, to control neopixel leds and extra fan.

## Materials

* KY-019 relay module or similar
* Adafruit neopixel Led strip or compatible
* 12v fan
* 12 power supply
* 320k resistor
* Dupont wire female - female x 3
* Dupont wire female - male x2
* Soldering iron
* Tin roll

## GIPO schematic

5v Fan_relay pin = 2
Ground Fan_relay pin = 6
Data relay_fan pin = 17

Led_data pin = 18
Led_ground pin = 14

## Script automation
`sudo crontab -e -u root`

add `sleep 60` to wait for the operating system to fully load

`@reboot sleep 60 &&  python3 /home/pi/temperature.py`
