# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import pandas as pd
import numpy as np
import os
import parameters

def parse_ids(season_id, game_id, load_pbp):

    ### pull common variables from the parameters file
    files_root = parameters.files_root

    ### establish file locations and destinations
    livefeed_parsed = files_root + 'livefeed.csv'
    ESPN_parsed = files_root + 'pbp_ESPN.csv'
    pbp_parsed = files_root + 'pbp.csv'
    TOI_parsed = files_root + 'TOI_matrix.csv'

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    ###
    ### MERGE PLAY-BY-PLAY FILES
    ###
 
    if int(season_id) >= 20102011:
        
        ### load the main and livefeed play-by-play files into pandas
        pbp_df = pd.read_csv(pbp_parsed, error_bad_lines=False)
        livefeed_df = pd.read_csv(livefeed_parsed)
        
        ### drop extraneous columns from the livefeed play-by-play dataframe; save the adjustments to file
        livefeed_df = livefeed_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'EVENT_TYPE', 'EVENT_DETAIL', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])
        livefeed_df.to_csv(livefeed_parsed, index=False)
        
        ### join the contents of both play-by-play files
        pbp_df = pd.merge(pbp_df, livefeed_df, on=['SECONDS_GONE', 'EVENT'], how='left')
        
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
        
        ### replace names for special name cases
        try:
            pbp_final.loc[(pbp_final.PLAYER_A == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'CAR'),['PLAYER_A']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_B == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'CAR'),['PLAYER_B']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_B == 'SEBASTIAN.AHO') & (pbp_final.TEAM != 'CAR') & (pbp_final.EVENT_TYPE == 'Block'),['PLAYER_B']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_B == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'CAR'),['PLAYER_B']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_C == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'CAR'),['PLAYER_C']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_1 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'CAR'),['HOMEON_1']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_2 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'CAR'),['HOMEON_2']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_3 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'CAR'),['HOMEON_3']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_4 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'CAR'),['HOMEON_4']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_5 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'CAR'),['HOMEON_5']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_6 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'CAR'),['HOMEON_6']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_1 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'CAR'),['AWAYON_1']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_2 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'CAR'),['AWAYON_2']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_3 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'CAR'),['AWAYON_3']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_4 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'CAR'),['AWAYON_4']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_5 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'CAR'),['AWAYON_5']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_6 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'CAR'),['AWAYON_6']] = 'SEBASTIAN.A.AHO'; pbp_final
        except:
            pass
        
        try:
            pbp_final.loc[(pbp_final.PLAYER_A == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'NYI'),['PLAYER_A']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_B == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'NYI'),['PLAYER_B']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_B == 'SEBASTIAN.AHO') & (pbp_final.TEAM != 'NYI') & (pbp_final.EVENT_TYPE == 'Block'),['PLAYER_B']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_B == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'NYI'),['PLAYER_B']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.PLAYER_C == 'SEBASTIAN.AHO') & (pbp_final.TEAM == 'NYI'),['PLAYER_C']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_1 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'NYI'),['HOMEON_1']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_2 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'NYI'),['HOMEON_2']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_3 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'NYI'),['HOMEON_3']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_4 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'NYI'),['HOMEON_4']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_5 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'NYI'),['HOMEON_5']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_6 == 'SEBASTIAN.AHO') & (pbp_final.HOME == 'NYI'),['HOMEON_6']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_1 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'NYI'),['AWAYON_1']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_2 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'NYI'),['AWAYON_2']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_3 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'NYI'),['AWAYON_3']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_4 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'NYI'),['AWAYON_4']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_5 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'NYI'),['AWAYON_5']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_6 == 'SEBASTIAN.AHO') & (pbp_final.AWAY == 'NYI'),['AWAYON_6']] = 'SEBASTIAN.J.AHO'; pbp_final
        except:
            pass

        ### read in the rosters file as a dataframe; generate a home roster list
        rosters_df = pd.read_csv(files_root + 'rosters.csv')

        homeROS_df = rosters_df.copy()
        homeROS_df = homeROS_df[(homeROS_df.LOCATION == 'Home')]
        homeROS_list = homeROS_df['PLAYER_NAME'].tolist()

        ### clean up instances where home players are listed in away player on-ice columns
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['HOMEON_6']] = pbp_final['HOMEON_5']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['HOMEON_5']] = pbp_final['HOMEON_4']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['HOMEON_4']] = pbp_final['HOMEON_3']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['HOMEON_3']] = pbp_final['HOMEON_2']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['HOMEON_2']] = pbp_final['HOMEON_1']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['HOMEON_1']] = pbp_final['AWAYON_6']; pbp_final
        
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['HOMEON_6']] = pbp_final['HOMEON_5']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['HOMEON_5']] = pbp_final['HOMEON_4']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['HOMEON_4']] = pbp_final['HOMEON_3']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['HOMEON_3']] = pbp_final['HOMEON_2']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['HOMEON_2']] = pbp_final['HOMEON_1']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['HOMEON_1']] = pbp_final['AWAYON_5']; pbp_final
        
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['HOMEON_6']] = pbp_final['HOMEON_5']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['HOMEON_5']] = pbp_final['HOMEON_4']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['HOMEON_4']] = pbp_final['HOMEON_3']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['HOMEON_3']] = pbp_final['HOMEON_2']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['HOMEON_2']] = pbp_final['HOMEON_1']; pbp_final
        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['HOMEON_1']] = pbp_final['AWAYON_4']; pbp_final

        for player in homeROS_list:
            pbp_final.loc[(pbp_final.AWAYON_4 == player), ['AWAYON_4']] = ''; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_5 == player), ['AWAYON_5']] = ''; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_6 == player), ['AWAYON_6']] = ''; pbp_final

        if pbp_final['PERIOD'].max() == 5:
            ### ensure the player taking a shootout attempt is recorded as the sole on-ice participant for the shooter's team
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['AWAYON_1']] = pbp_final['PLAYER_A']; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['AWAYON_2']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['AWAYON_3']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['AWAYON_4']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['AWAYON_5']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['AWAYON_6']] = ''; pbp_final            
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_1']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_2']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_3']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_4']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_5']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_6']] = ''; pbp_final

            
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['HOMEON_1']] = pbp_final['PLAYER_A']; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_2']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_3']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_4']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_5']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_6']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_1']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_2']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_3']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_4']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_5']] = ''; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_6']] = ''; pbp_final
        
            ### generate goalie lists from the rosters
            home_goalies_df = rosters_df.copy()
            home_goalies_df = home_goalies_df[(home_goalies_df.LOCATION == 'Home') & (home_goalies_df.PLAYER_POS == 'G')]
            home_goalies = home_goalies_df['PLAYER_NAME'].tolist()

            away_goalies_df = rosters_df.copy()        
            away_goalies_df = away_goalies_df[(away_goalies_df.LOCATION == 'Away') & (away_goalies_df.PLAYER_POS == 'G')]
            away_goalies = away_goalies_df['PLAYER_NAME'].tolist()
        
            ### create a list for each team of the on-ice players for the last event registered in overtime for games that ended in a shootout
            ot_pbp_df = pbp_final.copy()
            ot_pbp_df = ot_pbp_df[(ot_pbp_df['PERIOD'] == 4) & (ot_pbp_df['HOME_STATE'] != 'EN') & (ot_pbp_df['AWAY_STATE'] != 'EN')]
            ot_seconds_max = ot_pbp_df['SECONDS_GONE'].max()

            last_event = ot_pbp_df[(ot_pbp_df['PERIOD'] == 4) & (ot_pbp_df['SECONDS_GONE'] == ot_seconds_max)]

            last_homeON_1 = last_event['HOMEON_1'].values[0]
            last_homeON_2 = last_event['HOMEON_2'].values[0]
            last_homeON_3 = last_event['HOMEON_3'].values[0]
            last_homeON_4 = last_event['HOMEON_4'].values[0]
            last_homeON_5 = last_event['HOMEON_5'].values[0]
            last_homeON_6 = last_event['HOMEON_6'].values[0]          
            last_homeON_list = [last_homeON_1, last_homeON_2, last_homeON_3, last_homeON_4, last_homeON_5, last_homeON_6]

            for goalie in home_goalies:
                if goalie in last_homeON_list:
                    home_shootout_goalie = goalie
                    
            last_awayON_1 = last_event['AWAYON_1'].values[0]
            last_awayON_2 = last_event['AWAYON_2'].values[0]
            last_awayON_3 = last_event['AWAYON_3'].values[0]
            last_awayON_4 = last_event['AWAYON_4'].values[0]
            last_awayON_5 = last_event['AWAYON_5'].values[0]
            last_awayON_6 = last_event['AWAYON_6'].values[0]          
            last_awayON_list = [last_awayON_1, last_awayON_2, last_awayON_3, last_awayON_4, last_awayON_5, last_awayON_6]

            for goalie in away_goalies:
                if goalie in last_awayON_list:
                    away_shootout_goalie = goalie
            
            #### ensure the goalie facing a shootout attempt is recorded as the sole on-ice participant for the goalie's team
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == away),['HOMEON_1']] = home_shootout_goalie; pbp_final
            pbp_final.loc[(pbp_final.PERIOD == 5) & (pbp_final.TEAM == home),['AWAYON_1']] = away_shootout_goalie; pbp_final

        ### filter out the following events in order to standardize what makes it into the play-by-play output for any given season
        pbp_final = pbp_final[(pbp_final.EVENT != 'Period.Start') & (pbp_final.EVENT != 'Period.End') & (pbp_final.EVENT != 'SOC')]

        ### make sure all rows have the proper season and game ids
        pbp_final.loc[(pbp_final.SEASON != int(season_id)), ['SEASON']] = season_id; pbp_final
        pbp_final.loc[(pbp_final.GAME_ID != int(game_id)), ['GAME_ID']] = game_id; pbp_final
        
        ### replace names for special name cases
        if home == 'CAR':
            pbp_final.loc[(pbp_final.HOMEON_1 == 'SEBASTIAN.AHO'),['HOMEON_1']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_2 == 'SEBASTIAN.AHO'),['HOMEON_2']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_3 == 'SEBASTIAN.AHO'),['HOMEON_3']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_4 == 'SEBASTIAN.AHO'),['HOMEON_4']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_5 == 'SEBASTIAN.AHO'),['HOMEON_5']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_6 == 'SEBASTIAN.AHO'),['HOMEON_6']] = 'SEBASTIAN.A.AHO'; pbp_final
        elif away == 'CAR':
            pbp_final.loc[(pbp_final.AWAYON_1 == 'SEBASTIAN.AHO'),['AWAYON_1']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_2 == 'SEBASTIAN.AHO'),['AWAYON_2']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_3 == 'SEBASTIAN.AHO'),['AWAYON_3']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_4 == 'SEBASTIAN.AHO'),['AWAYON_4']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_5 == 'SEBASTIAN.AHO'),['AWAYON_5']] = 'SEBASTIAN.A.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_6 == 'SEBASTIAN.AHO'),['AWAYON_6']] = 'SEBASTIAN.A.AHO'; pbp_final            

        if home == 'NYI':
            pbp_final.loc[(pbp_final.HOMEON_1 == 'SEBASTIAN.AHO'),['HOMEON_1']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_2 == 'SEBASTIAN.AHO'),['HOMEON_2']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_3 == 'SEBASTIAN.AHO'),['HOMEON_3']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_4 == 'SEBASTIAN.AHO'),['HOMEON_4']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_5 == 'SEBASTIAN.AHO'),['HOMEON_5']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.HOMEON_6 == 'SEBASTIAN.AHO'),['HOMEON_6']] = 'SEBASTIAN.J.AHO'; pbp_final
        elif away == 'NYI':
            pbp_final.loc[(pbp_final.AWAYON_1 == 'SEBASTIAN.AHO'),['AWAYON_1']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_2 == 'SEBASTIAN.AHO'),['AWAYON_2']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_3 == 'SEBASTIAN.AHO'),['AWAYON_3']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_4 == 'SEBASTIAN.AHO'),['AWAYON_4']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_5 == 'SEBASTIAN.AHO'),['AWAYON_5']] = 'SEBASTIAN.J.AHO'; pbp_final
            pbp_final.loc[(pbp_final.AWAYON_6 == 'SEBASTIAN.AHO'),['AWAYON_6']] = 'SEBASTIAN.J.AHO'; pbp_final   
        
        ### write the file to csv, without an index column
        pbp_final.to_csv(pbp_parsed, index=False)


        print('Finished merging files for ' + season_id + ' ' + game_id)

        
    if int(season_id) < 20102011:
     
        ### load the main and ESPN play-by-play files into pandas
        pbp_df = pd.read_csv(pbp_parsed)

        ESPN_df = pd.read_csv(ESPN_parsed)
        
        if int(season_id) == 20062007:
            
            ### create a goal dataframe and then remove goal events and the home and away on-ice columns from the main play-by-play
            goals_df = pbp_df[(pbp_df['EVENT_TYPE'] == 'Goal')]
            goals_df = goals_df.rename(columns={'HOMEON_1': 'HOMEON_1_X', 'HOMEON_2': 'HOMEON_2_X', 'HOMEON_3': 'HOMEON_3_X', 'HOMEON_4': 'HOMEON_4_X', 'HOMEON_5': 'HOMEON_5_X', 'HOMEON_6': 'HOMEON_6_X', 'AWAYON_1': 'AWAYON_1_X', 'AWAYON_2': 'AWAYON_2_X', 'AWAYON_3': 'AWAYON_3_X', 'AWAYON_4': 'AWAYON_4_X', 'AWAYON_5': 'AWAYON_5_X', 'AWAYON_6': 'AWAYON_6_X'})
            goals_df = goals_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'GAME_TYPE', 'HOME_RESULT', 'AWAY_RESULT', 'PERIOD', 'TIME_LEFT', 'TIME_GONE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL', 'EVENT', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'TEAM', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C'])
            
            pbp_df = pbp_df.drop(columns=['HOME_STATE', 'AWAY_STATE', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
            
            ### load the TOI matrix into pandas
            TOI_df = pd.read_csv(TOI_parsed)

            ### drop extraneous columns from the TOI dataframe
            TOI_df = TOI_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'EVENT', 'TEAM', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SITUATION', 'AWAY_SITUATION'])
            
            ### join the contents of the main play-by-play and TOI matrix
            pbp_df = pd.merge(pbp_df, TOI_df, on='SECONDS_GONE', how='left')
                       
            ### rank and sort events registered at the same second in a way that makes chronological sense
            pbp_df['EVENT_RANK'] = int()
            pbp_df['EVENT_RANK_2'] = int()
            pbp_df.loc[(pbp_df.EVENT != 'Stoppage') | (pbp_df.EVENT != 'Faceoff'),['EVENT_RANK']] = 1; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Stoppage'),['EVENT_RANK']] = 2; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff'),['EVENT_RANK']] = 3; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Shot'),['EVENT_RANK_2']] = 1; pbp_df                        
            pbp_df.loc[(pbp_df.EVENT == 'Penalty'),['EVENT_RANK_2']] = 2; pbp_df            
            
            pbp_df = pbp_df.sort_values(by=['PERIOD', 'SECONDS_GONE', 'EVENT_RANK', 'EVENT_RANK_2'])
            pbp_df = pbp_df.drop(columns=['EVENT_RANK', 'EVENT_RANK_2'])
          
            ### compare the main play-by-play's state for each event with the TOI-derived state; make desired adjustments         
            pbp_df.loc[(pbp_df.HOME_STATE_DETAIL == 'EV') & (pbp_df.HOME_STATE == 'PP'),['HOME_STATE']] = 'EV'; pbp_df
            pbp_df.loc[(pbp_df.HOME_STATE_DETAIL == 'EV') & (pbp_df.HOME_STATE == 'SH'),['HOME_STATE']] = 'EV'; pbp_df
            pbp_df.loc[(pbp_df.HOME_STATE_DETAIL == 'EV') & (pbp_df.HOME_STATE != 'EN') & (pbp_df.HOME_STRENGTH != '5v5') | (pbp_df.HOME_STATE_DETAIL == 'EV') & (pbp_df.HOME_STATE != 'EN') & (pbp_df.HOME_STRENGTH != '4v4'),['HOME_STRENGTH']] = '5v5'; pbp_df           
            pbp_df.loc[(pbp_df.HOME_STATE_DETAIL == 'PS'),['HOME_STATE']] = 'PS'; pbp_df
            pbp_df.loc[(pbp_df.HOME_STATE_DETAIL == 'PS') & (pbp_df.TEAM == home),['HOME_STRENGTH']] = '1v0'; pbp_df
            pbp_df.loc[(pbp_df.HOME_STATE_DETAIL == 'PS') & (pbp_df.TEAM == away),['HOME_STRENGTH']] = '0v1'; pbp_df
            
            pbp_df.loc[(pbp_df.AWAY_STATE_DETAIL == 'EV') & (pbp_df.AWAY_STATE == 'PP'),['AWAY_STATE']] = 'EV'; pbp_df
            pbp_df.loc[(pbp_df.AWAY_STATE_DETAIL == 'EV') & (pbp_df.AWAY_STATE == 'SH'),['AWAY_STATE']] = 'EV'; pbp_df            
            pbp_df.loc[(pbp_df.AWAY_STATE_DETAIL == 'EV') & (pbp_df.AWAY_STATE != 'EN') & (pbp_df.AWAY_STRENGTH != '5v5') | (pbp_df.AWAY_STATE_DETAIL == 'EV') & (pbp_df.AWAY_STATE != 'EN') & (pbp_df.AWAY_STRENGTH != '4v4'),['AWAY_STRENGTH']] = '5v5'; pbp_df            
            pbp_df.loc[(pbp_df.AWAY_STATE_DETAIL == 'PS'),['AWAY_STATE']] = 'PS'; pbp_df
            pbp_df.loc[(pbp_df.AWAY_STATE_DETAIL == 'PS') & (pbp_df.TEAM == away),['AWAY_STRENGTH']] = '1v0'; pbp_df
            pbp_df.loc[(pbp_df.AWAY_STATE_DETAIL == 'PS') & (pbp_df.TEAM == home),['AWAY_STRENGTH']] = '0v1'; pbp_df
            
            ### create columns for previous and following events, event types and states for adjusting erroneous state and strength for faceoffs
            pbp_df['PREV_EVENT'] = pbp_df['EVENT'].shift(1)
            pbp_df['NEXT_EVENT'] = pbp_df['EVENT'].shift(-1)
            pbp_df['PREV_EVENT_TYPE'] = pbp_df['EVENT_TYPE'].shift(1)
            pbp_df['NEXT_EVENT_TYPE'] = pbp_df['EVENT_TYPE'].shift(-1)
            pbp_df['PREV_HOME_STATE'] = pbp_df['HOME_STATE'].shift(1)
            pbp_df['NEXT_HOME_STATE'] = pbp_df['HOME_STATE'].shift(-1)            
            pbp_df['PREV_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(1)
            pbp_df['NEXT_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(-1)
            pbp_df['PREV_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(1)
            pbp_df['NEXT_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(-1)            
            pbp_df['PREV_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(1)
            pbp_df['NEXT_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(-1)

            pbp_df.loc[(pbp_df.EVENT == 'Faceoff'),['HOME_STATE']] = pbp_df['NEXT_HOME_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff'),['HOME_STRENGTH']] = pbp_df['NEXT_HOME_STRENGTH']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff'),['AWAY_STATE']] = pbp_df['NEXT_AWAY_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff'),['AWAY_STRENGTH']] = pbp_df['NEXT_AWAY_STRENGTH']; pbp_df

            pbp_df = pbp_df.drop(columns=['PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH'])

            ### recreate columns for previous and following events, event types and states for adjusting erroneous state and strength for stoppages
            pbp_df['PREV_HOME_STATE'] = pbp_df['HOME_STATE'].shift(1)
            pbp_df['NEXT_HOME_STATE'] = pbp_df['HOME_STATE'].shift(-1)            
            pbp_df['PREV_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(1)
            pbp_df['NEXT_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(-1)
            pbp_df['PREV_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(1)
            pbp_df['NEXT_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(-1)            
            pbp_df['PREV_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(1)
            pbp_df['NEXT_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(-1)

            pbp_df.loc[(pbp_df.EVENT == 'Stoppage') ,['HOME_STATE']] = pbp_df['PREV_HOME_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Stoppage'),['HOME_STRENGTH']] = pbp_df['PREV_HOME_STRENGTH']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Stoppage'),['AWAY_STATE']] = pbp_df['PREV_AWAY_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Stoppage'),['AWAY_STRENGTH']] = pbp_df['PREV_AWAY_STRENGTH']; pbp_df

            pbp_df = pbp_df.drop(columns=['PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH'])

            ### recreate columns for previous and following events, event types and states for adjusting erroneous state and strength for penalties
            pbp_df['PREV_HOME_STATE'] = pbp_df['HOME_STATE'].shift(1)
            pbp_df['NEXT_HOME_STATE'] = pbp_df['HOME_STATE'].shift(-1)            
            pbp_df['PREV_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(1)
            pbp_df['NEXT_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(-1)
            pbp_df['PREV_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(1)
            pbp_df['NEXT_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(-1)            
            pbp_df['PREV_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(1)
            pbp_df['NEXT_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(-1)

            pbp_df.loc[(pbp_df.EVENT == 'Penalty') ,['HOME_STATE']] = pbp_df['PREV_HOME_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Penalty'),['HOME_STRENGTH']] = pbp_df['PREV_HOME_STRENGTH']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Penalty'),['AWAY_STATE']] = pbp_df['PREV_AWAY_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Penalty'),['AWAY_STRENGTH']] = pbp_df['PREV_AWAY_STRENGTH']; pbp_df

            pbp_df = pbp_df.drop(columns=['PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH'])

            ### recreate columns for previous and following events, event types and states for adjusting erroneous state and strength for remaining faceoffs
            pbp_df['PREV_HOME_STATE'] = pbp_df['HOME_STATE'].shift(1)
            pbp_df['NEXT_HOME_STATE'] = pbp_df['HOME_STATE'].shift(-1)            
            pbp_df['PREV_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(1)
            pbp_df['NEXT_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(-1)
            pbp_df['PREV_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(1)
            pbp_df['NEXT_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(-1)            
            pbp_df['PREV_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(1)
            pbp_df['NEXT_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(-1)

            pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.NEXT_EVENT == 'Penalty'),['HOME_STATE']] = pbp_df['PREV_HOME_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.NEXT_EVENT == 'Penalty'),['HOME_STRENGTH']] = pbp_df['PREV_HOME_STRENGTH']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.NEXT_EVENT == 'Penalty'),['AWAY_STATE']] = pbp_df['PREV_AWAY_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Faceoff') & (pbp_df.NEXT_EVENT == 'Penalty'),['AWAY_STRENGTH']] = pbp_df['PREV_AWAY_STRENGTH']; pbp_df

            pbp_df = pbp_df.drop(columns=['PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH'])

            ### recreate columns for previous and following events, event types and states for adjusting erroneous state and strength for remaining penalties and the last event
            pbp_df['PREV_HOME_STATE'] = pbp_df['HOME_STATE'].shift(1)
            pbp_df['NEXT_HOME_STATE'] = pbp_df['HOME_STATE'].shift(-1)            
            pbp_df['PREV_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(1)
            pbp_df['NEXT_AWAY_STATE'] = pbp_df['AWAY_STATE'].shift(-1)
            pbp_df['PREV_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(1)
            pbp_df['NEXT_HOME_STRENGTH'] = pbp_df['HOME_STRENGTH'].shift(-1)            
            pbp_df['PREV_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(1)
            pbp_df['NEXT_AWAY_STRENGTH'] = pbp_df['AWAY_STRENGTH'].shift(-1)

            pbp_df.loc[(pbp_df.EVENT == 'Penalty') & (pbp_df.PREV_EVENT == 'Faceoff'),['HOME_STATE']] = pbp_df['PREV_HOME_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Penalty') & (pbp_df.PREV_EVENT == 'Faceoff'),['HOME_STRENGTH']] = pbp_df['PREV_HOME_STRENGTH']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Penalty') & (pbp_df.PREV_EVENT == 'Faceoff'),['AWAY_STATE']] = pbp_df['PREV_AWAY_STATE']; pbp_df
            pbp_df.loc[(pbp_df.EVENT == 'Penalty') & (pbp_df.PREV_EVENT == 'Faceoff'),['AWAY_STRENGTH']] = pbp_df['PREV_AWAY_STRENGTH']; pbp_df

            pbp_df.loc[(pbp_df.HOME_STATE.isnull()),['HOME_STATE']] = pbp_df['PREV_HOME_STATE']; pbp_df
            pbp_df.loc[(pbp_df.HOME_STRENGTH.isnull()),['HOME_STRENGTH']] = pbp_df['PREV_HOME_STRENGTH']; pbp_df
            pbp_df.loc[(pbp_df.AWAY_STATE.isnull()),['AWAY_STATE']] = pbp_df['PREV_AWAY_STATE']; pbp_df
            pbp_df.loc[(pbp_df.AWAY_STRENGTH.isnull()),['AWAY_STRENGTH']] = pbp_df['PREV_AWAY_STRENGTH']; pbp_df

            pbp_df = pbp_df.drop(columns=['PREV_HOME_STATE', 'NEXT_HOME_STATE', 'PREV_AWAY_STATE', 'NEXT_AWAY_STATE', 'PREV_HOME_STRENGTH', 'NEXT_HOME_STRENGTH', 'PREV_AWAY_STRENGTH', 'NEXT_AWAY_STRENGTH'])
            pbp_df = pbp_df.drop(columns=['PREV_EVENT', 'NEXT_EVENT', 'PREV_EVENT_TYPE', 'NEXT_EVENT_TYPE'])
            pbp_df = pbp_df.drop(columns=['HOME_STATE_DETAIL', 'AWAY_STATE_DETAIL'])

            ### join the contents of the main play-by-play and goals dataframes; replace on-ice players as necessary
            pbp_df = pd.merge(pbp_df, goals_df, on=['SECONDS_GONE', 'EVENT_TYPE'], how='left')

            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['HOMEON_1']] = pbp_df['HOMEON_1_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['HOMEON_2']] = pbp_df['HOMEON_2_X']; pbp_df            
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['HOMEON_3']] = pbp_df['HOMEON_3_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['HOMEON_4']] = pbp_df['HOMEON_4_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['HOMEON_5']] = pbp_df['HOMEON_5_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['HOMEON_6']] = pbp_df['HOMEON_6_X']; pbp_df

            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['AWAYON_1']] = pbp_df['AWAYON_1_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['AWAYON_2']] = pbp_df['AWAYON_2_X']; pbp_df            
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['AWAYON_3']] = pbp_df['AWAYON_3_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['AWAYON_4']] = pbp_df['AWAYON_4_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['AWAYON_5']] = pbp_df['AWAYON_5_X']; pbp_df
            pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal'),['AWAYON_6']] = pbp_df['AWAYON_6_X']; pbp_df

            pbp_df = pbp_df.drop(columns=['HOMEON_1_X', 'HOMEON_2_X', 'HOMEON_3_X', 'HOMEON_4_X', 'HOMEON_5_X', 'HOMEON_6_X', 'AWAYON_1_X', 'AWAYON_2_X', 'AWAYON_3_X', 'AWAYON_4_X', 'AWAYON_5_X', 'AWAYON_6_X'])

            ### replace blank values in the on-ice columns for each team
            pbp_df.loc[(pbp_df.HOMEON_1.isnull()),['HOMEON_1']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.HOMEON_2.isnull()),['HOMEON_2']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.HOMEON_3.isnull()),['HOMEON_3']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.HOMEON_4.isnull()),['HOMEON_4']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.HOMEON_5.isnull()),['HOMEON_5']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.HOMEON_6.isnull()),['HOMEON_6']] = '$'; pbp_df

            pbp_df.loc[(pbp_df.AWAYON_1.isnull()),['AWAYON_1']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.AWAYON_2.isnull()),['AWAYON_2']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.AWAYON_3.isnull()),['AWAYON_3']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.AWAYON_4.isnull()),['AWAYON_4']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.AWAYON_5.isnull()),['AWAYON_5']] = '$'; pbp_df
            pbp_df.loc[(pbp_df.AWAYON_6.isnull()),['AWAYON_6']] = '$'; pbp_df
            
            ### fix even-strength team strengths as necessary
            pbp_df.loc[(pbp_df.SECONDS_GONE > 3600) & (pbp_df.HOME_STATE == 'EV') & (pbp_df.AWAY_STATE == 'EV') & (pbp_df.HOME_STRENGTH == '5v5') & (pbp_df.AWAY_STRENGTH == '5v5'),['HOME_STRENGTH']] = '4v4'; pbp_df
            pbp_df.loc[(pbp_df.SECONDS_GONE > 3600) & (pbp_df.HOME_STATE == 'EV') & (pbp_df.AWAY_STATE == 'EV') & (pbp_df.HOME_STRENGTH == '4v4') & (pbp_df.AWAY_STRENGTH == '5v5'),['AWAY_STRENGTH']] = '4v4'; pbp_df            
            
            ### ensure that when both players have a player penalized, the game strength for each team is recorded as 4v4
            pbp_df.loc[(pbp_df.HOME_PENALTY == 1) & (pbp_df.AWAY_PENALTY == 1) & (pbp_df.HOME_STATE == 'EV') & (pbp_df.AWAY_STATE == 'EV'),['HOME_STRENGTH']] = '4v4'; pbp_df
            pbp_df.loc[(pbp_df.HOME_PENALTY == 1) & (pbp_df.AWAY_PENALTY == 1) & (pbp_df.HOME_STATE == 'EV') & (pbp_df.AWAY_STATE == 'EV'),['AWAY_STRENGTH']] = '4v4'; pbp_df
                        
        ### remove extraneous columns from the ESPN play-by-play; add event x and y coordinates from the ESPN play-by-play to the main play-by-play
        ESPN_df = ESPN_df.drop(columns=['SEASON', 'GAME_ID', 'DATE', 'HOME', 'AWAY', 'PERIOD', 'TIME_LEFT', 'TIME_GONE', 'TEAM'])

        ESPN_nonshots = ESPN_df.copy()
        ESPN_nonshots = ESPN_nonshots[(ESPN_nonshots['EVENT'] != 'Shot')]      
        ESPN_nonshots = ESPN_nonshots.drop(columns=['EVENT_TYPE'])

        pbp_df = pd.merge(pbp_df, ESPN_nonshots, on=['SECONDS_GONE', 'EVENT'], how='left')        

        ESPN_shots = ESPN_df.copy()
        ESPN_shots = ESPN_shots[(ESPN_shots['EVENT'] == 'Shot')]
        ESPN_shots = ESPN_shots.rename(columns={'X_1': 'X_1_B', 'Y_1': 'Y_1_B', 'X_2': 'X_2_B', 'Y_2': 'Y_2_B'})

        pbp_df = pd.merge(pbp_df, ESPN_shots, on=['SECONDS_GONE', 'EVENT', 'EVENT_TYPE'], how='left')
        pbp_df.loc[(pbp_df.EVENT == 'Shot'),['X_1']] = pbp_df['X_1_B']; pbp_df
        pbp_df.loc[(pbp_df.EVENT == 'Shot'),['Y_1']] = pbp_df['Y_1_B']; pbp_df
        pbp_df.loc[(pbp_df.EVENT == 'Shot'),['X_2']] = pbp_df['X_2_B']; pbp_df
        pbp_df.loc[(pbp_df.EVENT == 'Shot'),['Y_2']] = pbp_df['Y_2_B']; pbp_df
        pbp_df = pbp_df.drop(columns=['X_1_B', 'Y_1_B', 'X_2_B', 'Y_2_B'])
        
        ### make adjustments to the XY values in order to make categorize home and away events by zone
        if int(season_id) == 20062007:
            pbp_df.loc[(pbp_df.X_1.notnull()) & (pbp_df.TEAM == away),['X_1']] *= -1; pbp_df
            pbp_df.loc[(pbp_df.Y_1.notnull()) & (pbp_df.TEAM == away),['Y_1']] *= -1; pbp_df
            pbp_df.loc[(pbp_df.X_2.notnull()) & (pbp_df.TEAM == home),['X_2']] *= -1; pbp_df
            pbp_df.loc[(pbp_df.Y_2.notnull()) & (pbp_df.TEAM == home),['Y_2']] *= -1; pbp_df

        ### beginning with the 20072008 season, the 2nd period coordinates need to be flipped back to match the 1st and 3rd zones
        if int(season_id) >= 20072008:
            pbp_df.loc[(pbp_df.PERIOD != 2) & (pbp_df.X_1.notnull()) & (pbp_df.TEAM == away),['X_1']] *= -1; pbp_df
            pbp_df.loc[(pbp_df.PERIOD != 2) & (pbp_df.Y_1.notnull()) & (pbp_df.TEAM == away),['Y_1']] *= -1; pbp_df
            pbp_df.loc[(pbp_df.PERIOD != 2) & (pbp_df.X_1.notnull()) & (pbp_df.TEAM == home),['X_1']] *= -1; pbp_df
            pbp_df.loc[(pbp_df.PERIOD != 2) & (pbp_df.Y_1.notnull()) & (pbp_df.TEAM == home),['Y_1']] *= -1; pbp_df
        
        pbp_df.loc[(pbp_df.EVENT == 'Shot') & (pbp_df.TEAM == home),['HOME_ZONE']] = 'Offensive'; pbp_df
        pbp_df.loc[(pbp_df.EVENT == 'Shot') & (pbp_df.TEAM == home),['AWAY_ZONE']] = 'Defensive'; pbp_df
        pbp_df.loc[(pbp_df.EVENT == 'Shot') & (pbp_df.TEAM == away),['HOME_ZONE']] = 'Defensive'; pbp_df
        pbp_df.loc[(pbp_df.EVENT == 'Shot') & (pbp_df.TEAM == away),['AWAY_ZONE']] = 'Offensive'; pbp_df
               
        pbp_df.loc[(pbp_df.X_1 > 25),['HOME_ZONE']] = 'Offensive'; pbp_df
        pbp_df.loc[(pbp_df.X_1 > 25),['AWAY_ZONE']] = 'Defensive'; pbp_df
        pbp_df.loc[(pbp_df.X_2 > 25),['HOME_ZONE']] = 'Offensive'; pbp_df
        pbp_df.loc[(pbp_df.X_2 > 25),['AWAY_ZONE']] = 'Defensive'; pbp_df

        pbp_df.loc[(pbp_df.X_1 < 25),['HOME_ZONE']] = 'Defensive'; pbp_df
        pbp_df.loc[(pbp_df.X_1 < 25),['AWAY_ZONE']] = 'Offensive'; pbp_df
        pbp_df.loc[(pbp_df.X_2 < 25),['HOME_ZONE']] = 'Defensive'; pbp_df
        pbp_df.loc[(pbp_df.X_2 < 25),['AWAY_ZONE']] = 'Offensive'; pbp_df

        pbp_df.loc[(pbp_df.X_1 > -25) & (pbp_df.X_1 < 25),['HOME_ZONE']] = 'Neutral'; pbp_df
        pbp_df.loc[(pbp_df.X_1 > -25) & (pbp_df.X_1 < 25),['AWAY_ZONE']] = 'Neutral'; pbp_df
               
        ### rearrange the column arrangement to match how output for games in the 20102011 season and beyond is structured
        if int(season_id) >= 20072008:            
            move_strengths_states_XY = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,43,44,45,46,31,32,33,34,35,36,37,38,39,40,41,42]
            pbp_df = pbp_df[pbp_df.columns[move_strengths_states_XY]]

        if int(season_id) == 20062007:           
            move_strengths_states_XY = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,27,28,29,30,43,44,18,19,20,21,22,23,24,25,26,45,46,47,48,31,32,33,34,35,36,37,38,39,40,41,42]
            pbp_df = pbp_df[pbp_df.columns[move_strengths_states_XY]]
            
            if load_pbp != 'true':
                missing_onice_patch = TOI_df.rename(columns={'HOMEON_1': 'HOMEON_1_X', 'HOMEON_2': 'HOMEON_2_X', 'HOMEON_3': 'HOMEON_3_X', 'HOMEON_4': 'HOMEON_4_X', 'HOMEON_5': 'HOMEON_5_X', 'HOMEON_6': 'HOMEON_6_X', 'AWAYON_1': 'AWAYON_1_X', 'AWAYON_2': 'AWAYON_2_X', 'AWAYON_3': 'AWAYON_3_X', 'AWAYON_4': 'AWAYON_4_X', 'AWAYON_5': 'AWAYON_5_X', 'AWAYON_6': 'AWAYON_6_X'})
                missing_onice_patch = missing_onice_patch.drop(columns=['HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_STATE', 'AWAY_STATE', 'HOME_PENALTY', 'AWAY_PENALTY'])
                
                pbp_df = pd.merge(pbp_df, missing_onice_patch, on='SECONDS_GONE', how='left')
                
                ### replace blank values in the on-ice columns for each team
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.HOME_STATE != 'PS') & (pbp_df.HOMEON_1 == '$') & (pbp_df.HOMEON_2 == '$') & (pbp_df.HOMEON_3 == '$') & (pbp_df.HOMEON_4 == '$') & (pbp_df.HOMEON_5 == '$') & (pbp_df.HOMEON_6 == '$'),['HOMEON_1']] = pbp_df['HOMEON_1_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.HOME_STATE != 'PS') & (pbp_df.HOMEON_2 == '$') & (pbp_df.HOMEON_3 == '$') & (pbp_df.HOMEON_4 == '$') & (pbp_df.HOMEON_5 == '$') & (pbp_df.HOMEON_6 == '$'),['HOMEON_2']] = pbp_df['HOMEON_2_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.HOME_STATE != 'PS') & (pbp_df.HOMEON_3 == '$') & (pbp_df.HOMEON_4 == '$') & (pbp_df.HOMEON_5 == '$') & (pbp_df.HOMEON_6 == '$'),['HOMEON_3']] = pbp_df['HOMEON_3_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.HOME_STATE != 'PS') & (pbp_df.HOMEON_4 == '$') & (pbp_df.HOMEON_5 == '$') & (pbp_df.HOMEON_6 == '$'),['HOMEON_4']] = pbp_df['HOMEON_4_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.HOME_STATE != 'PS') & (pbp_df.HOMEON_5 == '$') & (pbp_df.HOMEON_6 == '$'),['HOMEON_5']] = pbp_df['HOMEON_5_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.HOME_STATE != 'PS') & (pbp_df.HOMEON_6 == '$'),['HOMEON_6']] = pbp_df['HOMEON_6_X']; pbp_df
    
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.AWAY_STATE != 'PS') & (pbp_df.AWAYON_1 == '$') & (pbp_df.AWAYON_2 == '$') & (pbp_df.AWAYON_3 == '$') & (pbp_df.AWAYON_4 == '$') & (pbp_df.AWAYON_5 == '$') & (pbp_df.AWAYON_6 == '$'),['AWAYON_1']] = pbp_df['AWAYON_1_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.AWAY_STATE != 'PS') & (pbp_df.AWAYON_2 == '$') & (pbp_df.AWAYON_3 == '$') & (pbp_df.AWAYON_4 == '$') & (pbp_df.AWAYON_5 == '$') & (pbp_df.AWAYON_6 == '$'),['AWAYON_2']] = pbp_df['AWAYON_2_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.AWAY_STATE != 'PS') & (pbp_df.AWAYON_3 == '$') & (pbp_df.AWAYON_4 == '$') & (pbp_df.AWAYON_5 == '$') & (pbp_df.AWAYON_6 == '$'),['AWAYON_3']] = pbp_df['AWAYON_3_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.AWAY_STATE != 'PS') & (pbp_df.AWAYON_4 == '$') & (pbp_df.AWAYON_5 == '$') & (pbp_df.AWAYON_6 == '$'),['AWAYON_4']] = pbp_df['AWAYON_4_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.AWAY_STATE != 'PS') & (pbp_df.AWAYON_5 == '$') & (pbp_df.AWAYON_6 == '$'),['AWAYON_5']] = pbp_df['AWAYON_5_X']; pbp_df
                pbp_df.loc[(pbp_df.EVENT_TYPE == 'Goal') & (pbp_df.AWAY_STATE != 'PS') & (pbp_df.AWAYON_6 == '$'),['AWAYON_6']] = pbp_df['AWAYON_6_X']; pbp_df
                
                pbp_df = pbp_df.drop(columns=['HOMEON_1_X', 'HOMEON_2_X', 'HOMEON_3_X', 'HOMEON_4_X', 'HOMEON_5_X', 'HOMEON_6_X', 'AWAYON_1_X', 'AWAYON_2_X', 'AWAYON_3_X', 'AWAYON_4_X', 'AWAYON_5_X', 'AWAYON_6_X'])

        ### clean up any instances of the most-likely empty-net situations where more than six skaters are recorded for a team
        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '7v5') & (pbp_df.AWAY_STRENGTH == '5v7'),['HOME_STRENGTH']] = '6v5'; pbp_df           
        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '6v5') & (pbp_df.AWAY_STRENGTH == '5v7'),['AWAY_STRENGTH']] = '5v6'; pbp_df           

        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '8v5') & (pbp_df.AWAY_STRENGTH == '5v8'),['HOME_STRENGTH']] = '6v5'; pbp_df           
        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '6v5') & (pbp_df.AWAY_STRENGTH == '5v8'),['AWAY_STRENGTH']] = '5v6'; pbp_df           


        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '5v7') & (pbp_df.AWAY_STRENGTH == '7v5'),['AWAY_STRENGTH']] = '6v5'; pbp_df           
        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '5v7') & (pbp_df.AWAY_STRENGTH == '6v5'),['HOME_STRENGTH']] = '5v6'; pbp_df           

        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '5v8') & (pbp_df.AWAY_STRENGTH == '8v5'),['AWAY_STRENGTH']] = '6v5'; pbp_df           
        pbp_df.loc[(pbp_df.HOME_STATE == 'EN') & (pbp_df.AWAY_STATE == 'EN') & (pbp_df.HOME_STRENGTH == '5v8') & (pbp_df.AWAY_STRENGTH == '6v5'),['HOME_STRENGTH']] = '5v6'; pbp_df
                                
        ### final touches
        if int(season_id) == 20062007:
            pbp_df = pbp_df.replace('$', '')

            pbp_df = pbp_df[(pbp_df['EVENT_TYPE'] != 'Empty-Net')]
            if load_pbp != 'true':              
                ### correct any instances where the season_id might be missing
                pbp_df.loc[(pbp_df.SEASON.isnull()),['SEASON']] = season_id; pbp_df

            ### remove the penalty count columns for each team
            pbp_df = pbp_df.drop(columns=['HOME_PENALTY', 'AWAY_PENALTY'])

        if pbp_df['PERIOD'].max() == 5:
            ### change the value of seconds gone for shootout events from 3901 to blank
            pbp_df.loc[(pbp_df.PERIOD == 5),['SECONDS_GONE']] = ''; pbp_df

            ### make the strengths and states for each team reflect the shootout
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['HOME_STRENGTH']] = '1v0'; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAY_STRENGTH']] = '0v1'; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOME_STRENGTH']] = '0v1'; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAY_STRENGTH']] = '1v0'; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5),['HOME_STATE']] = 'SO'; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5),['AWAY_STATE']] = 'SO'; pbp_df 

            ### ensure the player taking a shootout attempt is recorded as the sole on-ice participant for the shooter's team
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAYON_1']] = pbp_df['PLAYER_A']; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAYON_2']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAYON_3']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAYON_4']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAYON_5']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['AWAYON_6']] = ''; pbp_df            
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_1']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_2']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_3']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_4']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_5']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_6']] = ''; pbp_df

            
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['HOMEON_1']] = pbp_df['PLAYER_A']; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_2']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_3']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_4']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_5']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_6']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_1']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_2']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_3']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_4']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_5']] = ''; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_6']] = ''; pbp_df
        
            ### read in the rosters file as a dataframe; separate home from away rosters; generate goalie lists
            rosters_df = pd.read_csv(files_root + 'rosters.csv')
                
            home_roster_df = rosters_df[(rosters_df.LOCATION == 'Home') & (rosters_df.PLAYER_POS == 'G')]
            home_goalies = home_roster_df['PLAYER_NAME'].tolist()
        
            away_roster_df = rosters_df[(rosters_df.LOCATION == 'Away') & (rosters_df.PLAYER_POS == 'G')]
            away_goalies = away_roster_df['PLAYER_NAME'].tolist()
        
            ### create a list for each team of the on-ice players for the last event registered in overtime for games that ended in a shootout
            ot_pbp_df = pbp_df.copy()
            ot_pbp_df = ot_pbp_df[(ot_pbp_df['PERIOD'] == 4) & (ot_pbp_df['HOME_STATE'] != 'EN') & (ot_pbp_df['AWAY_STATE'] != 'EN')]
            ot_seconds_max = ot_pbp_df['SECONDS_GONE'].max()

            last_event = ot_pbp_df[(ot_pbp_df['PERIOD'] == 4) & (ot_pbp_df['SECONDS_GONE'] == ot_seconds_max)]

            last_homeON_1 = last_event['HOMEON_1'].values[0]
            last_homeON_2 = last_event['HOMEON_2'].values[0]
            last_homeON_3 = last_event['HOMEON_3'].values[0]
            last_homeON_4 = last_event['HOMEON_4'].values[0]
            last_homeON_5 = last_event['HOMEON_5'].values[0]
            last_homeON_6 = last_event['HOMEON_6'].values[0]          
            last_homeON_list = [last_homeON_1, last_homeON_2, last_homeON_3, last_homeON_4, last_homeON_5, last_homeON_6]

            for goalie in home_goalies:
                if goalie in last_homeON_list:
                    home_shootout_goalie = goalie
                    
            last_awayON_1 = last_event['AWAYON_1'].values[0]
            last_awayON_2 = last_event['AWAYON_2'].values[0]
            last_awayON_3 = last_event['AWAYON_3'].values[0]
            last_awayON_4 = last_event['AWAYON_4'].values[0]
            last_awayON_5 = last_event['AWAYON_5'].values[0]
            last_awayON_6 = last_event['AWAYON_6'].values[0]          
            last_awayON_list = [last_awayON_1, last_awayON_2, last_awayON_3, last_awayON_4, last_awayON_5, last_awayON_6]

            for goalie in away_goalies:
                if goalie in last_awayON_list:
                    away_shootout_goalie = goalie
            
            #### ensure the goalie facing a shootout attempt is recorded as the sole on-ice participant for the goalie's team
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == away),['HOMEON_1']] = home_shootout_goalie; pbp_df
            pbp_df.loc[(pbp_df.PERIOD == 5) & (pbp_df.TEAM == home),['AWAYON_1']] = away_shootout_goalie; pbp_df

        ### drop any duplicates            
        pbp_df = pbp_df.drop_duplicates(subset=['SECONDS_GONE', 'EVENT', 'EVENT_TYPE', 'PLAYER_A', 'PLAYER_B'], keep='first')

        ### filter out the following events in order to standardize what makes it into the play-by-play output for any given season
        pbp_df = pbp_df[(pbp_df.EVENT != 'Period.Start') & (pbp_df.EVENT != 'Period.End') & (pbp_df.EVENT != 'SOC')]

        ### make sure all rows have the proper season and game ids
        pbp_df.loc[(pbp_df.SEASON != int(season_id)), ['SEASON']] = season_id; pbp_df
        pbp_df.loc[(pbp_df.GAME_ID != int(game_id)), ['GAME_ID']] = game_id; pbp_df

        ### write to file
        pbp_df.to_csv(pbp_parsed, index=False)
 
       
        print('Finished merging files for ' + season_id + ' ' + game_id)