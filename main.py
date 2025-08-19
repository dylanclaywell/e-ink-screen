#!/usr/bin/python

import sys
import os
import yaml

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

with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)

wDir = getWaveshareDirectory()
print(wDir)

