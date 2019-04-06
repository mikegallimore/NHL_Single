# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 22:02:10 2018

@author: @mikegallimore
"""
from twython import Twython
import pandas as pd
import parameters
import json
import twitter_credentials

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
files_root = parameters.files_root
charts_teams = parameters.charts_teams

### establish common filepaths
livefeed_file = files_root + 'livefeed.json'

### pull schedule info; generate key values
schedule_csv = files_root + season_id + "_schedule.csv"

schedule_df = pd.read_csv(schedule_csv)
schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]

date = schedule_date['DATE'].item()
home = schedule_date['HOME'].item()
away = schedule_date['AWAY'].item()
teams = [away, home]

### post charts to Twitter
APP_KEY = twitter_credentials.APP_KEY
APP_SECRET = twitter_credentials.APP_SECRET
OAUTH_TOKEN = twitter_credentials.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = twitter_credentials.OAUTH_TOKEN_SECRET

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

shots_gameflow = open(charts_teams + 'shots_gameflow.png', 'rb')
shots_gameflow_5v5 = open(charts_teams + 'shots_gameflow_5v5.png', 'rb')

with open(livefeed_file) as livefeed_json:
    livefeed_data = json.load(livefeed_json)
    livefeed_parsed = livefeed_data
   
    period = livefeed_data["liveData"]["linescore"]["currentPeriod"]
    status = livefeed_data["liveData"]["linescore"]["currentPeriodTimeRemaining"]
    minutes_gone = int()
    seconds_gone = int()
    regulation_time_gone = str()
    ot_time_gone = str()

    try:
        time_left_split = status.split(':')
        regulation_minutes_gone = 20 - int(time_left_split[0])
        ot_minutes_gone = 5 - int(time_left_split[0])
        if int(time_left_split[1]) == 0 and int(time_left_split[1]) > 50:
            seconds_gone = 0 - int(time_left_split[0])
            seconds_gone = '0' + str(seconds_gone)
        elif int(time_left_split[1]) != 0 and int(time_left_split[1]) > 50:
            seconds_gone = 60 - int(time_left_split[1])
            seconds_gone = '0' + str(seconds_gone)
        regulation_time_gone = str(regulation_minutes_gone) + ':' + str(seconds_gone)
        ot_time_gone = str(ot_minutes_gone) + ':' + str(seconds_gone)
    except:
        pass

images = [shots_gameflow, shots_gameflow_5v5]

media_ids = []

for i in images:
    response = twitter.upload_media(media=i)
    media_ids.append(response['media_id_string'])

if period == 1 and status != 'END':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through ' + regulation_time_gone + ' of the 1st Period:', media_ids=media_ids)
elif period == 1 and status == 'END':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through the 1st Period:', media_ids=media_ids)

if period == 2 and status != 'END':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through ' + regulation_time_gone + ' of the 2nd Period:', media_ids=media_ids)
elif period == 2 and status == 'END':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through the 2nd Period:', media_ids=media_ids)

if period == 3 and status != 'END' and status != 'Final':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through ' + regulation_time_gone + ' of the 3rd Period:', media_ids=media_ids)
elif period == 3 and status == 'END':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through the 3rd Period:', media_ids=media_ids)
elif period == 3 and status == 'Final':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow (FINAL):', media_ids=media_ids)

if period == 4 and status != 'END' and status != 'Final':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through ' + ot_time_gone + ' of Overtime:', media_ids=media_ids)
elif period == 4 and status == 'END':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow through Overtime:', media_ids=media_ids)
elif period == 4 and status == 'Final':
    twitter.update_status(status= away + ' @ ' + home + ' gameflow (FINAL):', media_ids=media_ids)

if period == 5 and status != 'Final':
    twitter.update_status(status= away + ' @ ' + home + ' unit 5v5 on-ice shots through Overtime:', media_ids=media_ids)
elif period == 5 and status == 'Final':
    twitter.update_status(status= away + ' @ ' + home + ' unit 5v5 on-ice shots (FINAL):', media_ids=media_ids)

    
print('Tweeted the gameflow by game state.')