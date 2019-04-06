# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 22:10:14 2018

@author: @mikegallimore
"""

import json
import pandas as pd
import parameters

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
files_root = parameters.files_root

### establish file locations and destinations
livefeed_parsed = files_root + 'livefeed.csv'
livefeed_source = files_root + 'livefeed.json'
pbp_parsed = files_root + 'pbp.csv'
rosters_parsed = files_root + 'rosters.csv'
shifts_parsed = files_root + 'shifts.csv'
TOI_outfile = files_root + 'TOI_matrix.csv'

### pull schedule info; generate key values
schedule_csv = files_root + season_id + "_schedule.csv"

schedule_df = pd.read_csv(schedule_csv)
schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]

date = schedule_date['DATE'].item()
home = schedule_date['HOME'].item()
away = schedule_date['AWAY'].item()
teams = [away, home]

### opens the game's livefeed (JSON) file to create a few shared variables
with open(livefeed_source) as livefeed_json:
    livefeed_data = json.load(livefeed_json)
   
    current_period = livefeed_data["liveData"]["linescore"]["currentPeriod"]
    current_time_remaining = livefeed_data["liveData"]["linescore"]["currentPeriodTimeRemaining"]
    try:
        time_remaining_min = int(current_time_remaining.split(':')[0])
        time_remaining_sec = int(current_time_remaining.split(':')[1])
    except:
        pass

    if current_period == 1 and current_time_remaining != 'END':
        current_seconds_gone = 1200 - ((time_remaining_min * 60) + time_remaining_sec)
    elif current_period ==1 and current_time_remaining == 'END':
        current_seconds_gone = 1200        
    if current_period == 2 and current_time_remaining != 'END':
        current_seconds_gone = 2400 - ((time_remaining_min * 60) + time_remaining_sec)
    elif current_period == 2 and current_time_remaining == 'END':
        current_seconds_gone = 2400
    if current_period == 3 and current_time_remaining != 'Final':
        current_seconds_gone = 3600 - ((time_remaining_min * 60) + time_remaining_sec)
    elif current_period == 4 and current_time_remaining != 'Final':
        current_seconds_gone = 3900 - ((time_remaining_min * 60) + time_remaining_sec)

###
### PLAY-BY-PLAY FROM LIVEFEED (CSV) & TOI MATRIX (CSV)
###

### reload both play-by-play files into pandas
pbp_df = pd.read_csv(pbp_parsed)
livefeed_df = pd.read_csv(livefeed_parsed)

### drop extraneous columns from the livefeed play-by-play dataframe; save the adjustments to file
livefeed_df = livefeed_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])
livefeed_df.to_csv(livefeed_parsed, index=False)

### join the contents of both play-by-play files
pbp_df = pd.merge(pbp_df, livefeed_df, on='SECONDS_GONE', how='left')

### rearrange the presentation of the X and Y columns from the end to roughly the middle of this merged play-by-play dataframe
move_zones_XY = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,41,42,26,27,28,43,44,45,46,29,30,31,32,33,34,35,36,37,38,39,40]
pbp_df = pbp_df[pbp_df.columns[move_zones_XY]]

### add zone and XY info to faceoffs that are missing it
pbp_df['PREV_HOME_ZONE'] = pbp_df['HOME_ZONE'].shift(1)
pbp_df['PREV_AWAY_ZONE'] = pbp_df['AWAY_ZONE'].shift(1)
pbp_df['PREV_X_1'] = pbp_df['X_1'].shift(1)
pbp_df['PREV_Y_1'] = pbp_df['Y_1'].shift(1)

pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.HOME_ZONE != 'Defensive') & (pbp_df.HOME_ZONE != 'Neutral') & (pbp_df.HOME_ZONE != 'Offensive'),['HOME_ZONE']] = pbp_df['PREV_HOME_ZONE']; pbp_df
pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.AWAY_ZONE != 'Defensive') & (pbp_df.AWAY_ZONE != 'Neutral') & (pbp_df.AWAY_ZONE != 'Offensive'),['AWAY_ZONE']] = pbp_df['PREV_AWAY_ZONE']; pbp_df

pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.X_1.isnull() == True),['X_1']] = pbp_df['PREV_X_1']; pbp_df
pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.Y_1.isnull() == True ),['Y_1']] = pbp_df['PREV_Y_1']; pbp_df

### drop now-extraneous columns
pbp_df = pbp_df.drop(columns=['PREV_HOME_ZONE', 'PREV_AWAY_ZONE', 'PREV_X_1', 'PREV_Y_1'])

### pull the shootout events into a separate dataframe
shootout_df = pbp_df.copy()
shootout_df = shootout_df[(shootout_df['PERIOD'] == 5) & (shootout_df['EVENT'] != 'Period.Start') & (shootout_df['EVENT'] != 'Period.End')]
shootout_df = shootout_df.drop_duplicates(subset=['TEAM', 'PLAYER_A'], keep='last')

### create separate penalties and goals dataframes in order to remove duplicates
penalties_df = pbp_df.copy()
penalties_df = penalties_df[(penalties_df['EVENT'] == 'Penalty')]
penalties_df = penalties_df.drop_duplicates(subset=['SECONDS_GONE', 'TEAM', 'PLAYER_A'], keep='last')

goals_df = pbp_df.copy()
goals_df = goals_df[(goals_df['EVENT_TYPE'] == 'Goal') & (goals_df['PERIOD'] != 5)]
goals_df = goals_df.drop_duplicates(subset=['SECONDS_GONE', 'TEAM', 'PLAYER_A'], keep='first')

### filter the main play-by-play dataframe for all events except penalties and goals; drop duplicates of remaining events
pbp_df = pbp_df[(pbp_df['PERIOD'] != 5) & (pbp_df['EVENT'] != 'Penalty') & (pbp_df['EVENT_TYPE'] != 'Goal')]

pbp_df = pbp_df.drop_duplicates(subset=['SECONDS_GONE', 'EVENT'], keep='last')

### merge the filtered main play-by-play dataframe with the goals and penalties dataframes; sort into chronological order 
pbp_final = pd.concat([penalties_df, goals_df, pbp_df])
pbp_final = pbp_final.sort_values(by=['PERIOD', 'SECONDS_GONE'])

### clean up specific instances where the league recorded different numbers of players on-ice for events that occurred at the same time
pbp_final['PREV_SECONDS_GONE'] = pbp_final['SECONDS_GONE'].shift(1)
pbp_final['NEXT_SECONDS_GONE'] = pbp_final['SECONDS_GONE'].shift(-1)
pbp_final['PREV_HOME_STRENGTH'] = pbp_final['HOME_STRENGTH'].shift(1)
pbp_final['NEXT_HOME_STRENGTH'] = pbp_final['HOME_STRENGTH'].shift(-1)
pbp_final['PREV_AWAY_STRENGTH'] = pbp_final['AWAY_STRENGTH'].shift(1)
pbp_final['NEXT_AWAY_STRENGTH'] = pbp_final['AWAY_STRENGTH'].shift(-1)
pbp_final['PREV_HOME_STATE'] = pbp_final['HOME_STATE'].shift(1)
pbp_final['NEXT_HOME_STATE'] = pbp_final['HOME_STATE'].shift(-1)
pbp_final['PREV_AWAY_STATE'] = pbp_final['AWAY_STATE'].shift(1)
pbp_final['NEXT_AWAY_STATE'] = pbp_final['AWAY_STATE'].shift(-1)
pbp_final['PREV_HOMEON_1'] = pbp_final['HOMEON_1'].shift(1)
pbp_final['NEXT_HOMEON_1'] = pbp_final['HOMEON_1'].shift(-1)
pbp_final['PREV_HOMEON_2'] = pbp_final['HOMEON_2'].shift(1)
pbp_final['NEXT_HOMEON_2'] = pbp_final['HOMEON_2'].shift(-1)
pbp_final['PREV_HOMEON_3'] = pbp_final['HOMEON_3'].shift(1)
pbp_final['NEXT_HOMEON_3'] = pbp_final['HOMEON_3'].shift(-1)
pbp_final['PREV_HOMEON_4'] = pbp_final['HOMEON_4'].shift(1)
pbp_final['NEXT_HOMEON_4'] = pbp_final['HOMEON_4'].shift(-1)
pbp_final['PREV_HOMEON_5'] = pbp_final['HOMEON_5'].shift(1)
pbp_final['NEXT_HOMEON_5'] = pbp_final['HOMEON_5'].shift(-1)
pbp_final['PREV_HOMEON_6'] = pbp_final['HOMEON_6'].shift(1)
pbp_final['NEXT_HOMEON_6'] = pbp_final['HOMEON_6'].shift(-1)
pbp_final['PREV_AWAYON_1'] = pbp_final['AWAYON_1'].shift(1)
pbp_final['NEXT_AWAYON_1'] = pbp_final['AWAYON_1'].shift(-1)
pbp_final['PREV_AWAYON_2'] = pbp_final['AWAYON_2'].shift(1)
pbp_final['NEXT_AWAYON_2'] = pbp_final['AWAYON_2'].shift(-1)
pbp_final['PREV_AWAYON_3'] = pbp_final['AWAYON_3'].shift(1)
pbp_final['NEXT_AWAYON_3'] = pbp_final['AWAYON_3'].shift(-1)
pbp_final['PREV_AWAYON_4'] = pbp_final['AWAYON_4'].shift(1)
pbp_final['NEXT_AWAYON_4'] = pbp_final['AWAYON_4'].shift(-1)
pbp_final['PREV_AWAYON_5'] = pbp_final['AWAYON_5'].shift(1)
pbp_final['NEXT_AWAYON_5'] = pbp_final['AWAYON_5'].shift(-1)
pbp_final['PREV_AWAYON_6'] = pbp_final['AWAYON_6'].shift(1)
pbp_final['NEXT_AWAYON_6'] = pbp_final['AWAYON_6'].shift(-1)

pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOME_STRENGTH != pbp_final.PREV_HOME_STRENGTH) & (pbp_final.HOME_STRENGTH != pbp_final.NEXT_HOME_STRENGTH), ['HOME_STRENGTH']] = pbp_final['PREV_HOME_STRENGTH']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAY_STRENGTH != pbp_final.PREV_AWAY_STRENGTH) & (pbp_final.AWAY_STRENGTH != pbp_final.NEXT_AWAY_STRENGTH), ['AWAY_STRENGTH']] = pbp_final['PREV_AWAY_STRENGTH']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOME_STATE != pbp_final.PREV_HOME_STATE) & (pbp_final.HOME_STATE != pbp_final.NEXT_HOME_STRENGTH), ['HOME_STATE']] = pbp_final['PREV_HOME_STATE']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAY_STATE != pbp_final.PREV_AWAY_STATE) & (pbp_final.AWAY_STATE != pbp_final.NEXT_AWAY_STRENGTH), ['AWAY_STATE']] = pbp_final['PREV_AWAY_STATE']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOMEON_1 != pbp_final.PREV_HOMEON_1) & (pbp_final.HOMEON_1 != pbp_final.NEXT_HOMEON_1), ['HOMEON_1']] = pbp_final['PREV_HOMEON_1']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOMEON_2 != pbp_final.PREV_HOMEON_2) & (pbp_final.HOMEON_2 != pbp_final.NEXT_HOMEON_2), ['HOMEON_2']] = pbp_final['PREV_HOMEON_2']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOMEON_3 != pbp_final.PREV_HOMEON_3) & (pbp_final.HOMEON_3 != pbp_final.NEXT_HOMEON_3), ['HOMEON_3']] = pbp_final['PREV_HOMEON_3']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOMEON_4 != pbp_final.PREV_HOMEON_4) & (pbp_final.HOMEON_4 != pbp_final.NEXT_HOMEON_4), ['HOMEON_4']] = pbp_final['PREV_HOMEON_4']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOMEON_5 != pbp_final.PREV_HOMEON_5) & (pbp_final.HOMEON_5 != pbp_final.NEXT_HOMEON_5), ['HOMEON_5']] = pbp_final['PREV_HOMEON_5']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.HOMEON_6 != pbp_final.PREV_HOMEON_6) & (pbp_final.HOMEON_6 != pbp_final.NEXT_HOMEON_6), ['HOMEON_6']] = pbp_final['PREV_HOMEON_6']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAYON_1 != pbp_final.PREV_AWAYON_1) & (pbp_final.AWAYON_1 != pbp_final.NEXT_AWAYON_1), ['AWAYON_1']] = pbp_final['PREV_AWAYON_1']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAYON_2 != pbp_final.PREV_AWAYON_2) & (pbp_final.AWAYON_2 != pbp_final.NEXT_AWAYON_2), ['AWAYON_2']] = pbp_final['PREV_AWAYON_2']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAYON_3 != pbp_final.PREV_AWAYON_3) & (pbp_final.AWAYON_3 != pbp_final.NEXT_AWAYON_3), ['AWAYON_3']] = pbp_final['PREV_AWAYON_3']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAYON_4 != pbp_final.PREV_AWAYON_4) & (pbp_final.AWAYON_4 != pbp_final.NEXT_AWAYON_4), ['AWAYON_4']] = pbp_final['PREV_AWAYON_4']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAYON_5 != pbp_final.PREV_AWAYON_5) & (pbp_final.AWAYON_5 != pbp_final.NEXT_AWAYON_5), ['AWAYON_5']] = pbp_final['PREV_AWAYON_5']; pbp_final
pbp_final.loc[(pbp_final.PREV_SECONDS_GONE == pbp_final.NEXT_SECONDS_GONE) & (pbp_final.AWAYON_6 != pbp_final.PREV_AWAYON_6) & (pbp_final.AWAYON_6 != pbp_final.NEXT_AWAYON_6), ['AWAYON_6']] = pbp_final['PREV_AWAYON_6']; pbp_final

### drop the now-extraneous previous and next columns
pbp_final = pbp_final.drop(columns=['PREV_SECONDS_GONE', 'NEXT_SECONDS_GONE', 'PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH', 'PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_HOMEON_1', 'NEXT_HOMEON_1', 'PREV_HOMEON_2', 'NEXT_HOMEON_2', 'PREV_HOMEON_3', 'NEXT_HOMEON_3', 'PREV_HOMEON_4', 'NEXT_HOMEON_4', 'PREV_HOMEON_5', 'NEXT_HOMEON_5', 'PREV_HOMEON_6', 'NEXT_HOMEON_6', 'PREV_AWAYON_1', 'NEXT_AWAYON_1', 'PREV_AWAYON_2', 'NEXT_AWAYON_2', 'PREV_AWAYON_3', 'NEXT_AWAYON_3', 'PREV_AWAYON_4', 'NEXT_AWAYON_4', 'PREV_AWAYON_5', 'NEXT_AWAYON_5', 'PREV_AWAYON_6', 'NEXT_AWAYON_6'])

### merge the now-combined play-by-play dataframe with shootout data
pbp_final = pd.concat([pbp_final, shootout_df])

### write the file to csv, without an index column
pbp_final.to_csv(pbp_parsed, index=False)


print('Finished parsing NHL play-by-play from the livefeed (csv) and pbp (csv) for ' + season_id + ' ' + game_id)