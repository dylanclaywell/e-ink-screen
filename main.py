#!/usr/bin/python

import sys
import os
import yaml
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont

from weather import OpenWeather
from config import Config
from logger import Logger
from files import Files

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

# early exit for testing things other than display
# exit()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Logger.debug("Initializing EPD")

epd = epd2in13_V3.EPD()
epd.init()

Logger.debug("Clearing screen")

# Clear screen
epd.Clear(0xFF)

Logger.debug("Creating background image")

# Create image
image = Image.new('1', (epd.height, epd.width), 255)

# Draw weather
weather.draw(image)

Logger.debug("Loading PICO-8 shortcuts image")

# pico8shortcutsImage = Files.load_pico8_shortcut_image()
# image.paste(pico8shortcutsImage, (0, 0), pico8shortcutsImage)

Logger.debug("Displaying final image")

# Display image
epd.display(epd.getbuffer(image))

# Sleep
epd.sleep()

