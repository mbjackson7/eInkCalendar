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
        first = True
        for listID in lists:
            if not first:
                colorChannels["black"].line([(currX, y), (currX, y + height)], fill = 0, width = 1)
            tempLen = font24.getlength(lists[listID]["name"])
            headerX = currX + (width // len(lists) - tempLen) // 2
            colorChannels["black"].text((headerX, currY), lists[listID]["name"], font = font24, fill = 0)
            currY += 36
            color = 'red'
            for card in lists[listID]["cards"]:
                cardShort = split_at_space(card, width // len(lists) - 4, font18, colorChannels[color])
                colorChannels[color].text((currX + 4, currY), cardShort, font = font18, fill = 0)
                for char in cardShort:
                    if char == "\n":
                        currY += 24
                        break
                currY += 30
                if currY > y + height:
                    break
                if color == 'black':
                    color = 'red'
                else:
                    color = 'black'
            currY = y
            currX += width // len(lists)
            first = False



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