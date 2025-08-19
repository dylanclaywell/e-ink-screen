#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
print(libdir)
if os.path.exists(libdir):
    sys.path.append(libdir)

import RPi.GPIO as GPIO
from waveshare_epd import epd2in13_V3
from PIL import Image, ImageDraw

# Optional: clean GPIO on start
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize display
epd = epd2in13_V3.EPD()
epd.init()

# Clear screen
epd.Clear(0xFF)

# Create image
image = Image.new('1', (epd.width, epd.height), 255)
draw = ImageDraw.Draw(image)
draw.text((10, 10), "Hello SPI 2.13 V3!", fill=0)

# Display image
epd.display(epd.getbuffer(image))

# Sleep
epd.sleep()


