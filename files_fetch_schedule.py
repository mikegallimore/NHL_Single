# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 23:55:23 2018

@author: @mikegallimore
"""

import requests
import json
import csv
import pandas as pd
import parameters
import dict_teams

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
files_root = parameters.files_root

### create variables that point to the .csv processed stats files for players
JSON_schedule = files_root + season_id + "_schedule.json"
schedule_csv = files_root + season_id + "_schedule.csv"

### retrieve the JSON schedule information
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

###
### SCHEDULE (JSON)
###

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
                if JSON_game_id > 29999:
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
    ### reload the newly minted csv file to replace the team names with their tricodes
    schedule_df = pd.read_csv(schedule_csv)
 
    schedule_df = schedule_df[(schedule_df.GAME_ID > 20000)].sort_values('GAME_ID')
      
    schedule_df['AWAY'] = schedule_df['AWAY'].replace(dict_teams.NHL)
    schedule_df['HOME'] = schedule_df['HOME'].replace(dict_teams.NHL)
          
    schedule_df.to_csv(schedule_csv, index = False)

except:
    ### reload the newly minted csv file to replace the team names with their tricodes
    schedule_df = pd.read_csv(schedule_csv, encoding='latin-1')
    
    schedule_df = schedule_df[(schedule_df.GAME_ID > 20000)].sort_values('GAME_ID')
    
    schedule_df['AWAY'] = schedule_df['AWAY'].replace(dict_teams.NHL)
    schedule_df['HOME'] = schedule_df['HOME'].replace(dict_teams.NHL)
          
    schedule_df.to_csv(schedule_csv, index = False)
    
print('Finished parsing the NHL schedule for ' + season_id)