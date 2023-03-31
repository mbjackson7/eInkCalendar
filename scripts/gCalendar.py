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
from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime
import requests
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

logging.basicConfig(level=logging.DEBUG)
def init_credentials():
    with open(os.path.join(scriptsdir, 'config.json')) as json_file:
        config = json.load(json_file)   

    with open(os.path.join(scriptsdir, 'token.json')) as json_file:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(scriptsdir, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(scriptsdir, 'token.json'), 'w') as token:
            token.write(creds.to_json())
    return creds

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

def military_to_standard(time):
    if time[0:2] == "00":
        return "12" + time[2:] + " AM"
    elif time[0:2] == "12":
        return "12" + time[2:] + " PM"
    elif int(time[0:2]) > 12:
        return str(int(time[0:2]) - 12).zfill(2) + time[2:] + " PM"
    else:
        return time + " AM"

def get_event_list(width: int, height: int, x: int, y: int, red_Channel: ImageDraw, black_Channel: ImageDraw, font24, font18, font18bold):
    try:
        creds = init_credentials()
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 30 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=20, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        oldDate = ""
        color = False
        currY = y + 2
        eventX = black_Channel.textbbox((x+8, currY), "00:00 AM", font = font18)[2] + 8
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            date = start[5:10]
            if start[11:16]:
                time = military_to_standard(start[11:16])
            else:
                time = "All Day"
            summary = event['summary']
            printDate = False
            startY = currY
            if date != oldDate:
                oldDate = date
                color = not color
                printDate = True
                currY = black_Channel.textbbox((x+2, startY), date, font = font24)[3]
            eventY = currY
            currY = black_Channel.textbbox((x+8, currY), time, font = font18)[3] 
            formattedSummary = split_at_space(summary, width - eventX, font24, black_Channel)
            if black_Channel.textbbox((eventX, eventY), formattedSummary, font = font24)[3] > currY:
                currY = black_Channel.textbbox((eventX, eventY), formattedSummary, font = font24)[3]
            if currY <= height + y - 2:
                if printDate:
                    if color:
                        black_Channel.text((x+2, startY), date, font = font24, fill = 0)
                    else:
                        red_Channel.text((x+2, startY), date, font = font24, fill = 0)
                if color:
                    black_Channel.text((x+8, eventY), time, font = font18, fill = 0)
                    black_Channel.text((eventX, eventY), formattedSummary, font = font24, fill = 0)
                else:
                    red_Channel.text((x+8, eventY), time, font = font18, fill = 0)
                    red_Channel.text((eventX, eventY), formattedSummary, font = font24, fill = 0)
            currY += 5



    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5b_V2.epdconfig.module_exit()
        exit()
