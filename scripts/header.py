#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime
import feedparser
import traceback
import time
from waveshare_epd import epd7in5b_V2
import logging
import sys
import os
picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic/fonts')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
widgetdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'widgets')
scriptsdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'scripts')
if os.path.exists(libdir):
    sys.path.append(libdir)


logging.basicConfig(level=logging.DEBUG)


def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


def split_at_space(s, width, font, channel):
    words = s.split()
    lines = []
    line = ''
    for word in words:
        if channel.textlength(line + ' ' + word, font) > width-4:
            lines.append(line)
            line = word
        else:
            line += ' ' + word
    lines.append(line)
    spaced_line = "\n".join(lines)
    spaced_line = spaced_line[1:]
    return spaced_line


def same_month_day(dt1, dt2):
    return dt1.month == dt2.month and dt1.day == dt2.day


def get_header_widget(width: int, height: int, x: int, y: int, red_Channel: ImageDraw, black_Channel: ImageDraw, font24, font18):
    try:
        with open(os.path.join(scriptsdir, 'config.json')) as json_file:
            config = json.load(json_file)
        currY = y + 2
        currTime = str(datetime.now())
        headerString = ""
        birthday = datetime.strptime(config['birthday'], "%m/%d/%Y")
        if same_month_day(datetime.now(), birthday):
            headerString = f"Happy {ordinal(datetime.now().year - birthday.year)} B-Day, {config['name']}!"
        else:
            if currTime[11:13] > "12":
                headerString = f"Good Afternoon, {config['name']}!"
            else:
                headerString = f"Good Morning, {config['name']}!"

        headerString = split_at_space(
            headerString, width, font24, black_Channel)
        print(headerString)
        textHeight = black_Channel.textsize(headerString, font=font24)[1]
        black_Channel.text((x+2, currY), headerString, font=font24, fill=0)
        currY += textHeight + 2
        #date and time string 
        datetimeStr = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        dateWidth, dateHeight = black_Channel.textsize(datetimeStr, font=font18)
        if dateWidth > width:
            datetimeStr = datetime.now().strftime("%A, %B %d, %Y")
            dateWidth, dateHeight = black_Channel.textsize(datetimeStr, font=font18)
        if dateWidth <= width and dateHeight + currY <= y + height:
            black_Channel.text((x+2, currY), datetimeStr, font=font18, fill=0)       

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5b_V2.epdconfig.module_exit()
        exit()
