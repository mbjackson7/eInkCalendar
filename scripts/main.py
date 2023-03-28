#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
widgetdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'widgets')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime

from news import get_news_widget
from weather import get_weather_widget, get_forecast_widget

logging.basicConfig(level=logging.DEBUG)

VERSION = "v0.0.1"
SCREEN_ORIENTATION = "v"

try:
    logging.info("Displaying HUD")

    epd = epd7in5b_V2.EPD()

    if SCREEN_ORIENTATION == "v":
        displayWidth = epd.height
        displayHeight = epd.width
    else:
        displayWidth = epd.width
        displayHeight = epd.height  

    font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
    notoSans48 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 48)
    notoSans24 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 24)
    notoSans18 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 18)

    Limage = Image.new('1', (displayWidth, displayHeight), 255)  # 255: clear the frame
    Limage_Other = Image.new('1', (displayWidth, displayHeight), 255)  # 255: clear the frame
    black_Channel = ImageDraw.Draw(Limage)
    red_Channel = ImageDraw.Draw(Limage_Other)
    
    logging.info("Prepping Widgets")
    black_Channel.text((0, displayHeight-20), VERSION, font = notoSans18, fill = 0)
    get_news_widget(380, 200, 0, 0, red_Channel, black_Channel, notoSans24, notoSans18)
    get_weather_widget(100, 200, 380, 0, red_Channel, black_Channel, notoSans48)
    get_forecast_widget(100, 600, 380, 200, red_Channel, black_Channel, notoSans24)
    

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("Displaying")
    epd.display(epd.getbuffer(Limage),epd.getbuffer(Limage_Other))

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit()
    exit()
