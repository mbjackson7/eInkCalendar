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

logging.basicConfig(level=logging.DEBUG)


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
    return spaced_line
def get_stories(width: int, height: int, x: int, y: int, red_Channel: ImageDraw, black_Channel: ImageDraw, font24, font18):
    try:   
        nyt_top_stories_url = 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
        nyt_politics_url = 'https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'
        nyt_world_url = 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'
        nyt_technology_url = 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'
        nyt_science_url = 'https://rss.nytimes.com/services/xml/rss/nyt/Science.xml'

        feeds = []
        stories = []
        # Fetch the RSS feed using feedparser
        feeds.append(feedparser.parse(nyt_top_stories_url))
        feeds.append(feedparser.parse(nyt_politics_url))
        feeds.append(feedparser.parse(nyt_technology_url))
        
        i = 0
        while len(stories) < 30:
            if feeds[i%3].entries[i//3].title not in stories:
                stories.append(feeds[i%3].entries[i//3].title)
            i += 1
            
        currY = y + 2
        currTime = str(datetime.now())
        headerString = "NYT " + currTime[:16]
        if black_Channel.textlength(headerString, font24) < width-4:
            black_Channel.text((x+2, currY), headerString, font = font24, fill = 0)
            currY += 36
        color = True
        for story in stories:
            title = split_at_space(story, width, font18, black_Channel)
            newBottom = black_Channel.multiline_textbbox((x+2, currY), title, font = font18)[3]
            if newBottom > y+height-2:
                break
            black_Channel.text((x+2, currY), title, font = font18, fill = 0)
            if color:
                red_Channel.text((x+2, currY), title, font = font18, fill = 0)
            currY = newBottom + 5
            color = not color
     
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5b_V2.epdconfig.module_exit()
        exit()
