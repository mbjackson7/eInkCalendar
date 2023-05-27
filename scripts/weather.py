#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/fonts')
weatherdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/weather')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
widgetdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'widgets')
scriptsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'scripts')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
from datetime import datetime
from dateutil import tz
from PIL import Image,ImageDraw,ImageFont
import PIL.ImageOps
import traceback
from datetime import datetime
import requests
import json

logging.basicConfig(level=logging.DEBUG)

def temp_string(temp: float, units: str):
    if units == "imperial":
        return f"{temp}°F"
    else:
        return f"{temp}°C"
    
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())

def get_weather_widget(width: int, height: int, x: int, y: int, colorChannels: dict, font48):
    try:   
        # load json file into a dictionary
        with open(os.path.join(scriptsdir, 'config.json')) as json_file:
            config = json.load(json_file)        

        apiURL = f"https://api.openweathermap.org/data/2.5/weather?lat={config['lat']}&lon={config['long']}&appid={config['weatherKey']}&units={config['units']}"
        response = requests.get(apiURL)
        data = response.json()
        
        xOffset = (width - 100) // 2
        
        if height >= 140:
            yOffset = (height - 140) // 2
        else:
            yOffset = (height - 40) // 2

        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        rawTempStr = str(temp)
        tempStr = f"{rawTempStr.split('.')[0]}°"
        tempLen = font48.getlength(tempStr)
        tempX = x + xOffset + (width - tempLen) // 2
        colorChannels["black"].text((tempX, yOffset + y), tempStr, font = font48, fill = 0)
        if height >= 140:
            if os.path.isfile(os.path.join(weatherdir, icon + ".bmp")):
                iconImg = Image.open(os.path.join(weatherdir, icon + ".bmp")).convert('L')
                iconImg = PIL.ImageOps.invert(iconImg)
                colorChannels["black"].bitmap((xOffset + x, yOffset + y + 40), iconImg, fill = 0)
            if os.path.isfile(os.path.join(weatherdir, icon + "r.bmp")):
                iconImg = Image.open(os.path.join(weatherdir, icon + "r.bmp")).convert('L')
                iconImg = PIL.ImageOps.invert(iconImg)
                colorChannels["red"].bitmap((xOffset + x, yOffset + y + 40), iconImg, fill = 0)
          
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5b_V2.epdconfig.module_exit()
        exit()

def get_forecast_widget(width: int, height: int, x: int, y: int, colorChannels: dict, font24):
    try:   
        # load json file into a dictionary
        with open(os.path.join(scriptsdir, 'config.json')) as json_file:
            config = json.load(json_file)        

        apiURL = f"https://api.openweathermap.org/data/2.5/forecast?lat={config['lat']}&lon={config['long']}&appid={config['weatherKey']}&units={config['units']}"
        response = requests.get(apiURL)
        data = response.json()

        rowCount = height // 140
        if rowCount == 0:
            rowCount = 1
        for r in range(rowCount):
            rowOffset = r * 140
            xOffset = (width % 100) / 2
            if height >= 140:
                yOffset = (height % 140) / 2
            else:
                yOffset = (height - 40) / 2
            num = width // 100
            numS = num * r
            numR = numS + num
            temp = 0
            icon = ""
            for i in range(numS, numR):
                temp = data['list'][i]['main']['temp']
                icon = data['list'][i]['weather'][0]['icon']
                dateStr = data['list'][i]['dt_txt']
                utc = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
                local = utc_to_local(utc)
                time = local.strftime("%I %p")
                if time[0] == "0":
                    time = time[1:]
                timeLen = font24.getlength(time)
                timeX = xOffset + (100 - timeLen) / 2
                colorChannels["black"].text((timeX + x, yOffset + y + rowOffset), time, font = font24, fill = 0)
                rawTempStr = str(temp)
                tempStr = f"{rawTempStr.split('.')[0]}°"
                tempLen = font24.getlength(tempStr)
                tempX = xOffset + (100 - tempLen) / 2
                colorChannels["black"].text((tempX + x, yOffset + y + 30 + rowOffset), tempStr, font = font24, fill = 0)
                if height >= 140:
                    if os.path.isfile(os.path.join(weatherdir, icon + ".bmp")):
                        iconImg = Image.open(os.path.join(weatherdir, icon + ".bmp")).convert('L')
                        iconImg = PIL.ImageOps.invert(iconImg)
                        colorChannels["black"].bitmap((xOffset + x, yOffset + y + 40 + rowOffset), iconImg, fill = 0)
                    if os.path.isfile(os.path.join(weatherdir, icon + "r.bmp")):
                        iconImg = Image.open(os.path.join(weatherdir, icon + "r.bmp")).convert('L')
                        iconImg = PIL.ImageOps.invert(iconImg)
                        colorChannels["red"].bitmap((xOffset + x, yOffset + y + 40 + rowOffset), iconImg, fill = 0)
                xOffset += 100
          
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        return