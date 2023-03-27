#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5b_V2 Demo")

    epd = epd7in5b_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("3.read bmp file")
    Himage = Image.open(os.path.join(picdir, 'bebop_b.bmp'))
    Himage_Other = Image.open(os.path.join(picdir, 'bebop_r.bmp'))
    epd.display(epd.getbuffer(Himage),epd.getbuffer(Himage_Other))
    time.sleep(2)

    # logging.info("4.read bmp file on window")
    # Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # Himage2_Other = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # bmp = Image.open(os.path.join(picdir, '2in9.bmp'))
    # Himage2.paste(bmp, (50,10))
    # Himage2_Other.paste(bmp, (50,300))
    # epd.display(epd.getbuffer(Himage2), epd.getbuffer(Himage2_Other))
    # time.sleep(2)

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit()
    exit()
