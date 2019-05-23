# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import pandas as pd
import parameters

def parse_ids(season_id, game_id):

    ### pull common variables from the parameters file
    files_root = parameters.files_root

    ### establish file locations and destinations
    livefeed_parsed = files_root + 'livefeed.csv'
    pbp_parsed = files_root + 'pbp.csv'
    
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
    
    ### write the file to csv, without an index column
    pbp_final.to_csv(pbp_parsed, index=False)
    
    
    print('Finished merging NHL play-by-play from the livefeed .csv and pbp .csv for ' + season_id + ' ' + game_id)