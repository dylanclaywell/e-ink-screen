#!/usr/bin/python

import sys
import os
import yaml
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw

from weather import OpenWeather

def getWaveshareDirectory():
    waveConfig = config.get('waveshare')
    if waveConfig is None:
        print('Waveshare entry missing from config; please check config.yaml')
        exit()

    waveDir = waveConfig.get('dir')
    if waveDir is None:
        print('Waveshare directory missing from config; please check config.yaml')
        exit()

    return waveDir

def getWeatherConfig():
    weatherConfig = config.get('weather')

    if weatherConfig is None:
        print('Weather entry missing from config; please check config.yaml')
        exit()

    apiKey = weatherConfig.get('apiKey')

    if apiKey is None:
        print('Weather API key missing from config; please check config.yaml')
        exit()

    locations = weatherConfig.get('locations')

    return apiKey, locations

with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)

wDir = getWaveshareDirectory()
print(wDir)

libdir = os.path.join(wDir, 'RaspberryPi_JetsonNano/python/lib')
if os.path.exists(wDir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V3

apiKey, locations = getWeatherConfig()
weather = OpenWeather(apiKey, locations)

for location in locations:
    print(f"Adding location {location.get('name')} to list of weather locations")
    weather.add_location(location)

weather.poll_location('fishers')

# early exit for testing things other than display
exit()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

epd = epd2in13_V3.EPD()
epd.init()

# Clear screen
epd.Clear(0xFF)

# Create image
image = Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(image)
draw.text((10, 10), "Hello SPI 2.13 V3!", fill=0)

# Display image
epd.display(epd.getbuffer(image))

# Sleep
epd.sleep()

