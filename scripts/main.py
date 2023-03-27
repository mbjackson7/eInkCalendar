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
import feedparser
from datetime import datetime

from nyt import get_stories

logging.basicConfig(level=logging.DEBUG)

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

    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
    notoSans24 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 24)
    notoSans18 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 18)

    Limage = Image.new('1', (displayWidth, displayHeight), 255)  # 255: clear the frame
    Limage_Other = Image.new('1', (displayWidth, displayHeight), 255)  # 255: clear the frame
    black_Channel = ImageDraw.Draw(Limage)
    red_Channel = ImageDraw.Draw(Limage_Other)
    
    logging.info("Prepping Widgets")
    get_stories(displayWidth, 200, 0, 0, red_Channel, black_Channel, notoSans24, notoSans18)

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
