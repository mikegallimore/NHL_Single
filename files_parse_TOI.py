# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 22:10:14 2018

@author: @mikegallimore
"""

import json
import csv
import parameters
import pandas as pd
import numpy as np

def parse_ids(season_id, game_id):

    ### pull common variables from the parameters file
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    ### establish file locations and destinations
    livefeed_parsed = files_root + 'livefeed.csv'
    livefeed_source = files_root + 'livefeed.json'
    rosters_parsed = files_root + 'rosters.csv'
    shifts_parsed = files_root + 'shifts.csv'
    TOI_outfile = files_root + 'TOI_matrix.csv'
    
    ### open the game's livefeed (JSON) file to create a few shared variables
    with open(livefeed_source) as livefeed_json:
        livefeed_data = json.load(livefeed_json)
       
        current_period = livefeed_data["liveData"]["linescore"]["currentPeriod"]
        current_time_remaining = livefeed_data["liveData"]["linescore"]["currentPeriodTimeRemaining"]
        
        time_remaining_min = 0
        time_remaining_sec = 0
        
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
    ### TOI MATRIX FROM SHIFTS (CSV)
    ###
    
    ### trigger the files that will be read from and written to; write column titles to a header row
    with open(shifts_parsed, 'r') as game_shifts:
    
        ### determine max game length from the 5-digit game identifier; 1 = preseason, 2 = regular season, 3 = postseason       
        seconds = 3901 if game_id[0] == '1' or game_id[0] == '2' else 10801
    
        ### identify goal events to record at the second occured by accessing play-by-play records
        livefeed_df = pd.read_csv(livefeed_parsed)
    
        events_table = livefeed_df[['SECONDS_GONE','EVENT_TYPE', 'TEAM']]
        goals_table = events_table[(events_table['EVENT_TYPE'] == 'Goal')]
        goals_table = goals_table.dropna(subset=['SECONDS_GONE'])
    
        goals_dict = goals_table[['SECONDS_GONE', 'EVENT_TYPE']].set_index('SECONDS_GONE').T.to_dict('list')
        team_dict = goals_table[['SECONDS_GONE', 'TEAM']].set_index('SECONDS_GONE').T.to_dict('list')
    
        ### read in the shifts file as a dataframe; separate home from away shifts; generate lists for later use
        shifts_df = pd.read_csv(shifts_parsed)
    
        home_shifts_df = shifts_df[shifts_df.LOCATION == 'Home']
        away_shifts_df = shifts_df[shifts_df.LOCATION == 'Away']
                
        hTOI = home_shifts_df.values.tolist()
        vTOI = away_shifts_df.values.tolist()
    
        ### read in the rosters file as a dataframe; separate home from away rosters; generate goalie lists
        rosters_df = pd.read_csv(rosters_parsed)
            
        home_roster_df = rosters_df[(rosters_df.LOCATION == 'Home') & (rosters_df.PLAYER_POS == 'G')]
        home_goalies = home_roster_df['PLAYER_NAME'].tolist()
    
        away_roster_df = rosters_df[(rosters_df.LOCATION == 'Away') & (rosters_df.PLAYER_POS == 'G')]
        away_goalies = away_roster_df['PLAYER_NAME'].tolist()
        
        ### start a counter for goals scored by each team
        home_goals = int(0)
        away_goals = int(0)
        
        ### establish the number of columns to be populated with each row
        playersON_rows = [[second, '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''] for second in range(seconds)]
                               
        ### iterate through rows in the hTOI and vTOI lists and adds each name and ID to the corresponding second
        for row in hTOI:
            second = shiftStart = int(row[9])
            shiftEnd = int(row[10])
                    
            while second <= shiftEnd:
                playersON_rows[second][2] += row[6] + ':'
                playersON_rows[second][3] += str(row[5]) + ':'
                second += 1
                
        for row in vTOI:
            second = shiftStart = int(row[9])
            shiftEnd = int(row[10])
                            
            while second <= shiftEnd:
                playersON_rows[second][4] += row[6] + ':'
                playersON_rows[second][5] += str(row[5]) + ':'
                second += 1
               
        ### iterate through all seconds, assign strength states, and remove times after game end
        for i in range(len(playersON_rows)):
                    
            ### remove trailing colon from player lists
            playersON_rows[i][2] = playersON_rows[i][2][:-1]
            playersON_rows[i][3] = playersON_rows[i][3][:-1]
            playersON_rows[i][4] = playersON_rows[i][4][:-1]
            playersON_rows[i][5] = playersON_rows[i][5][:-1]
                                    
            ### get lists of home and away players
            home_players = playersON_rows[i][2].split(':')
            away_players = playersON_rows[i][4].split(':')
    
            ### copy the set of players from previous record when one of the home or away player lists are missing due to a source file error
            if(not home_players[0]):
                playersON_rows[i][2] = playersON_rows[i-1][2]
                playersON_rows[i][3] = playersON_rows[i-1][3]
            if(not away_players[0]):
                playersON_rows[i][4] = playersON_rows[i-1][4]
                playersON_rows[i][5] = playersON_rows[i-1][5]
                        
            home_players = playersON_rows[i][2].split(':')
            away_players = playersON_rows[i][4].split(':')
                        
            ### get on-ice player counts; use the counts to determine each team's strength they are playing under
            home_skaters = 0
            home_goalie = 0
                
            away_skaters = 0
            away_goalie = 0
    
            for player in home_players:
                if player != home_goalies[0] and player != home_goalies[1]:
                    home_skaters += 1                    
                if player == home_goalies[0] or player == home_goalies[1]:
                    home_goalie += 1
    
            for player in away_players:
                if player != away_goalies[0] and player != away_goalies[1]:
                    away_skaters += 1  
                if player == away_goalies[0] or player == away_goalies[1]:
                    away_goalie += 1
    
            home_strength = str(home_skaters) + 'v' + str(away_skaters)
            playersON_rows[i][6] = home_strength
            away_strength = str(away_skaters) + 'v' + str(home_skaters)
            playersON_rows[i][7] = away_strength
    
            ### use each team's number of skaters to determine the home and away state of play
            home_compare = home_strength.split('v')[0]
            away_compare = away_strength.split('v')[0]
            home_state = ()
            away_state = ()
                
            if int(home_compare) == int(away_compare):
                home_state = 'EV'
                away_state = 'EV'
            elif int(home_compare) > int(away_compare):
                home_state = 'PP'
                away_state = 'SH'
            elif int(home_compare) < int(away_compare):
                home_state = 'SH'
                away_state = 'PP'          
    
            playersON_rows[i][8] = home_state
            playersON_rows[i][9] = away_state            
    
            ### use the number of skaters and whether a goalie is on the ice to change bogus strengths and update states to  previous row values
            if home_skaters > 6:
                playersON_rows[i][2] = playersON_rows[i-1][2]
                playersON_rows[i][6] = playersON_rows[i-1][6]
                playersON_rows[i][7] = playersON_rows[i-1][7] 
                playersON_rows[i][8] = playersON_rows[i-1][8]
                playersON_rows[i][9] = playersON_rows[i-1][9] 
            if away_skaters > 6:
                playersON_rows[i][4] = playersON_rows[i-1][4]    
                playersON_rows[i][6] = playersON_rows[i-1][6]
                playersON_rows[i][7] = playersON_rows[i-1][7] 
                playersON_rows[i][8] = playersON_rows[i-1][8]
                playersON_rows[i][9] = playersON_rows[i-1][9]
    
            if home_skaters == 6 and home_goalie == 1:
                playersON_rows[i][2] = playersON_rows[i-1][2] 
                playersON_rows[i][6] = playersON_rows[i-1][6]
                playersON_rows[i][7] = playersON_rows[i-1][7] 
                playersON_rows[i][8] = playersON_rows[i-1][8]
                playersON_rows[i][9] = playersON_rows[i-1][9] 
            if away_skaters == 6 and away_goalie == 1:
                playersON_rows[i][4] = playersON_rows[i-1][4]    
                playersON_rows[i][6] = playersON_rows[i-1][6]
                playersON_rows[i][7] = playersON_rows[i-1][7] 
                playersON_rows[i][8] = playersON_rows[i-1][8]
                playersON_rows[i][9] = playersON_rows[i-1][9]
    
            if home_goalie == 0 or away_goalie == 0:
                playersON_rows[i][8] = 'EN'
                playersON_rows[i][9] = 'EN'
                    
            ### determine if a goal was scored and by what team in order to produce home and away game situation for each team
            event = str()
            team_scored = str()
                    
            try:
                event = goals_dict[i][0]
            except:
                pass
            playersON_rows[i][10] = event
    
            try:
                team_scored = team_dict[i][0]
            except:
                pass
            playersON_rows[i][11] = team_scored
    
            ### find the number of goals presently scored by the home and away team
            if event == 'Goal' and team_scored == home:
                home_goals += 1
            playersON_rows[i][12] = home_goals
                
            if event == 'Goal' and team_scored == away:
                away_goals += 1
            playersON_rows[i][13] = away_goals
    
            ### split the combined score state into distinct home and away goals scored differentials
            home_scorediff = int(home_goals) - int(away_goals)
            away_scorediff = int(away_goals) - int(home_goals)
    
            if event == 'Goal' and team_scored == home:
                home_scorediff = home_scorediff - 1
                away_scorediff = away_scorediff + 1
    
            if event == 'Goal' and team_scored == away:
                home_scorediff = home_scorediff + 1
                away_scorediff = away_scorediff - 1
    
            home_situation = ()
            away_situation = ()
    
            ### determine the home and away score situations
            if int(home_scorediff) == int(away_scorediff):
                home_situation = 'TIED'
                away_situation = 'TIED'
            elif int(home_scorediff) > int(away_scorediff):
                home_situation = 'LEADING'
                away_situation = 'TRAILING'
            elif int(home_scorediff) < int(away_scorediff):
                home_situation = 'TRAILING'
                away_situation = 'LEADING'
            playersON_rows[i][14] = home_situation
            playersON_rows[i][15] = away_situation
    
            ### remove any row that trail the end of the game
            if playersON_rows[i][0] > 3600 and event == 'Goal':
                break
            elif playersON_rows[i][0] > 3599 and home_goals != away_goals:
                break
    
        with open(TOI_outfile, 'w', newline='') as TOI_matrix:
    
            writer = csv.writer(TOI_matrix)               
            writer.writerow(['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'SECONDS_GONE', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'EVENT', 'TEAM', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6', 'BURN_1', 'BURN_2'])
            
            ### loop through the rows
            for i in range(1, len(playersON_rows)):
                game_info = [season_id, game_id, date, home, away]
                team_states = [playersON_rows[i][8], playersON_rows[i][9]]
                goals_info = [playersON_rows[i][10], playersON_rows[i][11], playersON_rows[i][12], playersON_rows[i][13], playersON_rows[i][14], playersON_rows[i][15]]
    
                homeON = playersON_rows[i][2].split(':')
    
                ### add empty strings for game states where teams have fewer than 6 players in order to prevent incorrect placement
                if len(homeON) == 5:
                    homeON.append('')
                if len(homeON) == 4:
                    homeON.append('')
                    homeON.append('')
    
                awayON = playersON_rows[i][4].split(':')
                if len(awayON) == 5:
                    awayON.append('')
                if len(awayON) == 4:
                    awayON.append('')
                    awayON.append('')
                                  
                row = game_info + [playersON_rows[i][0]] + [playersON_rows[i][6]] + [playersON_rows[i][7]] + team_states + goals_info + homeON + awayON 
                    
                ### writes each row to csv
                writer.writerow(row)
     
    ### reload the newly minted csv file for some (okay, a lot of) finessing in pandas
    TOI_df = pd.read_csv(TOI_outfile)
    
    ###
    TOI_df['HOME_STRENGTH'].replace('', np.nan, inplace=True)
    TOI_df['AWAY_STRENGTH'].replace('', np.nan, inplace=True)
    
    ### 
    TOI_df= TOI_df.dropna(subset=['HOME_STRENGTH'])
    TOI_df= TOI_df.dropna(subset=['AWAY_STRENGTH'])
    
    ### create new columns for each team's previous and following strength and state 
    TOI_df['PREV_HOME_STRENGTH'] = TOI_df['HOME_STRENGTH'].shift(1)
    TOI_df['NEXT_HOME_STRENGTH'] = TOI_df['HOME_STRENGTH'].shift(-1)
    TOI_df['PREV_AWAY_STRENGTH'] = TOI_df['AWAY_STRENGTH'].shift(1)
    TOI_df['NEXT_AWAY_STRENGTH'] = TOI_df['AWAY_STRENGTH'].shift(-1)
    TOI_df['PREV_HOME_STATE'] = TOI_df['HOME_STATE'].shift(1)
    TOI_df['NEXT_HOME_STATE'] = TOI_df['HOME_STATE'].shift(-1)
    TOI_df['PREV_AWAY_STATE'] = TOI_df['AWAY_STATE'].shift(1)
    TOI_df['NEXT_AWAY_STATE'] = TOI_df['AWAY_STATE'].shift(-1)
    
    ### create a new column for the previous event
    TOI_df['PREV_EVENT'] = TOI_df['EVENT'].shift(1)
    
    ### create new columns for the each team's previous and following on-ice players
    TOI_df['PREV_HOMEON_1'] = TOI_df['HOMEON_1'].shift(1)
    TOI_df['NEXT_HOMEON_1'] = TOI_df['HOMEON_1'].shift(-1)
    TOI_df['PREV_HOMEON_2'] = TOI_df['HOMEON_2'].shift(1)
    TOI_df['NEXT_HOMEON_2'] = TOI_df['HOMEON_2'].shift(-1)
    TOI_df['PREV_HOMEON_3'] = TOI_df['HOMEON_3'].shift(1)
    TOI_df['NEXT_HOMEON_3'] = TOI_df['HOMEON_3'].shift(-1)
    TOI_df['PREV_HOMEON_4'] = TOI_df['HOMEON_4'].shift(1)
    TOI_df['NEXT_HOMEON_4'] = TOI_df['HOMEON_4'].shift(-1)
    TOI_df['PREV_HOMEON_5'] = TOI_df['HOMEON_5'].shift(1)
    TOI_df['NEXT_HOMEON_5'] = TOI_df['HOMEON_5'].shift(-1)
    TOI_df['PREV_HOMEON_6'] = TOI_df['HOMEON_6'].shift(1)
    TOI_df['NEXT_HOMEON_6'] = TOI_df['HOMEON_6'].shift(-1)
    
    TOI_df['PREV_AWAYON_1'] = TOI_df['AWAYON_1'].shift(1)
    TOI_df['NEXT_AWAYON_1'] = TOI_df['AWAYON_1'].shift(-1)
    TOI_df['PREV_AWAYON_2'] = TOI_df['AWAYON_2'].shift(1)
    TOI_df['NEXT_AWAYON_2'] = TOI_df['AWAYON_2'].shift(-1)
    TOI_df['PREV_AWAYON_3'] = TOI_df['AWAYON_3'].shift(1)
    TOI_df['NEXT_AWAYON_3'] = TOI_df['AWAYON_3'].shift(-1)
    TOI_df['PREV_AWAYON_4'] = TOI_df['AWAYON_4'].shift(1)
    TOI_df['NEXT_AWAYON_4'] = TOI_df['AWAYON_4'].shift(-1)
    TOI_df['PREV_AWAYON_5'] = TOI_df['AWAYON_5'].shift(1)
    TOI_df['NEXT_AWAYON_5'] = TOI_df['AWAYON_5'].shift(-1)
    TOI_df['PREV_AWAYON_6'] = TOI_df['AWAYON_6'].shift(1)
    TOI_df['NEXT_AWAYON_6'] = TOI_df['AWAYON_6'].shift(-1)
    
    ### modify home strengths and states as needed for erroneous rows that occur in the run of a specific strength or state
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '5v5') & (TOI_df.PREV_HOME_STRENGTH != '5v5') & (TOI_df.NEXT_HOME_STRENGTH != '5v5'),['HOME_STRENGTH']] = TOI_df['PREV_HOME_STRENGTH']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '5v5') & (TOI_df.PREV_AWAY_STRENGTH != '5v5') & (TOI_df.NEXT_AWAY_STRENGTH != '5v5'),['AWAY_STRENGTH']] = TOI_df['PREV_AWAY_STRENGTH']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH != '4v4') & (TOI_df.PREV_HOME_STRENGTH == '4v4') & (TOI_df.NEXT_HOME_STRENGTH == '4v4'),['HOME_STRENGTH']] = TOI_df['PREV_HOME_STRENGTH']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH != '4v4') & (TOI_df.PREV_AWAY_STRENGTH == '4v4') & (TOI_df.NEXT_AWAY_STRENGTH == '4v4'),['AWAY_STRENGTH']] = TOI_df['PREV_AWAY_STRENGTH']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH != '3v3') & (TOI_df.PREV_HOME_STRENGTH == '3v3') & (TOI_df.NEXT_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = TOI_df['PREV_HOME_STRENGTH']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH != '3v3') & (TOI_df.PREV_AWAY_STRENGTH == '3v3') & (TOI_df.NEXT_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = TOI_df['PREV_AWAY_STRENGTH']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE == 'EV') & (TOI_df.PREV_HOME_STATE != 'EV') & (TOI_df.NEXT_HOME_STATE != 'EV'),['HOME_STATE']] = TOI_df['PREV_HOME_STATE']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EV') & (TOI_df.PREV_AWAY_STATE != 'EV') & (TOI_df.NEXT_AWAY_STATE != 'EV'),['AWAY_STATE']] = TOI_df['PREV_AWAY_STATE']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE != 'EV') & (TOI_df.PREV_HOME_STATE == 'EV') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = TOI_df['PREV_HOME_STATE']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE != 'EV') & (TOI_df.PREV_AWAY_STATE == 'EV') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = TOI_df['PREV_AWAY_STATE']; TOI_df
    
    try:
        ### correct erroneous rows that show 5 skaters and a goalie for the home or away team when either they should be shorthanded or during 4v4 play
        TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.PREV_HOME_STATE == 'SH') & (TOI_df.NEXT_HOME_STATE == 'SH'),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
        TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.PREV_HOME_STATE == 'SH') & (TOI_df.NEXT_HOME_STATE == 'SH'),['HOMEON_6']] = ''; TOI_df
        TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.PREV_AWAY_STATE == 'SH') & (TOI_df.NEXT_AWAY_STATE == 'SH'),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
        TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.PREV_AWAY_STATE == 'SH') & (TOI_df.NEXT_AWAY_STATE == 'SH'),['AWAYON_6']] = ''; TOI_df
    
        TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.PREV_HOME_STRENGTH == '4v4') & (TOI_df.NEXT_HOME_STRENGTH == '4v4'),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
        TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.PREV_HOME_STRENGTH == '4v4') & (TOI_df.NEXT_HOME_STRENGTH == '4v4'),['HOMEON_6']] = ''; TOI_df
        TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.PREV_AWAY_STRENGTH == '4v4') & (TOI_df.NEXT_AWAY_STRENGTH == '4v4'),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
        TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.PREV_AWAY_STRENGTH == '4v4') & (TOI_df.NEXT_AWAY_STRENGTH == '4v4'),['AWAYON_6']] = ''; TOI_df
        
        ### modify home and away strengths as needed for erronenous overtime rows that occur in the run of a specific strength or state
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.PREV_HOME_STATE == 'EV') & (TOI_df.NEXT_HOME_STATE == 'SH'),['HOME_STATE']] = TOI_df['PREV_HOME_STATE']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.PREV_AWAY_STATE == 'EV') & (TOI_df.NEXT_AWAY_STATE == 'SH'),['AWAY_STATE']] = TOI_df['PREV_AWAY_STATE']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.PREV_HOME_STATE == 'EV') & (TOI_df.NEXT_HOME_STATE == 'PP'),['HOME_STATE']] = TOI_df['PREV_HOME_STATE']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.PREV_AWAY_STATE == 'EV') & (TOI_df.NEXT_AWAY_STATE == 'PP'),['AWAY_STATE']] = TOI_df['PREV_AWAY_STATE']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.PREV_HOME_STATE != 'EV') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = TOI_df['NEXT_HOME_STATE']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.PREV_AWAY_STATE != 'EV') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = TOI_df['NEXT_AWAY_STATE']; TOI_df
        
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.PREV_HOME_STATE == 'EV') & (TOI_df.NEXT_HOME_STATE == 'SH'),['HOME_STRENGTH']] = TOI_df['PREV_HOME_STRENGTH']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.PREV_AWAY_STATE == 'EV') & (TOI_df.NEXT_AWAY_STATE == 'SH'),['AWAY_STRENGTH']] = TOI_df['PREV_AWAY_STRENGTH']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.PREV_HOME_STATE == 'EV') & (TOI_df.NEXT_HOME_STATE == 'PP'),['HOME_STRENGTH']] = TOI_df['PREV_HOME_STRENGTH']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.PREV_AWAY_STATE == 'EV') & (TOI_df.NEXT_AWAY_STATE == 'PP'),['AWAY_STRENGTH']] = TOI_df['PREV_AWAY_STRENGTH']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.PREV_HOME_STATE != 'EV') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STRENGTH']] = TOI_df['NEXT_HOME_STRENGTH']; TOI_df
        TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.PREV_AWAY_STATE != 'EV') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STRENGTH']] = TOI_df['NEXT_AWAY_STRENGTH']; TOI_df
    except:
        pass
    
    ### change NaN values to empty strings
    TOI_df['HOMEON_5'].replace(np.nan, '', inplace=True)
    TOI_df['HOMEON_6'].replace(np.nan, '', inplace=True)
    TOI_df['AWAYON_5'].replace(np.nan, '', inplace=True)
    TOI_df['AWAYON_6'].replace(np.nan, '', inplace=True)
    
    ### correct erroneous rows that show 4 skaters and a goalie for the home or away team during 3v3 play
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_6']] = ''; TOI_df
    
    ### correct erroneous rows that show 5 skaters and a goalie for the home or away team during 3v3 play
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_6']] = ''; TOI_df
    
    ### correct erroneous rows that show 4 skaters and a goalie for the home or away team during 3v4 play
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_6 == '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_6 == '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_6']] = ''; TOI_df
    
    ### correct erroneous rows that show at least 4 skaters and a goalie for the home or away team during 3v5 play
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_6']] = ''; TOI_df
    
    ### correct erroneous rows that show 5 skaters and a goalie for the home or away team during 3v4 play
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_6']] = ''; TOI_df
    
    ### correct erroneous rows that show 5 skaters and a goalie for the home or away team during 4v3 play
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '4v3'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '4v3'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '4v3'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '4v3'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 != '') & (TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '4v3'),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_6 != '') & (TOI_df.HOME_STRENGTH == '4v3'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '4v3'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '4v3'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '4v3'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '4v3'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 != '') & (TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '4v3'),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_6 != '') & (TOI_df.AWAY_STRENGTH == '4v3'),['AWAYON_6']] = ''; TOI_df
    
    try:
        ### ensure that where goals occured, the previous second's on-ice players will be returned
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
        TOI_df.loc[(TOI_df.EVENT == 'Goal'),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df
    
        
        ### ensure that for the second after a goal, the following second's on-ice players will be returned
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['HOMEON_1']] = TOI_df['NEXT_HOMEON_1']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['HOMEON_2']] = TOI_df['NEXT_HOMEON_2']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['HOMEON_3']] = TOI_df['NEXT_HOMEON_3']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['HOMEON_4']] = TOI_df['NEXT_HOMEON_4']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['HOMEON_6']] = TOI_df['NEXT_HOMEON_6']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['AWAYON_1']] = TOI_df['NEXT_AWAYON_1']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['AWAYON_2']] = TOI_df['NEXT_AWAYON_2']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['AWAYON_3']] = TOI_df['NEXT_AWAYON_3']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['AWAYON_4']] = TOI_df['NEXT_AWAYON_4']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
        TOI_df.loc[(TOI_df.PREV_EVENT == 'Goal'),['AWAYON_6']] = TOI_df['NEXT_AWAYON_6']; TOI_df
    except:
        pass
    
    ### ensure that the first second of overtime returns the following second's on-ice players
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['HOMEON_1']] = TOI_df['NEXT_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['HOMEON_2']] = TOI_df['NEXT_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['HOMEON_3']] = TOI_df['NEXT_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['HOMEON_4']] = TOI_df['NEXT_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['HOMEON_6']] = TOI_df['NEXT_HOMEON_6']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['AWAYON_1']] = TOI_df['NEXT_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['AWAYON_2']] = TOI_df['NEXT_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['AWAYON_3']] = TOI_df['NEXT_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['AWAYON_4']] = TOI_df['NEXT_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 3601),['AWAYON_6']] = TOI_df['NEXT_AWAYON_6']; TOI_df
    
    ### correct any row that potentially has the same home player listed as on-ice twice
    TOI_df.loc[(TOI_df.HOMEON_1 == TOI_df.HOMEON_2) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_6),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_1 == TOI_df.HOMEON_2) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_6),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_1 == TOI_df.HOMEON_2) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_6),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_1 == TOI_df.HOMEON_2) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_6),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_1 == TOI_df.HOMEON_2) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_6),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_1 == TOI_df.HOMEON_2) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_1 == TOI_df.HOMEON_6),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.HOMEON_2 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_6),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_2 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_6),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_2 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_6),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_2 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_6),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_2 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_6),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_2 == TOI_df.HOMEON_3) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_2 == TOI_df.HOMEON_6),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.HOMEON_3 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_6),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_3 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_6),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_3 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_6),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_3 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_6),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_3 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_6),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_3 == TOI_df.HOMEON_4) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_3 == TOI_df.HOMEON_6),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.HOMEON_4 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_4 == TOI_df.HOMEON_6),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_4 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_4 == TOI_df.HOMEON_6),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_4 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_4 == TOI_df.HOMEON_6),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_4 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_4 == TOI_df.HOMEON_6),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_4 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_4 == TOI_df.HOMEON_6),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_4 == TOI_df.HOMEON_5) | (TOI_df.HOMEON_4 == TOI_df.HOMEON_6),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.HOMEON_5 == TOI_df.HOMEON_6),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 == TOI_df.HOMEON_6),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 == TOI_df.HOMEON_6),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 == TOI_df.HOMEON_6),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 == TOI_df.HOMEON_6),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOMEON_5 == TOI_df.HOMEON_6),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df    
    
    ### correct any row that potentially has the same away player listed as on-ice twice
    TOI_df.loc[(TOI_df.AWAYON_1 == TOI_df.AWAYON_2) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_6),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_1 == TOI_df.AWAYON_2) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_6),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_1 == TOI_df.AWAYON_2) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_6),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_1 == TOI_df.AWAYON_2) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_6),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_1 == TOI_df.AWAYON_2) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_6),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_1 == TOI_df.AWAYON_2) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_1 == TOI_df.AWAYON_6),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.AWAYON_2 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_6),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_2 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_6),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_2 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_6),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_2 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_6),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_2 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_6),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_2 == TOI_df.AWAYON_3) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_2 == TOI_df.AWAYON_6),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.AWAYON_3 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_6),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_3 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_6),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_3 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_6),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_3 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_6),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_3 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_6),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_3 == TOI_df.AWAYON_4) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_3 == TOI_df.AWAYON_6),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.AWAYON_4 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_4 == TOI_df.AWAYON_6),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_4 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_4 == TOI_df.AWAYON_6),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_4 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_4 == TOI_df.AWAYON_6),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_4 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_4 == TOI_df.AWAYON_6),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_4 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_4 == TOI_df.AWAYON_6),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_4 == TOI_df.AWAYON_5) | (TOI_df.AWAYON_4 == TOI_df.AWAYON_6),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df    
    
    TOI_df.loc[(TOI_df.AWAYON_5 == TOI_df.AWAYON_6),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 == TOI_df.AWAYON_6),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 == TOI_df.AWAYON_6),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 == TOI_df.AWAYON_6),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 == TOI_df.AWAYON_6),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAYON_5 == TOI_df.AWAYON_6),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df
    
    ### further clean-up of any extra players listed for 3v3, 3v4 or 3v5 play
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v3'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v3'),['AWAYON_6']] = ''; TOI_df
    
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4'),['AWAYON_6']] = ''; TOI_df
    
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v5'),['HOMEON_6']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v5'),['AWAYON_6']] = ''; TOI_df
    
    ### further clean up of erroneous shorthanded siuations
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v5') & (TOI_df.PREV_HOME_STRENGTH == '3v4') & (TOI_df.NEXT_HOME_STRENGTH == '3v4'),['HOME_STRENGTH']] = '3v4'; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v5') & (TOI_df.PREV_AWAY_STRENGTH == '3v4') & (TOI_df.NEXT_AWAY_STRENGTH == '3v4'),['AWAY_STRENGTH']] = '3v4'; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '5v3') & (TOI_df.PREV_HOME_STRENGTH == '4v3') & (TOI_df.NEXT_HOME_STRENGTH == '4v3'),['HOME_STRENGTH']] = '4v3'; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '5v3') & (TOI_df.PREV_AWAY_STRENGTH == '4v3') & (TOI_df.NEXT_AWAY_STRENGTH == '4v3'),['AWAY_STRENGTH']] = '4v3'; TOI_df
    
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.HOMEON_5 != ''),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.HOMEON_5 != ''),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.HOMEON_5 != ''),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.HOMEON_5 != ''),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.HOMEON_5 != ''),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.HOMEON_5 != ''),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.AWAYON_5 != ''),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.AWAYON_5 != ''),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.AWAYON_5 != ''),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.AWAYON_5 != ''),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.AWAYON_5 != ''),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.AWAYON_5 != ''),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df
    
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.HOMEON_6 != ''),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.HOMEON_6 != ''),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.HOMEON_6 != ''),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.HOMEON_6 != ''),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.HOMEON_6 != ''),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.HOMEON_6 != ''),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.AWAYON_6 != ''),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.AWAYON_6 != ''),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.AWAYON_6 != ''),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.AWAYON_6 != ''),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.AWAYON_6 != ''),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.AWAYON_6 != ''),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df
    
    TOI_df.loc[(TOI_df.HOME_STATE != 'EV') & (TOI_df.PREV_HOME_STATE != 'EN') & (TOI_df.NEXT_HOME_STATE == 'EN'),['HOME_STATE']] = 'EN'; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE != 'EV') & (TOI_df.PREV_AWAY_STATE != 'EN') & (TOI_df.NEXT_AWAY_STATE == 'EN'),['AWAY_STATE']] = 'EN'; TOI_df
    
    TOI_df.loc[(TOI_df.HOME_STATE == 'EN') & (TOI_df.PREV_HOME_STATE != 'EN'),['HOMEON_1']] = TOI_df['NEXT_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE == 'EN') & (TOI_df.PREV_HOME_STATE != 'EN'),['HOMEON_2']] = TOI_df['NEXT_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE == 'EN') & (TOI_df.PREV_HOME_STATE != 'EN'),['HOMEON_3']] = TOI_df['NEXT_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE == 'EN') & (TOI_df.PREV_HOME_STATE != 'EN'),['HOMEON_4']] = TOI_df['NEXT_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE == 'EN') & (TOI_df.PREV_HOME_STATE != 'EN'),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.HOME_STATE == 'EN') & (TOI_df.PREV_HOME_STATE != 'EN'),['HOMEON_6']] = TOI_df['NEXT_HOMEON_6']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EN') & (TOI_df.PREV_AWAY_STATE != 'EN'),['AWAYON_1']] = TOI_df['NEXT_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EN') & (TOI_df.PREV_AWAY_STATE != 'EN'),['AWAYON_2']] = TOI_df['NEXT_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EN') & (TOI_df.PREV_AWAY_STATE != 'EN'),['AWAYON_3']] = TOI_df['NEXT_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EN') & (TOI_df.PREV_AWAY_STATE != 'EN'),['AWAYON_4']] = TOI_df['NEXT_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EN') & (TOI_df.PREV_AWAY_STATE != 'EN'),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.AWAY_STATE == 'EN') & (TOI_df.PREV_AWAY_STATE != 'EN'),['AWAYON_6']] = TOI_df['NEXT_AWAYON_6']; TOI_df
      
    ### further clean up of erroneous 5v4 or 4v5 situations in overtime
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.HOME_STRENGTH == '4v5') & (TOI_df.PREV_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.AWAY_STRENGTH == '4v5') & (TOI_df.PREV_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.HOME_STRENGTH == '5v4') & (TOI_df.PREV_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.AWAY_STRENGTH == '5v4') & (TOI_df.PREV_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.HOME_STRENGTH == '4v5') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.AWAY_STRENGTH == '4v5') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.HOME_STRENGTH == '5v4') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.AWAY_STRENGTH == '5v4') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v5') & (TOI_df.PREV_HOME_STRENGTH == '4v4'),['HOME_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v5') & (TOI_df.PREV_AWAY_STRENGTH == '4v4'),['AWAY_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '5v4') & (TOI_df.PREV_HOME_STRENGTH == '4v4'),['HOME_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '5v4') & (TOI_df.PREV_AWAY_STRENGTH == '4v4'),['AWAY_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v5') & (TOI_df.NEXT_HOME_STRENGTH == '4v4'),['HOME_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v5') & (TOI_df.NEXT_AWAY_STRENGTH == '4v4'),['AWAY_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '5v4') & (TOI_df.NEXT_HOME_STRENGTH == '4v4'),['HOME_STRENGTH']] = '4v4'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '5v4') & (TOI_df.NEXT_AWAY_STRENGTH == '4v4'),['AWAY_STRENGTH']] = '4v4'; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v4') & (TOI_df.HOMEON_6 != ''),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v4') & (TOI_df.HOMEON_6 != ''),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v4') & (TOI_df.HOMEON_6 != ''),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v4') & (TOI_df.HOMEON_6 != ''),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v4') & (TOI_df.HOMEON_6 != ''),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v4') & (TOI_df.HOMEON_6 != ''),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df   
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v4') & (TOI_df.AWAYON_6 != ''),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v4') & (TOI_df.AWAYON_6 != ''),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v4') & (TOI_df.AWAYON_6 != ''),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v4') & (TOI_df.AWAYON_6 != ''),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v4') & (TOI_df.AWAYON_6 != ''),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v4') & (TOI_df.AWAYON_6 != ''),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df   
    
    ### further clean up of erroneous 4v3 or 3v4 situations in overtime
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.PREV_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.PREV_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.PREV_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.PREV_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.PREV_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.PREV_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.PREV_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.PREV_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v4') & (TOI_df.NEXT_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v4') & (TOI_df.NEXT_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '4v3') & (TOI_df.NEXT_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '4v3') & (TOI_df.NEXT_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_6']] = ''; TOI_df   
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_5']] = ''; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_6']] = ''; TOI_df   
    
    ### further clean up of erroneous 5v3 or 3v5 situations in overtime
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.HOME_STRENGTH == '3v5') & (TOI_df.PREV_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.AWAY_STRENGTH == '3v5') & (TOI_df.PREV_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.HOME_STRENGTH == '5v3') & (TOI_df.PREV_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.AWAY_STRENGTH == '5v3') & (TOI_df.PREV_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'SH') & (TOI_df.HOME_STRENGTH == '3v5') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'SH') & (TOI_df.AWAY_STRENGTH == '3v5') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'PP') & (TOI_df.HOME_STRENGTH == '5v3') & (TOI_df.NEXT_HOME_STATE == 'EV'),['HOME_STATE']] = 'EV'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'PP') & (TOI_df.AWAY_STRENGTH == '5v3') & (TOI_df.NEXT_AWAY_STATE == 'EV'),['AWAY_STATE']] = 'EV'; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v5') & (TOI_df.PREV_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v5') & (TOI_df.PREV_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '5v3') & (TOI_df.PREV_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '5v3') & (TOI_df.PREV_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v5') & (TOI_df.NEXT_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v5') & (TOI_df.NEXT_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '5v3') & (TOI_df.NEXT_HOME_STRENGTH == '3v3'),['HOME_STRENGTH']] = '3v3'; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '5v3') & (TOI_df.NEXT_AWAY_STRENGTH == '3v3'),['AWAY_STRENGTH']] = '3v3'; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_1']] = TOI_df['PREV_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_2']] = TOI_df['PREV_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_3']] = TOI_df['PREV_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_4']] = TOI_df['PREV_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_5']] = TOI_df['PREV_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.HOME_STATE == 'EV') & (TOI_df.HOME_STRENGTH == '3v3') & (TOI_df.HOMEON_5 != ''),['HOMEON_6']] = TOI_df['PREV_HOMEON_6']; TOI_df   
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_1']] = TOI_df['PREV_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_2']] = TOI_df['PREV_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_3']] = TOI_df['PREV_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_4']] = TOI_df['PREV_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_5']] = TOI_df['PREV_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE > 3600) & (TOI_df.AWAY_STATE == 'EV') & (TOI_df.AWAY_STRENGTH == '3v3') & (TOI_df.AWAYON_5 != ''),['AWAYON_6']] = TOI_df['PREV_AWAYON_6']; TOI_df
    
    ### add a row for th initial faceoff at 0 seconds gone
    TOI_df.loc[-1] = [season_id, game_id, date, home, away, 0, '5v5', '5v5', 'EV', 'EV', '', '', 0, 0, 'TIED', 'TIED', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    TOI_df.index = TOI_df.index + 1
    TOI_df = TOI_df.sort_index()
    
    ### remove the extraneous columns
    TOI_df = TOI_df.drop(columns=['PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH', 'PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_EVENT', 'PREV_HOMEON_1', 'NEXT_HOMEON_1', 'PREV_HOMEON_2', 'NEXT_HOMEON_2', 'PREV_HOMEON_3', 'NEXT_HOMEON_3', 'PREV_HOMEON_4', 'NEXT_HOMEON_4', 'PREV_HOMEON_5', 'NEXT_HOMEON_5', 'PREV_HOMEON_6', 'NEXT_HOMEON_6', 'PREV_AWAYON_1', 'NEXT_AWAYON_1', 'PREV_AWAYON_2', 'NEXT_AWAYON_2', 'PREV_AWAYON_3', 'NEXT_AWAYON_3', 'PREV_AWAYON_4', 'NEXT_AWAYON_4', 'PREV_AWAYON_5', 'NEXT_AWAYON_5', 'PREV_AWAYON_6', 'NEXT_AWAYON_6', 'BURN_1', 'BURN_2'])
    
    ### regenerate new columns for each team's on-ice players for the second following
    TOI_df['NEXT_HOMEON_1'] = TOI_df['HOMEON_1'].shift(-1)
    TOI_df['NEXT_HOMEON_2'] = TOI_df['HOMEON_2'].shift(-1)
    TOI_df['NEXT_HOMEON_3'] = TOI_df['HOMEON_3'].shift(-1)
    TOI_df['NEXT_HOMEON_4'] = TOI_df['HOMEON_4'].shift(-1)
    TOI_df['NEXT_HOMEON_5'] = TOI_df['HOMEON_5'].shift(-1)
    TOI_df['NEXT_HOMEON_6'] = TOI_df['HOMEON_6'].shift(-1)
    
    TOI_df['NEXT_AWAYON_1'] = TOI_df['AWAYON_1'].shift(-1)
    TOI_df['NEXT_AWAYON_2'] = TOI_df['AWAYON_2'].shift(-1)
    TOI_df['NEXT_AWAYON_3'] = TOI_df['AWAYON_3'].shift(-1)
    TOI_df['NEXT_AWAYON_4'] = TOI_df['AWAYON_4'].shift(-1)
    TOI_df['NEXT_AWAYON_5'] = TOI_df['AWAYON_5'].shift(-1)
    TOI_df['NEXT_AWAYON_6'] = TOI_df['AWAYON_6'].shift(-1)
    
    ### use the home and away players on-ice from 1 seconds gone to populate the on-ice home and away players for 0 seconds gone
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['HOMEON_1']] = TOI_df['NEXT_HOMEON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['HOMEON_2']] = TOI_df['NEXT_HOMEON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['HOMEON_3']] = TOI_df['NEXT_HOMEON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['HOMEON_4']] = TOI_df['NEXT_HOMEON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['HOMEON_5']] = TOI_df['NEXT_HOMEON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['HOMEON_6']] = TOI_df['NEXT_HOMEON_6']; TOI_df
    
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['AWAYON_1']] = TOI_df['NEXT_AWAYON_1']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['AWAYON_2']] = TOI_df['NEXT_AWAYON_2']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['AWAYON_3']] = TOI_df['NEXT_AWAYON_3']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['AWAYON_4']] = TOI_df['NEXT_AWAYON_4']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['AWAYON_5']] = TOI_df['NEXT_AWAYON_5']; TOI_df
    TOI_df.loc[(TOI_df.SECONDS_GONE == 0),['AWAYON_6']] = TOI_df['NEXT_AWAYON_6']; TOI_df
    
    ### remove the extraneous columns
    TOI_df = TOI_df.drop(columns=['NEXT_HOMEON_1', 'NEXT_HOMEON_2', 'NEXT_HOMEON_3', 'NEXT_HOMEON_4', 'NEXT_HOMEON_5', 'NEXT_HOMEON_6', 'NEXT_AWAYON_1', 'NEXT_AWAYON_2', 'NEXT_AWAYON_3', 'NEXT_AWAYON_4', 'NEXT_AWAYON_5', 'NEXT_AWAYON_6'])
    
    if current_time_remaining != 'Final':
        TOI_df = TOI_df[(TOI_df['SECONDS_GONE'] <= current_seconds_gone)]
    
    ### write the file to csv, without an index column
    TOI_df.to_csv(TOI_outfile, index = False)
    
    
    print('Finished parsing NHL TOI matrix from the shifts .csv for ' + season_id + ' ' + game_id)