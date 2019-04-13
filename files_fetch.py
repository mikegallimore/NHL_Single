# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 23:55:23 2018

@author: @mikegallimore
"""

import requests
import os
import csv
import json
import pandas as pd
import dict_teams
import parameters

def parse_ids(season_id, game_id):

    ### pull common variables from the parameters file
    files_root = parameters.files_root
    
    ### retrieve schedule
    schedule_csv = files_root + season_id + "_schedule.csv"
    schedule_exists = os.path.isfile(schedule_csv)
    
    if schedule_exists:
        print(season_id + ' schedule already exists')
    
    else:
        ### create variables that point to the .csv processed stats files for players
        JSON_schedule = files_root + season_id + "_schedule.json"
        schedule_csv = files_root + season_id + "_schedule.csv"
        
        ### find the .json schedule source and save to file
        try:    
            year_start = season_id[0:4]
            year_end = season_id[4:8]
        
            JSON_schedule_url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate=' + year_start + '-09-28&endDate=' + year_end + '-06-30'
            JSON_schedule_request = requests.get(JSON_schedule_url, timeout=5).text
        
            f = open(files_root + season_id + '_schedule.json', 'w+')
            f.write(JSON_schedule_request)
            f.close()
            print('Retrieved NHL schedule (JSON) for ' + season_id)
        except:
            print('ERROR: Could not retreive the season schedule (JSON) for ' + season_id)
        
        ### pull and parse the .json schedule file as .csv
        with open(JSON_schedule) as JSON_schedule_in:
            JSON_schedule_parsed = json.load(JSON_schedule_in)
        
            JSON_game_dates = JSON_schedule_parsed['dates']
        
            ### begin the portion of the script that handles the csv generation
            with open(schedule_csv, 'w', newline='') as schedule_out:
                JSON_csvWriter = csv.writer(schedule_out)
                
                JSON_csvWriter.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY'])
                
                for JSON_allgames in JSON_game_dates:
                    JSON_dates = JSON_allgames["date"]
                
                    JSON_games = JSON_allgames['games']
                
                    for JSON_game in JSON_games:
        
                        JSON_seasonid = JSON_game["season"]
                
                        JSON_game_id = str(JSON_game["gamePk"])[5:]
                        JSON_game_id = int(JSON_game_id)
                        ### skip any non-regular season games
                        if JSON_game_id > 39999:
                            continue
        
                        JSON_date = JSON_dates
                        JSON_date_split = JSON_date.split('-')
                        JSON_year = JSON_date_split[0]
                        JSON_month = JSON_date_split[1]
                        JSON_day = JSON_date_split[2]
                        JSON_date = JSON_month + '/' + JSON_day + '/' + JSON_year
                         
                        JSON_home = JSON_game["teams"]["home"]["team"]["name"].upper()
                        JSON_away = JSON_game["teams"]["away"]["team"]["name"].upper()
                           
                        JSON_game_data = (JSON_seasonid, JSON_game_id, JSON_date, JSON_home, JSON_away)
                           
                        ### write the rows of shifts to the csv file
                        JSON_csvWriter.writerows([JSON_game_data])
        
        try:
            ### reload the newly minted .csv file to replace the team names with their tricodes
            schedule_df = pd.read_csv(schedule_csv)
         
            schedule_df = schedule_df[(schedule_df.GAME_ID > 20000)].sort_values('GAME_ID')
              
            schedule_df['AWAY'] = schedule_df['AWAY'].replace(dict_teams.NHL)
            schedule_df['HOME'] = schedule_df['HOME'].replace(dict_teams.NHL)
                  
            schedule_df.to_csv(schedule_csv, index = False)
        
        except:
            ### reload the newly minted .csv file to replace the team names with their tricodes
            schedule_df = pd.read_csv(schedule_csv, encoding='latin-1')
            
            schedule_df = schedule_df[(schedule_df.GAME_ID > 20000)].sort_values('GAME_ID')
            
            schedule_df['AWAY'] = schedule_df['AWAY'].replace(dict_teams.NHL)
            schedule_df['HOME'] = schedule_df['HOME'].replace(dict_teams.NHL)
                  
            schedule_df.to_csv(schedule_csv, index = False)
            
        print('Finished parsing the NHL schedule for ' + season_id)
    
    
    
    ### retrieve HTM rosters
    try:
        ROS_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/RO0' + game_id + '.HTM', timeout=5).text
        if(len(ROS_content) < 10000):
            raise Exception
        f = open(files_root + 'rosters.HTM', 'w+')
        f.write(ROS_content)
        f.close()
        print('Retrieved NHL rosters (HTM) for ' + season_id + ' ' + game_id)
    except:
        print('ERROR: Could not retrieve NHL rosters (HTM) for ' + season_id + ' ' + game_id)
    
    ### retrieve HTM play-by-play
    try:
        PBP_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/PL0' + game_id + '.HTM', timeout=5).text
        if(len(ROS_content) < 10000):
            raise Exception
        f = open(files_root + 'pbp.HTM', 'w+')
        f.write(PBP_content)
        f.close()
        print('Retrieved NHL play-by-play (HTM) for ' + season_id + ' ' + game_id)
    except:
        print('ERROR: Could not retrieve NHL play-by-play (HTM) for ' + season_id + ' ' + game_id)
    
    ### retrieve HTM home shift charts
    try:
        TH0_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/TH0' + game_id + '.HTM', timeout=5).text
        if(len(TH0_content) < 10000):
            raise Exception
        f = open(files_root + 'shifts_home.HTM', 'w+')
        f.write(TH0_content)
        f.close()
        print('Retrieved NHL shifts (THO, HTM) for ' + season_id + ' ' + game_id)
    except:
        print('ERROR: Could not retrieve NHL shifts (THO, HTM) for ' + season_id + ' ' + game_id)
    
    ### retrieve HTM visitor shift charts
    try:
        TV0_content = requests.get('http://www.nhl.com/scores/htmlreports/' + season_id + '/TV0' + game_id + '.HTM', timeout=5).text
        if(len(TV0_content) < 10000):
            raise Exception
        f = open(files_root +'shifts_away.HTM', 'w+')
        f.write(TV0_content)
        f.close()
        print('Retrieved NHL shifts (TVI, HTM) for ' + season_id + ' ' + game_id)
    except:
        print('ERROR: Could not retrieve NHL shifts (TVI, HTM) for ' + season_id + ' ' + game_id)
    
    ### retrieve JSON livefeed
    try:
        JSON_content = requests.get('http://statsapi.web.nhl.com/api/v1/game/' + season_id[0:4] + '0' + game_id + '/feed/live', timeout=5).text
        if(len(JSON_content) < 1000):
            raise Exception
        f = open(files_root + 'livefeed.json', 'w+')
        f.write(JSON_content)
        f.close()
        print('Retrieved NHL livefeed (JSON) for ' + season_id + ' ' + game_id)
    except:
        print('ERROR: Could not retrieve NHL livefeed (JSON) ' + season_id + ' ' + game_id)
    
    ### retrieve JSON shifts
    try:
        JSON_content = requests.get('http://www.nhl.com/stats/rest/shiftcharts?cayenneExp=gameId=' + season_id[0:4] + '0' + game_id, timeout=5).text
        if(len(JSON_content) < 1000):
            raise Exception
        f = open(files_root + 'shifts.json', 'w+')
        f.write(JSON_content)
        f.close()
        print('Retrieved NHL shifts (JSON) for ' + season_id + ' ' + game_id)
    except:
        print('ERROR: Could not retrieve NHL shifts (JSON) for ' + season_id + ' ' + game_id)