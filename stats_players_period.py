# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import csv
import pandas as pd
import numpy as np
import parameters

def parse_ids(season_id, game_id):

    # pull common variables from the parameters file
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    # establish file locations and destinations
    TOI_matrix = files_root + 'TOI_matrix.csv'
    pbp = files_root + 'pbp.csv'
    stats_individual = files_root + 'stats_players_individual_period.csv'
    stats_onice = files_root + 'stats_players_onice_period.csv'
        
    # create a dataframe for extracting TOI info; add a column with all of the on-ice players for expedited searching; derive the last on-ice second recorded
    TOI_df = pd.read_csv(TOI_matrix)
    
    TOI_df['HOMEON_5'].fillna('NaN', inplace = True)
    TOI_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    TOI_df['AWAYON_5'].fillna('NaN', inplace = True)
    TOI_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    TOI_df['HOMEON'] = TOI_df['HOMEON_1'] + ', ' + TOI_df['HOMEON_2'] + ', ' + TOI_df['HOMEON_3'] + ', ' + TOI_df['HOMEON_4'] + ', ' + TOI_df['HOMEON_5'] + ', ' + TOI_df['HOMEON_6']
    TOI_df['AWAYON'] = TOI_df['AWAYON_1'] + ', ' + TOI_df['AWAYON_2'] + ', ' + TOI_df['AWAYON_3'] + ', ' + TOI_df['AWAYON_4'] + ', ' + TOI_df['AWAYON_5'] + ', ' + TOI_df['AWAYON_6']
       
    # create a dataframe for extracting play-by-play info; add a column with all of the on-ice players for expedited searching
    pbp_df = pd.read_csv(pbp)
    pbp_df = pbp_df[(pbp_df['PERIOD'] != 5)]
    
    pbp_df['HOMEON_5'].fillna('NaN', inplace = True)
    pbp_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    pbp_df['AWAYON_5'].fillna('NaN', inplace = True)
    pbp_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    pbp_df['HOMEON'] = pbp_df['HOMEON_1'] + ', ' + pbp_df['HOMEON_2'] + ', ' + pbp_df['HOMEON_3'] + ', ' + pbp_df['HOMEON_4'] + ', ' + pbp_df['HOMEON_5'] + ', ' + pbp_df['HOMEON_6']
    pbp_df['AWAYON'] = pbp_df['AWAYON_1'] + ', ' + pbp_df['AWAYON_2'] + ', ' + pbp_df['AWAYON_3'] + ', ' + pbp_df['AWAYON_4'] + ', ' + pbp_df['AWAYON_5'] + ', ' + pbp_df['AWAYON_6']

    # extract the game type, which will determine the list of period values to loop through
    game_type = pbp_df['GAME_TYPE'][1]

    periods = []
    if game_type == 'Regulation':
        periods = [1,2,3]
    if game_type != 'Regulation':
        periods = [1,2,3,4]
   
    # trigger the csv files that will be written; write column titles to a header row 
    with open(stats_individual, 'w', newline = '') as players_individual, open(stats_onice, 'w', newline = '') as players_onice:
       
        individual_out = csv.writer(players_individual)
        individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'NO', 'PLAYER', 'POS', 'STATE', 'PERIOD', 'GP', 'TOI', 'G', 'xG', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S', 'FO', 'FOW', 'PD', 'PT', 'BK', 'GS'])
    
        onice_out = csv.writer(players_onice)
        onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'NO', 'PLAYER', 'POS', 'STATE', 'PERIOD', 'GP', 'TOI', 'GF', 'GA', 'xGF', 'xGA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'xGD', 'ONSD', 'USD', 'SD', 'FO', 'GS'])
    
        # access the game's roster file in order to create team-specific dicts for later use converting numbers to names 
        rosters_csv = files_root + 'rosters.csv'
    
        rosters_df = pd.read_csv(rosters_csv)
        
        rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]
    
        homeROS_df = rosters_table.copy()
        homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)].sort_values(by=['PLAYER_NO'])
        homeROS_list = homeROS_df['PLAYER_NAME'].tolist()
    
        awayROS_df = rosters_table.copy()
        awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)].sort_values(by=['PLAYER_NO'])
        awayROS_list = awayROS_df['PLAYER_NAME'].tolist() 
    
        # begin looping by team   
        for team in teams:

            if team == away:
                team_text = 'AWAY'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                teamON = team_text + 'ON'          
                team_players = awayROS_list
                
            elif team == home:
                team_text = 'HOME'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                teamON = team_text + 'ON'         
                team_players = homeROS_list
                       
            # add a loop for players
            for player in team_players:                               
 
                player_no = rosters_table.loc[(rosters_table['TEAM'] == team) & (rosters_table['PLAYER_NAME'] == player)]['PLAYER_NO'].item()
                player_pos = rosters_table.loc[(rosters_table['TEAM'] == team) & (rosters_table['PLAYER_NAME'] == player)]['PLAYER_POS'].item()
    
                # add a final loop for period
                for period in periods:

                    if period == 1:
                        period_name = '1st'
                    elif period == 2:
                        period_name = '2nd'
                    elif period == 3:
                        period_name = '3rd'
                    elif period == 4:
                        period_name = 'OT'

                    
                    ###
                    ### TIME ON ICE
                    ###

                    # duplicate the TOI dataframe for manipulation according to period status
                    TOI_df_start = TOI_df.copy()
                    
                    if period == 1:
                        TOI_period_df = TOI_df_start[(TOI_df_start['SECONDS_GONE'] < 1201)]
                    elif period == 2:
                        TOI_period_df = TOI_df_start[((TOI_df_start['SECONDS_GONE'] > 1200) & (TOI_df_start['SECONDS_GONE'] < 2401))]
                    elif period == 3:
                        TOI_period_df = TOI_df_start[((TOI_df_start['SECONDS_GONE'] > 2400) & (TOI_df_start['SECONDS_GONE'] < 3601))]
                    elif period == 4:
                        TOI_period_df = TOI_df_start[(TOI_df_start['SECONDS_GONE'] > 3600)]

                    # run a check to see verify the player actually played any, otherwise skipping if not                   
                    toi_all_first = TOI_df[(TOI_df[teamON].str.contains(player, na=False))].count()
                    toi_all = round(toi_all_first[1] * 0.0166667, 1)
        
                    if toi_all == 0:
                        continue

                    # generate counts of time on ice in different game states for the period being looped through     
                    toi_all_first = TOI_period_df[(TOI_period_df[teamON].str.contains(player, na=False))].count()
                    toi_all = round(toi_all_first[1] * 0.0166667, 1)                   
    
                    toi_5v5_first = TOI_period_df[(TOI_period_df[team_strength] == '5v5') & (TOI_period_df[teamON].str.contains(player))].count()
                    toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)

                    if int(game_id) < 30000 and period == 4:
                        toi_3v3_first = TOI_period_df[(TOI_period_df[team_strength] == '3v3') & (TOI_period_df[teamON].str.contains(player))].count()
                        toi_3v3 = round(toi_3v3_first[1] * 0.0166667, 1)
        
                    toi_PP_first = TOI_period_df[(TOI_period_df[team_state] == 'PP') & (TOI_period_df[teamON].str.contains(player))].count()
                    toi_PP = round(toi_PP_first[1] * 0.0166667, 1)
        
                    toi_SH_first = TOI_period_df[(TOI_period_df[team_state] == 'SH') & (TOI_period_df[teamON].str.contains(player))].count()
                    toi_SH = round(toi_SH_first[1] * 0.0166667, 1)
      
    
                    ###
                    ### PLAY-BY-PLAY
                    ###
     
                    # duplicate the play-by-play dataframe for manipulation according to period status
                    pbp_df_start = pbp_df.copy()  
                    if period < 4:
                        pbp_period_df = pbp_df_start[(pbp_df_start['PERIOD'] == period)]
                    if period == 4:
                        pbp_period_df = pbp_df_start[(pbp_df_start['PERIOD'] >= period)]
       
                    ##
                    ## INDIVIDUAL
                    ##
                    
                    #
                    # shot-based metrics
                    #
                    
                    # goals, assists and primary assists
                    event = 'Goal'
                    G_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    G_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        G_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    G_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    G_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                
                    try:
                        A1_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    except:
                        A1_all = 0
                    try:
                        A1_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    except:
                        A1_5v5 = 0
                    if int(game_id) < 30000 and period == 4:
                        try:
                            A1_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                        except:
                            A1_3v3 = 0                       
                    try:
                        A1_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    except:
                        A1_PP = 0
                    try:
                        A1_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    except:
                        A1_SH = 0
            
                    try:
                        A2_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_C'] == player)].count()[1]
                    except:
                        A2_all = 0
                    try:
                        A2_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_C'] == player)].count()[1]
                    except:
                        A2_5v5 = 0
                    if int(game_id) < 30000 and period == 4:
                        try:
                            A2_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_C'] == player)].count()[1]
                        except:
                            A2_3v3 = 0
                    try:
                        A2_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_C'] == player)].count()[1]
                    except:
                        A2_PP = 0
                    try:
                        A2_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_C'] == player)].count()[1]
                    except:
                        A2_SH = 0
                    
                    A_all = A1_all + A2_all
                    A_5v5 = A1_5v5 + A2_5v5
                    if int(game_id) < 30000 and period == 4:
                        A_3v3 = A1_3v3 + A2_3v3                      
                    A_PP = A1_PP + A2_PP
                    A_SH = A1_SH + A2_SH
        
                    # points and primary points
                    PTS_all = G_all + A_all
                    PTS_5v5 = G_5v5 + A_5v5
                    if int(game_id) < 30000 and period == 4:
                        PTS_3v3 = G_3v3 + A_3v3
                    PTS_PP = G_PP + A_PP
                    PTS_SH = G_SH + A_SH
            
                    PTS1_all = G_all + A1_all
                    PTS1_5v5 = G_5v5 + A1_5v5
                    if int(game_id) < 30000 and period == 4:
                        PTS1_3v3 = G_3v3 + A1_3v3
                    PTS1_PP = G_PP + A1_PP
                    PTS1_SH = G_SH + A1_SH
        
                    # on-net shots (shots that scored or were saved)
                    event = 'Save'
                    ONS_all = G_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    ONS_5v5 = G_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        ONS_3v3 = G_3v3 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    ONS_PP = G_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    ONS_SH = G_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                        
                    # unblocked shots (shots that scored, were saved or missed)
                    event = 'Miss'
                    US_all = ONS_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    US_5v5 = ONS_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        US_3v3 = ONS_3v3 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    US_PP = ONS_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    US_SH = ONS_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                        
                    # shots (shots that scored, were saved, missed or were blocked)
                    event = 'Shot'
                    S_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    S_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        S_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    S_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    S_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]

                    # expected goals
                    xG_all = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df['PLAYER_A'] == player), pbp_period_df['xG'], 0).sum(), 2)
                    xG_5v5 = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player), pbp_period_df['xG'], 0).sum(), 2)
                    if int(game_id) < 30000 and period == 4:
                        xG_3v3 = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player), pbp_period_df['xG'], 0).sum(), 2)
                    xG_PP = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player), pbp_period_df['xG'], 0).sum(), 2)
                    xG_SH = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player), pbp_period_df['xG'], 0).sum(), 2)
              
                    #
                    # non-shot or defending metrics
                    #

                    # faceoffs
                    event = 'Faceoff'
                    iFO_all = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    iFO_5v5 = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    if int(game_id) < 30000 and period == 4:
                        iFO_3v3 = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                    pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    iFO_PP = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    iFO_SH = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
    
                    iFOW_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    iFOW_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        iFOW_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    iFOW_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    iFOW_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
        
                    # penalties
                    event = 'Penalty'
                    PD_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    PD_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        PD_3v3 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    PD_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    PD_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
    
                    PT_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    PT_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        PT_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    PT_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    PT_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]

                    # shot blocks
                    event = 'Block'
                    SB_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    SB_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    if int(game_id) < 30000 and period == 4:
                        SB_3v3 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    SB_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    SB_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                          
            
                    ##
                    ## ON-ICE
                    ##
                    
                    #
                    # shot-based metrics
                    #
                    
                    # goals (shots that scored) for and against
                    event = 'Goal'
                    GF_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    GF_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]

                    if int(game_id) < 30000 and period == 4:
                        GF_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                        GA_3v3 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    GF_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    GF_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
                  
                    GD_all = GF_all - GA_all
                    GD_5v5 = GF_5v5 - GA_5v5
                    if int(game_id) < 30000 and period == 4:
                        GD_3v3 = GF_3v3 - GA_3v3
                    GD_PP = GF_PP - GA_PP        
                    GD_SH = GF_SH - GA_SH        
        
        
                    # on-net shots (shots that scored or were saved) for and against
                    event = 'Save'
                    ONSF_all = GF_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_all = GA_all + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    ONSF_5v5 = GF_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_5v5 = GA_5v5 + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]

                    if int(game_id) < 30000 and period == 4:
                        ONSF_3v3 = GF_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                        ONSA_3v3 = GA_5v5 + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    ONSF_PP = GF_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_PP = GA_PP + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    ONSF_SH = GF_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_SH = GA_SH + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
            
                    ONSD_all = ONSF_all - ONSA_all
                    ONSD_5v5 = ONSF_5v5 - ONSA_5v5
                    if int(game_id) < 30000 and period == 4:
                        ONSD_3v3 = ONSF_3v3 - ONSA_3v3
                    ONSD_PP = ONSF_PP - ONSA_PP        
                    ONSD_SH = ONSF_SH - ONSA_SH        
        
            
                    # unblocked shots (shots that scored, were saved or missed) for and against
                    event = 'Miss'
                    USF_all = ONSF_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_all = ONSA_all + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    USF_5v5 = ONSF_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_5v5 = ONSA_5v5 + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]

                    if int(game_id) < 30000 and period == 4:
                        USF_3v3 = ONSF_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                        USA_3v3 = ONSA_5v5 + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    USF_PP = ONSF_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_PP = ONSA_PP + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    USF_SH = ONSF_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_SH = ONSA_SH + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
                    
                    USD_all = USF_all - USA_all
                    USD_5v5 = USF_5v5 - USA_5v5
                    if int(game_id) < 30000 and period == 4:
                        USD_3v3 = USF_3v3 - USA_3v3
                    USD_PP = USF_PP - USA_PP        
                    USD_SH = USF_SH - USA_SH        
         
                    # shots (shots that scored, were saved, missed or were blocked) for and against
                    event = 'Shot'
                    SF_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    SF_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]

                    if int(game_id) < 30000 and period == 4:
                        SF_3v3 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                        SA_3v3 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    SF_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    SF_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
                   
                    SD_all = SF_all - SA_all
                    SD_5v5 = SF_5v5 - SA_5v5
                    if game_type != 'Regulation' and period == 4:
                        SD_3v3 = SF_3v3 - SA_3v3
                    SD_PP = SF_PP - SA_PP        
                    SD_SH = SF_SH - SA_SH        
        
                    # expected goals for and against
                    xGF_all = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)
                    xGA_all = round(np.where((pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == 'Shot') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)

                    xGF_5v5 = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)
                    xGA_5v5 = round(np.where((pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)

                    if int(game_id) < 30000 and period == 4:
                        xGF_3v3 = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)
                        xGA_3v3 = round(np.where((pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)

                    xGF_PP = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)
                    xGA_PP = round(np.where((pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)

                    xGF_SH = round(np.where((pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)
                    xGA_SH = round(np.where((pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == 'Shot')  & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['EVENT_TYPE'] != 'Block') & (pbp_period_df[teamON].str.contains(player)), pbp_period_df['xG'], 0).sum(), 2)
                   
                    xGD_all = xGF_all - xGA_all
                    xGD_5v5 = xGF_5v5 - xGA_5v5
                    if int(game_id) < 30000 and period == 4:
                        xGD_3v3 = xGF_3v3 - xGA_3v3
                    xGD_PP = xGF_PP - xGA_PP        
                    xGD_SH = xGF_SH - xGA_SH        

                    #
                    # non-shot or defending metrics
                    # 
                    
                    # faceoffs
                    event = 'Faceoff'
                    onFO_all = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    onFO_5v5 = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    if int(game_id) < 30000 and period == 4:
                        onFO_3v3 = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '3v3') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    onFO_PP = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    onFO_SH = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          

                    ##
                    ## FINAL PREPARATION
                    ##

                    # calculate the player's gamescore (metric formula: @domluszczyszyn)
                    if player_pos == 'F':
                        iGS_all = (G_all * 0.75) + (xG_all * 0.5) + (A1_all * 0.7)  + (A2_all * 0.55) + (ONS_all * 0.075) + (SB_all * 0.05) + ((PD_all * 0.15) - (PT_all * 0.15)) + ((iFOW_all * 0.01) - ((iFO_all - iFOW_all) * 0.01))
                        iGS_5v5 = (G_5v5 * 0.75) + (xG_5v5 * 0.5) + (A1_5v5 * 0.7)  + (A2_5v5 * 0.55) + (ONS_5v5 * 0.075) + (SB_5v5 * 0.05) + ((PD_5v5 * 0.15) - (PT_5v5 * 0.15)) + ((iFOW_5v5 * 0.01) - ((iFO_5v5 - iFOW_5v5) * 0.01))
                        if int(game_id) < 30000 and period == 4:
                            iGS_3v3 = (G_3v3 * 0.75) + (xG_3v3 * 0.5) + (A1_3v3 * 0.7)  + (A2_3v3 * 0.55) + (ONS_3v3 * 0.075) + (SB_3v3 * 0.05) + ((PD_3v3 * 0.15) - (PT_3v3 * 0.15)) + ((iFOW_3v3 * 0.01) - ((iFO_3v3 - iFOW_3v3) * 0.01))
                        iGS_PP = (G_PP * 0.75) + (xG_PP * 0.5) + (A1_PP * 0.7)  + (A2_PP * 0.55) + (ONS_PP * 0.075) + (SB_PP * 0.05) + ((PD_PP * 0.15) - (PT_PP * 0.15)) + ((iFOW_PP * 0.01) - ((iFO_PP - iFOW_PP) * 0.01))
                        iGS_SH = (G_SH * 0.75) + (xG_SH * 0.5) + (A1_SH * 0.7)  + (A2_SH * 0.55) + (ONS_SH * 0.075) + (SB_SH * 0.05) + ((PD_SH * 0.15) - (PT_SH * 0.15)) + ((iFOW_SH * 0.01) - ((iFO_SH - iFOW_SH) * 0.01))
    
                        onGS_all = ((GF_all * 0.625) - (GA_all * 0.4375)) + ((xGF_all * 0.625) - (xGA_all * 1.75))
                        onGS_5v5 = ((GF_5v5 * 0.625) - (GA_5v5 * 0.4375)) + ((xGF_5v5 * 0.625) - (xGA_5v5 * 1.75))
                        if int(game_id) < 30000 and period == 4:
                            onGS_3v3 = ((GF_3v3 * 0.625) - (GA_3v3 * 0.4375)) + ((xGF_3v3 * 0.625) - (xGA_3v3 * 1.75))
                        onGS_PP = ((GF_PP * 0.625) - (GA_PP * 0.4375)) + ((xGF_PP * 0.625) - (xGA_PP * 1.75))
                        onGS_SH = ((GF_SH * 0.625) - (GA_SH * 0.4375)) + ((xGF_SH * 0.625) - (xGA_SH * 1.75))
    
                    if player_pos == 'D':
                        iGS_all = (G_all * 0.75) + (xG_all * 0.5) + (A1_all * 0.7)  + (A2_all * 0.55) + (ONS_all * 0.075) + (SB_all * 0.05) + ((PD_all * 0.15) - (PT_all * 0.15)) + ((iFOW_all * 0.01) - ((iFO_all - iFOW_all) * 0.01))
                        iGS_5v5 = (G_5v5 * 0.75) + (xG_5v5 * 0.5) + (A1_5v5 * 0.7)  + (A2_5v5 * 0.55) + (ONS_5v5 * 0.075) + (SB_5v5 * 0.05) + ((PD_5v5 * 0.15) - (PT_5v5 * 0.15)) + ((iFOW_5v5 * 0.01) - ((iFO_5v5 - iFOW_5v5) * 0.01))
                        if int(game_id) < 30000 and period == 4:
                            iGS_3v3 = (G_3v3 * 0.75) + (xG_3v3 * 0.5) + (A1_3v3 * 0.7)  + (A2_3v3 * 0.55) + (ONS_3v3 * 0.075) + (SB_3v3 * 0.05) + ((PD_3v3 * 0.15) - (PT_3v3 * 0.15)) + ((iFOW_3v3 * 0.01) - ((iFO_3v3 - iFOW_3v3) * 0.01))
                        iGS_PP = (G_PP * 0.75) + (xG_PP * 0.5) + (A1_PP * 0.7)  + (A2_PP * 0.55) + (ONS_PP * 0.075) + (SB_PP * 0.05) + ((PD_PP * 0.15) - (PT_PP * 0.15)) + ((iFOW_PP * 0.01) - ((iFO_PP - iFOW_PP) * 0.01))
                        iGS_SH = (G_SH * 0.75) + (xG_SH * 0.5) + (A1_SH * 0.7)  + (A2_SH * 0.55) + (ONS_SH * 0.075) + (SB_SH * 0.05) + ((PD_SH * 0.15) - (PT_SH * 0.15)) + ((iFOW_SH * 0.01) - ((iFO_SH - iFOW_SH) * 0.01))
    
                        onGS_all = ((GF_all * 0.425) - (GA_all * 0.575)) + ((xGF_all * 1.7) - (xGA_all * 2.3))
                        onGS_5v5 = ((GF_5v5 * 0.425) - (GA_5v5 * 0.575)) + ((xGF_5v5 * 1.7) - (xGA_5v5 * 2.3))
                        if int(game_id) < 30000 and period == 4:
                            onGS_3v3 = ((GF_3v3 * 0.425) - (GA_3v3 * 0.575)) + ((xGF_3v3 * 1.7) - (xGA_3v3 * 2.3))
                        onGS_PP = ((GF_PP * 0.425) - (GA_PP * 0.575)) + ((xGF_PP * 1.7) - (xGA_PP * 2.3))
                        onGS_SH = ((GF_SH * 0.425) - (GA_SH * 0.575)) + ((xGF_SH * 1.7) - (xGA_SH * 2.3))
    
                    if player_pos == 'G':
                        iGS_all = (G_all * 0.75) + (xG_all * 0.5) + (A1_all * 0.7)  + (A2_all * 0.55) + (ONS_all * 0.075) + (SB_all * 0.05) + ((PD_all * 0.15) - (PT_all * 0.15))
                        iGS_5v5 = (G_5v5 * 0.75) + (xG_5v5 * 0.5) + (A1_5v5 * 0.7)  + (A2_5v5 * 0.55) + (ONS_5v5 * 0.075) + (SB_5v5 * 0.05) + ((PD_5v5 * 0.15) - (PT_5v5 * 0.15))
                        if int(game_id) < 30000 and period == 4:
                            iGS_3v3 = (G_3v3 * 0.75) + (xG_3v3 * 0.5) + (A1_3v3 * 0.7)  + (A2_3v3 * 0.55) + (ONS_3v3 * 0.075) + (SB_3v3 * 0.05) + ((PD_3v3 * 0.15) - (PT_3v3 * 0.15))
                        iGS_PP = (G_PP * 0.75) + (xG_PP * 0.5) + (A1_PP * 0.7)  + (A2_PP * 0.55) + (ONS_PP * 0.075) + (SB_PP * 0.05) + ((PD_PP * 0.15) - (PT_PP * 0.15))
                        iGS_SH = (G_all * 0.75) + (xG_SH * 0.5) + (A1_SH * 0.7)  + (A2_SH * 0.55) + (ONS_SH * 0.075) + (SB_SH * 0.05) + ((PD_SH * 0.15) - (PT_SH * 0.15))
    
                        onGS_all = ((GA_all * -1) + xGA_all) + ((ONSA_all - GA_all) * 0.01)
                        onGS_5v5 = ((GA_5v5 * -1) + xGA_5v5) + ((ONSA_5v5 - GA_5v5) * 0.01)
                        if int(game_id) < 30000 and period == 4:
                            onGS_3v3 = ((GA_3v3 * -1) + xGA_3v3) + ((ONSA_3v3 - GA_3v3) * 0.01)
                        onGS_PP = ((GA_PP * -1) + xGA_PP) + ((ONSA_PP - GA_PP) * 0.01)
                        onGS_SH = ((GA_SH * -1) + xGA_SH) + ((ONSA_SH - GA_SH) * 0.01)

                    # arrange individual player data to record              
                    individual_all = (G_all, xG_all, A_all, A1_all, PTS_all, PTS1_all, ONS_all, US_all, S_all, iFO_all, iFOW_all, PD_all, PT_all, SB_all, iGS_all)
                    individual_5v5 = (G_5v5, xG_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5, iFO_5v5, iFOW_5v5, PD_5v5, PT_5v5, SB_5v5, iGS_5v5)
                    if int(game_id) < 30000 and period == 4:
                        individual_3v3 = (G_3v3, xG_3v3, A_3v3, A1_3v3, PTS_3v3, PTS1_3v3, ONS_3v3, US_3v3, S_3v3, iFO_3v3, iFOW_3v3, PD_3v3, PT_3v3, SB_3v3, iGS_3v3)
                    individual_PP = (G_PP, xG_PP, A_PP, A1_PP, PTS_PP, PTS1_PP, ONS_PP, US_PP, S_PP, iFO_PP, iFOW_PP, PD_PP, PT_PP, SB_PP, iGS_PP)
                    individual_SH = (G_SH, xG_SH, A_SH, A1_SH, PTS_SH, PTS1_SH, ONS_SH, US_SH, S_SH, iFO_SH, iFOW_SH, PD_SH, PT_SH, SB_SH, iGS_SH) 

                    # arrange on-ice player data to record
                    onice_all = (GF_all, GA_all, xGF_all, xGA_all, ONSF_all, ONSA_all, USF_all, USA_all, SF_all, SA_all, GD_all, xGD_all, ONSD_all, USD_all, SD_all, onFO_all, onGS_all)
                    onice_5v5 = (GF_5v5, GA_5v5, xGF_5v5, xGA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, xGD_5v5, ONSD_5v5, USD_5v5, SD_5v5, onFO_5v5, onGS_5v5)
                    if int(game_id) < 30000 and period == 4:
                        onice_3v3 = (GF_3v3, GA_3v3, xGF_3v3, xGA_3v3, ONSF_3v3, ONSA_3v3, USF_3v3, USA_3v3, SF_3v3, SA_3v3, GD_3v3, xGD_3v3, ONSD_3v3, USD_3v3, SD_3v3, onFO_3v3, onGS_3v3)
                    onice_PP = (GF_PP, GA_PP, xGF_PP, xGA_PP, ONSF_PP, ONSA_PP, USF_PP, USA_PP, SF_PP, SA_PP, GD_PP, xGD_PP, ONSD_PP, USD_PP, SD_PP, onFO_PP, onGS_PP)
                    onice_SH = (GF_SH, GA_SH, xGF_SH, xGA_SH, ONSF_SH, ONSA_SH, USF_SH, USA_SH, SF_SH, SA_SH, GD_SH, xGD_SH, ONSD_SH, USD_SH, SD_SH, onFO_SH, onGS_SH)


                    ###
                    ### WRITE TO FILE
                    ### 
                    
                    if team == away:
                        team_text = 'Away'
                    elif team == home:
                        team_text = 'Home'                    
    
                    # write out individual player data by period
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'ALL', period_name, '1', toi_all) + individual_all)
                    if period < 4 or int(game_id) > 30000 and period == 4:
                        individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '5v5', period_name, '1', toi_5v5) + individual_5v5)
                    if int(game_id) < 30000 and period == 4:
                        individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '3v3', period_name, '1', toi_3v3) + individual_3v3)
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'PP', period_name, '1', toi_PP) + individual_PP)
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'SH', period_name, '1', toi_SH) + individual_SH)
                    
                    # status update
                    print('Processing ' + team + ' individual ' + period_name + ' period player stats for ' + player)                      
                    
                    # write out on-ice player data by period
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'ALL', period_name, '1', toi_all) + onice_all)
                    if period < 4 or int(game_id) > 30000 and period == 4:
                        onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '5v5', period_name, '1', toi_5v5) + onice_5v5)
                    if int(game_id) < 30000 and period == 4:
                        onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '3v3', period_name, '1', toi_3v3) + onice_3v3)                        
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'PP', period_name, '1', toi_PP) + onice_PP)
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'SH', period_name, '1', toi_SH) + onice_SH)
                    
                    # status update
                    print('Processing ' + team + ' on-ice ' + period_name + ' period player stats for ' + player)
      
    # status update
    print('Finished generating period player stats for ' + season_id + ' ' + game_id)