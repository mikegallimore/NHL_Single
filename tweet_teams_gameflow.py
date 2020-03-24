# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
from twython import Twython
import parameters
import pandas as pd
import json
import twitter_credentials

def parse_ids(season_id, game_id):

    ### pull common variables from the parameters file
    charts_teams = parameters.charts_teams
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    ### establish common filepaths
    livefeed_file = files_root + 'livefeed.json'
    
    ### post charts to Twitter
    APP_KEY = twitter_credentials.APP_KEY
    APP_SECRET = twitter_credentials.APP_SECRET
    OAUTH_TOKEN = twitter_credentials.OAUTH_TOKEN
    OAUTH_TOKEN_SECRET = twitter_credentials.OAUTH_TOKEN_SECRET
    
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    shots_gameflow = open(charts_teams + 'shots_gameflow.png', 'rb')
    shots_gameflow_5v5 = open(charts_teams + 'shots_gameflow_5v5.png', 'rb')
    shots_gameflow_xg = open(charts_teams + 'shots_gameflow_xg.png', 'rb')
    shots_gameflow_xg_5v5 = open(charts_teams + 'shots_gameflow_xg_5v5.png', 'rb')
    
    with open(livefeed_file) as livefeed_json:
        livefeed_data = json.load(livefeed_json)
       
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
    
    images = [shots_gameflow, shots_gameflow_5v5, shots_gameflow_xg, shots_gameflow_xg_5v5]
    
    media_ids = []
    
    for i in images:
        response = twitter.upload_media(media=i)
        media_ids.append(response['media_id_string'])
    
    if period == 1 and status != 'END':
        twitter.update_status(status= away + ' @ ' + home + ' (' + regulation_time_gone + ' into the 1st Period) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 1 and status == 'END':
        twitter.update_status(status= away + ' @ ' + home + ' (End of 1st Period) GameFlow for shots, xG:', media_ids=media_ids)
    
    if period == 2 and status != 'END':
        twitter.update_status(status= away + ' @ ' + home + ' (' + regulation_time_gone + ' into the 2nd Period) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 2 and status == 'END':
        twitter.update_status(status= away + ' @ ' + home + ' (End of 2nd Period) GameFlow for shots, xG:', media_ids=media_ids)
    
    if period == 3 and status != 'END' and status != 'Final':
        twitter.update_status(status= away + ' @ ' + home + ' (' + regulation_time_gone + ' into the 3rd Period) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 3 and status == 'END':
        twitter.update_status(status= away + ' @ ' + home + ' (End of 3rd Period) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 3 and status == 'Final':
        twitter.update_status(status= away + ' @ ' + home + ' (Final) GameFlow for shots, xG:', media_ids=media_ids)
    
    if period == 4 and status != 'END' and status != 'Final':
        twitter.update_status(status= away + ' @ ' + home + ' (' + ot_time_gone + ' into Overtime) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 4 and status == 'END':
        twitter.update_status(status= away + ' @ ' + home + ' (End of Overtime) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 4 and status == 'Final':
        twitter.update_status(status= away + ' @ ' + home + ' (Final) GameFlow for shots, xG:', media_ids=media_ids)
    
    if period == 5 and status != 'Final':
        twitter.update_status(status= away + ' @ ' + home + ' (End of Overtime) GameFlow for shots, xG:', media_ids=media_ids)
    elif period == 5 and status == 'Final':
        twitter.update_status(status= away + ' @ ' + home + ' (Final) GameFlow for shots, xG:', media_ids=media_ids)
    
        
    print('Tweeted GameFlow charts.')