#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/fonts')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
widgetdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'widgets')
scriptsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'scripts')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime
import requests
import json

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
    spaced_line = spaced_line[1:]
    return spaced_line

def shorten_string(s, width, font, channel):
    shortened = False
    while channel.textlength(s, font) >= width-4:
        shortened = True
        s = s[:-1]
    if shortened:
        while channel.textlength(s + "...", font) >= width-4:
            s = s[:-1]
    return s + "..." if shortened else s

def get_trello_board(width: int, height: int, x: int, y: int, colorChannels: dict, font24, font18, font18bold, boardID: str):
    try:
        board_data = requests.get(f"https://trello.com/b/{boardID}.json").json()
        lists = {}
        # Call the Calendar API
        for list in board_data["lists"]:
            lists[list["id"]] = {'name': list["name"], 'cards': []}
            
        for card in board_data["cards"]:
            lists[card["idList"]]["cards"].append(card['name'])
        
        # Prints the start and name of the next 10 events
        currY = y
        currX = x
        for listID in lists:
            colorChannels["black"].text((currX, currY), lists[listID]["name"], font = font18bold, fill = 0)
            currY += 24
            for card in lists[listID]["cards"]:
                cardShort = split_at_space(card, width // len(lists), font18, colorChannels["black"])
                colorChannels["black"].text((currX, currY), cardShort, font = font18, fill = 0)
                for char in cardShort:
                    if char == "\n":
                        currY += 18
                        break
                currY += 24
                if currY > y + height:
                    break
            currY = y
            currX += width // len(lists)



    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5b_V2.epdconfig.module_exit()
        exit()

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        return