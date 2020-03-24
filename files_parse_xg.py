# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import pandas as pd
import numpy as np
import pickle
import parameters


def parse_ids(season_id, game_id):
    
    ### pull common variables from the parameters file
    files_root = parameters.files_root

    # establish file locations and destinations
    pbp_infile = files_root + 'pbp.csv'
    pbp_outfile = files_root + 'pbp.csv'

    ### access the game's roster file in order to create team-specific dicts
    rosters_csv = files_root + 'rosters.csv'
    
    rosters_df = pd.read_csv(rosters_csv)
    
    rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]
    rosters_dict = rosters_table.copy()
    rosters_dict = rosters_dict[['PLAYER_NAME', 'PLAYER_POS']].set_index('PLAYER_NAME').T.to_dict('list')
    
    ###
    ### ADJUSTMENTS & CALCULATIONS
    ### 

    # load the game's play-by-play file; create a dataframe
    pbp_csv = pbp_infile
    shots_df = pd.read_csv(pbp_csv)

    # initial filtering
    shots_df = shots_df[(shots_df['EVENT'] != 'Penalty') & (shots_df['EVENT'] != 'Stoppage')]

    # calculate seconds since previous event; if value is < 1, change to 1; set value for the initial faceoff to 0
    shots_df['SECONDS_LAST_EVENT'] = shots_df['SECONDS_GONE'] - shots_df['SECONDS_GONE'].shift(1)
    shots_df.loc[(shots_df.SECONDS_LAST_EVENT < 1), ['SECONDS_LAST_EVENT']] = 1; shots_df
    shots_df.loc[(shots_df.EVENT == 'Faceoff') & (shots_df.PERIOD == 1) & (shots_df.SECONDS_GONE == 0), ['SECONDS_LAST_EVENT']] = 0; shots_df

    # determine the shooter position   
    shots_df['SHOOTER_POS'] = shots_df['PLAYER_A']
    shots_df['SHOOTER_POS'].replace(rosters_dict, inplace=True)
    
    # determine the last event
    shots_df['LAST_EVENT'] = shots_df['EVENT'].shift(1)

    # determine the last event type
    shots_df['LAST_EVENT_TYPE'] = shots_df['EVENT_TYPE'].shift(1)

    # determine the team credited with the previous event
    shots_df['LAST_EVENT_TEAM'] = shots_df['TEAM'].shift(1)

    # determine, for each team, the zone of the previous team
    shots_df['LAST_EVENT_HOME_ZONE'] = shots_df['HOME_ZONE'].shift(1)
    shots_df['LAST_EVENT_AWAY_ZONE'] = shots_df['AWAY_ZONE'].shift(1)

    # place blocked shot coordinates in the unblocked shot coordinates column (in order to providing last event locations for unblocked shots that follow blocked shots)
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.EVENT_TYPE == 'Block'), ['X_1']] = shots_df['X_2']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.EVENT_TYPE == 'Block'), ['Y_1']] = shots_df['Y_2']; shots_df

    # create adjusted x and y coordinates
    shots_df['X_ADJ'] = np.nan
    shots_df['Y_ADJ'] = np.nan
    
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.X_1 < 0), ['Y_ADJ']] = shots_df['Y_1']*-1; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.X_1 > 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.X_1 == 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.X_1 < 0), ['Y_ADJ']] = shots_df['Y_1']*-1; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.X_1 > 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.X_1 == 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_1 < 0), ['Y_ADJ']] = shots_df['Y_1']*-1; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_1 > 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_1 == 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_1 < 0), ['Y_ADJ']] = shots_df['Y_1']*-1; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_1 > 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_1 == 0), ['Y_ADJ']] = shots_df['Y_1']; shots_df
    
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Defensive'),['Y_ADJ']] = shots_df['Y_1']*-1; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Defensive'),['Y_ADJ']] = shots_df['Y_1']*-1; shots_df    
    
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive'),['X_ADJ']] = abs(shots_df['X_1']); shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive'),['X_ADJ']] = abs(shots_df['X_1']); shots_df
    
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_1 < 0),['X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_1 > 0),['X_ADJ']] = abs(shots_df['X_1']); shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_1 == 0),['X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_1 < 0),['X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_1 > 0),['X_ADJ']] = abs(shots_df['X_1']); shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_1 == 0),['X_ADJ']] = 0; shots_df

    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Defensive'),['X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Defensive'),['X_ADJ']] = 0; shots_df

    # create absolute x and y coordinates
    shots_df['X_ABS'] = abs(shots_df['X_ADJ'])
    shots_df['Y_ABS'] = abs(shots_df['Y_ADJ'])

    # convert the original x and y coordinates to float 
    shots_df['X_1'] = shots_df['X_1'].astype(float)
    shots_df['Y_1'] = shots_df['Y_1'].astype(float)

    # create x and y coordinates for the previous event
    shots_df['LAST_EVENT_X'] = np.nan
    shots_df['LAST_EVENT_Y'] = np.nan

    shots_df.loc[(shots_df.EVENT == 'Shot'), ['LAST_EVENT_X']] = shots_df['X_1'].shift(1); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot'), ['LAST_EVENT_Y']] = shots_df['Y_1'].shift(1); shots_df
 
    # create adjusted x and y coordinates for the previous event
    shots_df['LAST_EVENT_X_ADJ'] = np.nan
    shots_df['LAST_EVENT_Y_ADJ'] = np.nan
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT_X < 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']*-1; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT_X > 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT_X == 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT_X < 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']*-1; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT_X > 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT_X == 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X < 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']*-1; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X > 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X == 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X < 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']*-1; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X > 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X == 0), ['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']; shots_df
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Defensive'),['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']*-1; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Defensive'),['LAST_EVENT_Y_ADJ']] = shots_df['LAST_EVENT_Y']*-1; shots_df    
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive'),['LAST_EVENT_X_ADJ']] = abs(shots_df['LAST_EVENT_X']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Offensive'),['LAST_EVENT_X_ADJ']] = abs(shots_df['LAST_EVENT_X']); shots_df
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X < 0),['LAST_EVENT_X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X > 0),['LAST_EVENT_X_ADJ']] = abs(shots_df['LAST_EVENT_X']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X == 0),['LAST_EVENT_X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X < 0),['LAST_EVENT_X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X > 0),['LAST_EVENT_X_ADJ']] = abs(shots_df['LAST_EVENT_X']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.LAST_EVENT_X == 0),['LAST_EVENT_X_ADJ']] = 0; shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Defensive'),['LAST_EVENT_X_ADJ']] = 0; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_ZONE == 'Defensive'),['LAST_EVENT_X_ADJ']] = 0; shots_df

    # create absolute x and y coordinates for the previous event
    shots_df['LAST_EVENT_X_ABS'] = abs(shots_df['LAST_EVENT_X_ADJ'])
    shots_df['LAST_EVENT_Y_ABS'] = abs(shots_df['LAST_EVENT_Y_ADJ'])

    # convert the original x and y coordinates  for the previous event to float 
    shots_df['LAST_EVENT_X'] = shots_df['LAST_EVENT_X'].astype(float)
    shots_df['LAST_EVENT_Y'] = shots_df['LAST_EVENT_Y'].astype(float)

    # calculate the angle
    shots_df['ANGLE'] = np.nan

    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.Y_ADJ != 0) & (shots_df.X_ADJ != 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - abs(shots_df['X_1']))**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.Y_ADJ != 0) & (shots_df.X_ADJ != 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - abs(shots_df['X_1']))**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df

    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.X_ADJ == 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - 88.5)**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.X_ADJ == 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - 88.5)**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df

    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.Y_ADJ != 0) & (shots_df.X_ADJ != 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - abs(shots_df['X_1']))**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.Y_ADJ != 0) & (shots_df.X_ADJ != 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - abs(shots_df['X_1']))**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df   

    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral') & (shots_df.X_ADJ == 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - 88.5)**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral') & (shots_df.X_ADJ == 89),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 - 88.5)**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df
    
    shots_df.loc[(shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Defensive') & (shots_df.Y_ADJ != 0),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 + abs(shots_df['X_1']))**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df
    shots_df.loc[(shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Defensive') & (shots_df.Y_ADJ != 0),['ANGLE']] = (np.arcsin((shots_df['Y_ADJ'] / (np.sqrt((89 + abs(shots_df['X_1']))**2 + (shots_df['Y_ADJ']**2))))) * 180) / 3.14; shots_df

    shots_df.loc[(shots_df.Y_ADJ == 0),['ANGLE']] = 0; shots_df
    
    shots_df.loc[(shots_df.X_ADJ > 89) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.ANGLE > 0),['ANGLE']] = 90 + shots_df['ANGLE']; shots_df # for home shots below the goal line with a positive raw angle
    shots_df.loc[(shots_df.X_ADJ > 89) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.ANGLE > 0),['ANGLE']] = 90 + shots_df['ANGLE']; shots_df # for away shots below the goal line with a positive raw angle

    shots_df.loc[(shots_df.X_ADJ > 89) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.ANGLE < 0),['ANGLE']] = shots_df['ANGLE'] - 90; shots_df # for home shots below the goal line with a negative raw angle
    shots_df.loc[(shots_df.X_ADJ > 89) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.ANGLE < 0),['ANGLE']] = shots_df['ANGLE'] - 90; shots_df # for away shots below the goal line with a negative raw angle
   
    shots_df['ANGLE_ABS'] = abs(shots_df['ANGLE'])

    # calculate the distance
    shots_df['DISTANCE'] = np.nan

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Offensive'),['DISTANCE']] = np.sqrt((89 - abs(shots_df['X_1']))**2 + (abs(shots_df['Y_1'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Offensive'),['DISTANCE']] = np.sqrt((89 - abs(shots_df['X_1']))**2 + (abs(shots_df['Y_1'])**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Neutral'),['DISTANCE']] = np.sqrt((89 - abs(shots_df['X_1']))**2 + (abs(shots_df['Y_1'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Neutral'),['DISTANCE']] = np.sqrt((89 - abs(shots_df['X_1']))**2 + (abs(shots_df['Y_1'])**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_ZONE == 'Defensive'),['DISTANCE']] = np.sqrt((89 + abs(shots_df['X_1']))**2 + (abs(shots_df['Y_1'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_ZONE == 'Defensive'),['DISTANCE']] = np.sqrt((89 + abs(shots_df['X_1']))**2 + (abs(shots_df['Y_1'])**2)); shots_df

    # calculate the distance from the event to the last event
    shots_df['DISTANCE_LAST_EVENT'] = np.nan

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 - abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['LAST_EVENT_X'])) - (89 - abs(shots_df['X_1'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 - abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['LAST_EVENT_X'])) - (89 - abs(shots_df['X_1'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 - abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['LAST_EVENT_X'])) - (89 - abs(shots_df['X_1'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 - abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['LAST_EVENT_X'])) - (89 - abs(shots_df['X_1'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df   
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 + abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 + abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 >= 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 + abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y >= 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) + abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X < 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 + abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X >= 0) & (shots_df.Y_1 < 0) & (shots_df.LAST_EVENT_Y < 0),['DISTANCE_LAST_EVENT']] = np.sqrt(abs(((89 + abs(shots_df['X_1'])) - (89 - abs(shots_df['LAST_EVENT_X'])))**2) + (abs((abs(shots_df['Y_1']) - abs(shots_df['LAST_EVENT_Y'])))**2)); shots_df

    # calculate the 'speed' between the event and the preceding event (see: moneypuck.com/about.htm)
    shots_df['SPEED_LAST_EVENT'] = shots_df['DISTANCE_LAST_EVENT']
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.SECONDS_LAST_EVENT > 0), ['SPEED_LAST_EVENT']] = shots_df['DISTANCE_LAST_EVENT'] / shots_df['SECONDS_LAST_EVENT']; shots_df

    # calculate, for when the event and last event were both unblocked shots for the same team, the last event's angle
    shots_df['LAST_EVENT_ANGLE'] = 0

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block'),['LAST_EVENT_ANGLE']] = (np.arcsin((shots_df['LAST_EVENT_Y_ADJ'] / (np.sqrt((89 - abs(shots_df['LAST_EVENT_X']))**2 + (shots_df['LAST_EVENT_Y_ADJ']**2))))) * 180) / 3.14; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block'),['LAST_EVENT_ANGLE']] = (np.arcsin((shots_df['LAST_EVENT_Y_ADJ'] / (np.sqrt((89 - abs(shots_df['LAST_EVENT_X']))**2 + (shots_df['LAST_EVENT_Y_ADJ']**2))))) * 180) / 3.14; shots_df

    shots_df.loc[(shots_df.LAST_EVENT_Y_ADJ == 0),['LAST_EVENT_ANGLE']] = 0; shots_df

    shots_df['LAST_EVENT_ANGLE_ABS'] = abs(shots_df['LAST_EVENT_ANGLE'])

    # calculate, for when the event and last events were both unblocked shots for the same team, the last event's distance
    shots_df['LAST_EVENT_DISTANCE'] = 0
    
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X >= 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 - abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X >= 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 - abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X < 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 + abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 >= 0) & (shots_df.LAST_EVENT_X < 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 + abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X < 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 - abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X < 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 - abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X >= 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 + abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.X_1 < 0) & (shots_df.LAST_EVENT_X >= 0),['LAST_EVENT_DISTANCE']] = np.sqrt((89 + abs(shots_df['LAST_EVENT_X']))**2 + (abs(shots_df['LAST_EVENT_Y'])**2)); shots_df

    # calculate, for when the event and last event were both unblocked shots for the same team, the change in angle
    shots_df['CHANGE_IN_ANGLE'] = 0

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE >= 0) & (shots_df.LAST_EVENT_ANGLE >= 0),['CHANGE_IN_ANGLE']] = abs(shots_df['ANGLE'] - shots_df['LAST_EVENT_ANGLE']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE >= 0) & (shots_df.LAST_EVENT_ANGLE < 0),['CHANGE_IN_ANGLE']] = shots_df['ANGLE'] + abs(shots_df['LAST_EVENT_ANGLE']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE < 0) & (shots_df.LAST_EVENT_ANGLE >= 0),['CHANGE_IN_ANGLE']] = abs(shots_df['ANGLE']) + shots_df['LAST_EVENT_ANGLE']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE < 0) & (shots_df.LAST_EVENT_ANGLE < 0),['CHANGE_IN_ANGLE']] = abs(abs(shots_df['ANGLE']) - abs(shots_df['LAST_EVENT_ANGLE'])); shots_df

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE >= 0) & (shots_df.LAST_EVENT_ANGLE >= 0),['CHANGE_IN_ANGLE']] = abs(shots_df['ANGLE'] - shots_df['LAST_EVENT_ANGLE']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE >= 0) & (shots_df.LAST_EVENT_ANGLE < 0),['CHANGE_IN_ANGLE']] = shots_df['ANGLE'] + abs(shots_df['LAST_EVENT_ANGLE']); shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE < 0) & (shots_df.LAST_EVENT_ANGLE >= 0),['CHANGE_IN_ANGLE']] = abs(shots_df['ANGLE']) + shots_df['LAST_EVENT_ANGLE']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block') & (shots_df.ANGLE < 0) & (shots_df.LAST_EVENT_ANGLE < 0),['CHANGE_IN_ANGLE']] = abs(abs(shots_df['ANGLE']) - abs(shots_df['LAST_EVENT_ANGLE'])); shots_df

    # calculate, for when the event and last event were both unblocked shots for the same team, the change of angle
    shots_df['SPEED_CHANGE_IN_ANGLE'] = 0

    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.HOME) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.HOME_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block'),['SPEED_CHANGE_IN_ANGLE']] = shots_df['CHANGE_IN_ANGLE'] / shots_df['SECONDS_LAST_EVENT']; shots_df
    shots_df.loc[(shots_df.EVENT == 'Shot') & (shots_df.TEAM == shots_df.AWAY) & (shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df.AWAY_ZONE == 'Offensive') & (shots_df.LAST_EVENT == 'Shot') & (shots_df.LAST_EVENT_TYPE != 'Block'),['SPEED_CHANGE_IN_ANGLE']] = shots_df['CHANGE_IN_ANGLE'] / shots_df['SECONDS_LAST_EVENT']; shots_df


    ###
    ### DUMMY VARIABLES
    ###
    
    # booleans for the shooter being a forward
    shots_df['IS_SHOOTER_POS_F'] = np.where(shots_df['SHOOTER_POS'].isin(['F']), 1, 0)
    
    # booleans for the shooting team being the home side
    shots_df['IS_TEAM_HOME'] = np.where((shots_df.TEAM == shots_df.HOME), 1, 0)
    
    # booleans for shots credited as a goal or on-net
    shots_df['IS_GOAL'] = np.where(shots_df['EVENT_TYPE'].isin(['Goal']), 1, 0)
    shots_df['IS_ON_NET'] = np.where(shots_df['EVENT_TYPE'].isin(['Goal', 'Save']), 1, 0)
    
    # booleans for inferred type of shot
    shots_df['IS_REBOUND'] = np.where((shots_df['LAST_EVENT'] == 'Shot') & (shots_df['SECONDS_LAST_EVENT'] <= 2) & (shots_df['TEAM'] == shots_df['LAST_EVENT_TEAM']), 1, 0)
    
    # booleans for shot description
    shots_df['IS_BACKHAND'] = np.where(shots_df['EVENT_DETAIL'].isin(['Backhand']), 1, 0)
    shots_df['IS_REDIRECT'] = np.where(shots_df['EVENT_DETAIL'].isin(['Redirect']), 1, 0)
    shots_df['IS_SLAP'] = np.where(shots_df['EVENT_DETAIL'].isin(['Slap']), 1, 0)
    shots_df['IS_SNAP'] = np.where(shots_df['EVENT_DETAIL'].isin(['Snap']), 1, 0)
    shots_df['IS_WRAPAROUND'] = np.where(shots_df['EVENT_DETAIL'].isin(['Wraparound']), 1, 0)
    shots_df['IS_WRIST'] = np.where(shots_df['EVENT_DETAIL'].isin(['Wrist']), 1, 0)
    
    # booleans for empty-net situations
    shots_df['IS_TEAM_NET_EMPTY'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '6v5') | (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '6v4') | (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '5v5') | (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '5v4') | (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '5v3') | (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '4v4') | (shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '4v3') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '6v5') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '6v4') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '5v5') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '5v4') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '5v3') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '4v4') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '4v3'), 1, 0)
    shots_df['IS_OPP_NET_EMPTY'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '6v5') | (shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '6v4') | (shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '5v5') | (shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '5v4') | (shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '5v3') | (shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '4v4') | (shots_df.TEAM == shots_df.HOME) & (shots_df.AWAY_STATE == 'EN') & (shots_df.AWAY_STRENGTH == '4v3') |(shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '6v5') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '6v4') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '5v5') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '5v4') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '5v3') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '4v4') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.HOME_STATE == 'EN') & (shots_df.HOME_STRENGTH == '4v3'), 1, 0)

    # booleans for team situation 
    shots_df['IS_TEAM_UP_3_OR_MORE'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF >= 3) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF >= 3), 1, 0)
    shots_df['IS_TEAM_UP_2'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF == 2) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF == 2), 1, 0)
    shots_df['IS_TEAM_UP_1'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF == 1) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF == 1), 1, 0)

    shots_df['IS_TEAM_TIED'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF == 0) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF == 0), 1, 0)
       
    shots_df['IS_TEAM_DOWN_1'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF == -1) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF == -1), 1, 0)
    shots_df['IS_TEAM_DOWN_2'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF == -2) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF == -2), 1, 0)
    shots_df['IS_TEAM_DOWN_3_OR_MORE'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_SCOREDIFF <= -3) | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_SCOREDIFF <= -3), 1, 0)
       
    ### booleans for team strength
    shots_df['IS_TEAM_5v5'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '5v5') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '5v5') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    shots_df['IS_TEAM_4v4'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '4v4') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '4v4') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    shots_df['IS_TEAM_3v3'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '3v3') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '3v3') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    
    shots_df['IS_TEAM_5v4'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '5v4') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '5v4') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    shots_df['IS_TEAM_5v3'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '5v3') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '5v3') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    shots_df['IS_TEAM_4v3'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '4v3') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '4v3') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    
    shots_df['IS_TEAM_4v5'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '4v5') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '4v5') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    shots_df['IS_TEAM_3v5'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '3v5') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '3v5') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    shots_df['IS_TEAM_3v4'] = np.where((shots_df.TEAM == shots_df.HOME) & (shots_df.HOME_STRENGTH == '3v4') & (shots_df.HOME_STATE != 'EN') | (shots_df.TEAM == shots_df.AWAY) & (shots_df.AWAY_STRENGTH == '3v4') & (shots_df.AWAY_STATE != 'EN'), 1, 0)
    
    # booleans for last event type
    shots_df['IS_LAST_EVENT_TEAM_SHOT'] = np.where((shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Shot'])), 1, 0)
    shots_df['IS_LAST_EVENT_TEAM_FACEOFF'] = np.where((shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Faceoff'])), 1, 0)
    shots_df['IS_LAST_EVENT_TEAM_GIVEAWAY'] = np.where((shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Giveaway'])), 1, 0)
    shots_df['IS_LAST_EVENT_TEAM_TAKEAWAY'] = np.where((shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Takeaway'])), 1, 0)
    shots_df['IS_LAST_EVENT_TEAM_HIT'] = np.where((shots_df.TEAM == shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Hit'])), 1, 0)
    
    shots_df['IS_LAST_EVENT_OPP_SHOT'] = np.where((shots_df.TEAM != shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Shot'])), 1, 0)
    shots_df['IS_LAST_EVENT_OPP_FACEOFF'] = np.where((shots_df.TEAM != shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Faceoff'])), 1, 0)
    shots_df['IS_LAST_EVENT_OPP_GIVEAWAY'] = np.where((shots_df.TEAM != shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Giveaway'])), 1, 0)    
    shots_df['IS_LAST_EVENT_OPP_TAKEAWAY'] = np.where((shots_df.TEAM != shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Takeaway'])), 1, 0)
    shots_df['IS_LAST_EVENT_OPP_HIT'] = np.where((shots_df.TEAM != shots_df.LAST_EVENT_TEAM) & (shots_df['LAST_EVENT'].isin(['Hit'])), 1, 0)
     
    # final filtering
    if int(game_id) < 30000: 
        shots_df = shots_df[(shots_df['PERIOD'] < 5) & (shots_df['EVENT'] == 'Shot') & (shots_df['EVENT_TYPE'] != 'Block') & (shots_df['EVENT_DETAIL'] != 'PS')]

    if int(game_id) > 30000:
        shots_df = shots_df[(shots_df['EVENT'] == 'Shot') & (shots_df['EVENT_TYPE'] != 'Block') & (shots_df['EVENT_DETAIL'] != 'PS')]

    # round various columns
    shots_df['ANGLE'] = round(shots_df['ANGLE'], 2)
    shots_df['ANGLE_ABS'] = round(shots_df['ANGLE_ABS'], 2)
    shots_df['DISTANCE'] = round(shots_df['DISTANCE'], 2)
    shots_df['DISTANCE_LAST_EVENT'] = round(shots_df['DISTANCE_LAST_EVENT'], 2)
    shots_df['SPEED_LAST_EVENT'] = round(shots_df['SPEED_LAST_EVENT'], 2)
    shots_df['LAST_EVENT_ANGLE'] = round(shots_df['LAST_EVENT_ANGLE'], 2)
    shots_df['LAST_EVENT_ANGLE_ABS'] = round(shots_df['LAST_EVENT_ANGLE_ABS'], 2)
    shots_df['LAST_EVENT_DISTANCE'] = round(shots_df['LAST_EVENT_DISTANCE'], 2)
    shots_df['CHANGE_IN_ANGLE'] = round(shots_df['CHANGE_IN_ANGLE'], 2)
    shots_df['SPEED_CHANGE_IN_ANGLE'] = round(shots_df['SPEED_CHANGE_IN_ANGLE'], 2)

    # drop unnecessary columns
    shots_df = shots_df.drop(columns=['TIME_LEFT', 'TIME_GONE', 'PLAYER_B', 'PLAYER_C', 'X_2', 'Y_2', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])


    print('Finished expected goals preparation for ' + season_id + ' ' + game_id)


    ###
    ### XG VALUES
    ###
    
    # trim the dataframe
    drop_columns = ['SEASON', 'GAME_ID', 'HOME', 'AWAY', 'PERIOD', 'SECONDS_LAST_EVENT', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'EVENT', 'EVENT_TYPE', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'X_1', 'Y_1', 'SHOOTER_POS', 'LAST_EVENT', 'LAST_EVENT_TYPE', 'LAST_EVENT_TEAM', 'LAST_EVENT_X', 'LAST_EVENT_Y', 'X_ADJ', 'Y_ADJ', 'ANGLE', 'LAST_EVENT_X_ADJ', 'LAST_EVENT_Y_ADJ', 'LAST_EVENT_ANGLE', 'LAST_EVENT_ANGLE_ABS', 'LAST_EVENT_DISTANCE', 'CHANGE_IN_ANGLE', 'IS_TEAM_HOME', 'IS_ON_NET']
    xg_df = shots_df.copy()
   
    xg_df = xg_df.drop(columns=drop_columns)
    
    # select the features
    continuous_variables = ['SECONDS_GONE', 'X_ABS', 'Y_ABS', 'ANGLE_ABS', 'DISTANCE', 'DISTANCE_LAST_EVENT', 'SPEED_LAST_EVENT', 'SPEED_CHANGE_IN_ANGLE']
    boolean_variables = ['IS_SHOOTER_POS_F', 'IS_REBOUND', 'IS_LAST_EVENT_TEAM_SHOT', 'IS_LAST_EVENT_OPP_SHOT', 'IS_LAST_EVENT_TEAM_FACEOFF', 'IS_LAST_EVENT_OPP_FACEOFF', 'IS_LAST_EVENT_TEAM_GIVEAWAY', 'IS_LAST_EVENT_OPP_GIVEAWAY', 'IS_LAST_EVENT_TEAM_TAKEAWAY', 'IS_LAST_EVENT_OPP_TAKEAWAY', 'IS_LAST_EVENT_OPP_HIT', 'IS_LAST_EVENT_TEAM_HIT', 'IS_TEAM_NET_EMPTY', 'IS_OPP_NET_EMPTY', 'IS_TEAM_UP_3_OR_MORE', 'IS_TEAM_UP_2', 'IS_TEAM_UP_1', 'IS_TEAM_TIED', 'IS_TEAM_DOWN_1', 'IS_TEAM_DOWN_2', 'IS_TEAM_DOWN_3_OR_MORE', 'IS_TEAM_5v5', 'IS_TEAM_4v4', 'IS_TEAM_3v3', 'IS_TEAM_5v4', 'IS_TEAM_5v3', 'IS_TEAM_4v3', 'IS_TEAM_4v5', 'IS_TEAM_3v5', 'IS_TEAM_3v4']

    independent_variables = continuous_variables + boolean_variables
    x = xg_df[independent_variables]
    
    # set the dependent variable
    y = xg_df['IS_GOAL']
    
    # load the model
    pkl_model = 'pickle_gb.pkl'
    with open(pkl_model, 'rb') as file_xg_model:
        xg_model = pickle.load(file_xg_model)
        
    # generate predictions for each shot; turn them into a dataframe and then convert goal probabilities to a list
    predictions = xg_model.predict_proba(x) 
    predictions_df = pd.DataFrame(predictions)      
    xg_column = predictions_df[1].tolist()
    
    # add the probabilities to a new column in the original shots dataframe
    shots_df['xG'] = xg_column
    
    # create a new dataframe with the original pbp info
    pbp_df = pd.read_csv(pbp_csv)    
    
    # make a truncated version of shots_df to join with the pbp data
    shots_df_copy = shots_df[['SECONDS_GONE', 'EVENT_TYPE', 'PLAYER_A', 'xG']].copy()

    pbp_df = pd.merge(pbp_df, shots_df_copy, on=['SECONDS_GONE', 'EVENT_TYPE', 'PLAYER_A'], how='left')

    
    ###
    ### WRITEOUT
    ###

    # save to file
    pbp_df.to_csv(pbp_outfile, index=False)