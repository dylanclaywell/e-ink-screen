#!/usr/bin/python

import sys
import os
import yaml
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw

from weather import OpenWeather
from config import Config
from logger import Logger

with open('config.yaml', 'r') as stream:
    try:
        config = Config(yaml.safe_load(stream))
    except yaml.YAMLError as e:
        Logger.error(e)

wDir = config.getWaveshareDirectory()

libdir = os.path.join(wDir, 'RaspberryPi_JetsonNano/python/lib')
if os.path.exists(wDir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V3

apiKey, locations = config.getWeatherConfig()
weather = OpenWeather(apiKey, locations)

for location in locations:
    Logger.info(f"Adding location {location.get('name')} to list of weather locations")
    weather.add_location(location)

curWeather = weather.poll_location('fishers')

img = weather.get_weather_code_img(curWeather.get('weather')[0].get('icon'))

# early exit for testing things other than display
# exit()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

epd = epd2in13_V3.EPD()
epd.init()

# Clear screen
epd.Clear(0xFF)

# Create image
image = Image.new('1', (epd.height, epd.width), 255)

# Draw (paste) weather image onto image, using the weather image's alpha channel as a bitmask
image.paste(img, (10, 10), img)

# Display image
epd.display(epd.getbuffer(image))

# Sleep
epd.sleep()

