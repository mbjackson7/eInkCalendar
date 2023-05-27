import sys
import os
import json

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
scriptsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'scripts')
screenshotsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'screenshots')

with open(os.path.join(scriptsdir, 'config.json')) as json_file:
    config = json.load(json_file) 

TEST_MODE = config["testMode"]
VERSION = "v0.0.1"
SCREEN_ORIENTATION = "v"
EXPORT_SCREENSHOTS = TEST_MODE

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
if not TEST_MODE:
    from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import PIL.ImageOps
import traceback
from datetime import datetime


from news import get_news_widget
from weather import get_weather_widget, get_forecast_widget
from gCalendar import get_event_list, get_countdown_list
from header import get_header_widget

logging.basicConfig(level=logging.DEBUG)


try:
    print("Starting HUD")
    if not TEST_MODE:
        logging.info("Displaying HUD")
        epd = epd7in5b_V2.EPD()

        if SCREEN_ORIENTATION == "v":
            displayWidth = epd.height
            displayHeight = epd.width
        else:
            displayWidth = epd.width
            displayHeight = epd.height
    else:
        displayWidth = 480
        displayHeight = 800

    font24 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
    notoSans48 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 48)
    notoSans32 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 32)
    notoSans28 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 28)
    notoSans24 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 24)
    notoSans18 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 18)
    notoBold24 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedSemiBold.ttf'), 24)
    notoBold18 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedSemiBold.ttf'), 18)
    comicSans24 = ImageFont.truetype(os.path.join(fontdir, 'ComicSansMS/comic.ttf'), 24)
    comicSans18 = ImageFont.truetype(os.path.join(fontdir, 'ComicSansMS/comic.ttf'), 18)
    helvetica48 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 48)
    helvetica24 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 24)
    helvetica18 = ImageFont.truetype(os.path.join(fontdir, 'NotoSans/NotoSans-SemiCondensedMedium.ttf'), 18)

    Limage = Image.new('1', (displayWidth, displayHeight), 255)  # 255: clear the frame
    Limage_Other = Image.new('1', (displayWidth, displayHeight), 255)  # 255: clear the frame
    colorChannels = {
        "black": ImageDraw.Draw(Limage),
        "red": ImageDraw.Draw(Limage_Other),
    }
    
    logging.info("Prepping Widgets")
        

    colorChannels["black"].text((0, displayHeight-20), VERSION, font = helvetica18, fill = 0)
    get_header_widget(380, 80, 0, 0, colorChannels, notoSans28, helvetica18)
    get_news_widget(380, 160, 0, 80, colorChannels, helvetica24, helvetica24)
    get_weather_widget(100, 200, 380, 0, colorChannels, helvetica48)
    get_forecast_widget(100, 600, 380, 180, colorChannels, helvetica24)
    #get_countdown_list(380, 540, 0, 240, colorChannels, notoSans24, notoSans18, notoBold18, config["calendarID1"])
    get_event_list(380, 540, 0, 240, colorChannels, notoSans24, notoSans18, notoBold18)

    if not TEST_MODE:
        logging.info("Displaying")
        epd.init()
        epd.display(epd.getbuffer(Limage),epd.getbuffer(Limage_Other))

        logging.info("Goto Sleep...")
        epd.sleep()
    
    if EXPORT_SCREENSHOTS:
        logging.info("Exporting Image")
        blackMask = PIL.ImageOps.invert(Limage)
        redMask = PIL.ImageOps.invert(Limage_Other)
        canvas = Image.new('RGB', (displayWidth, displayHeight), (255, 255, 255))
        black = Image.new('RGB', (displayWidth, displayHeight), (0, 0, 0))
        red = Image.new('RGB', (displayWidth, displayHeight), (255, 0, 0))
        canvas.paste(black, mask=blackMask)
        canvas.paste(red, mask=redMask)
        canvas.save(os.path.join(screenshotsdir, f'{str("test")}.png'))
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    if not TEST_MODE:
        epd7in5b_V2.epdconfig.module_exit()
    exit()

except Exception as e:
    logging.info(e)
    print(e)
    input()
    if not TEST_MODE:
        epd7in5b_V2.epdconfig.module_exit()
    exit()