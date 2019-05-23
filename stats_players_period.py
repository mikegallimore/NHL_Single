# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import csv
import pandas as pd
import parameters

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
    teams = [away, home]

    ### establish file locations and destinations
    TOI_matrix = files_root + 'TOI_matrix.csv'
    pbp = files_root + 'pbp.csv'
    stats_individual = files_root + 'stats_players_individual_period.csv'
    stats_onice = files_root + 'stats_players_onice_period.csv'
    
    ### create a list of period values to loop through
    periods = [1,2,3,4]
    
    ### create a dataframe for extracting TOI info; add a column with all of the on-ice players for expedited searching; derive the last on-ice second recorded
    TOI_df = pd.read_csv(TOI_matrix)
    
    TOI_df['HOMEON_5'].fillna('NaN', inplace = True)
    TOI_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    TOI_df['AWAYON_5'].fillna('NaN', inplace = True)
    TOI_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    TOI_df['HOMEON'] = TOI_df['HOMEON_1'] + ', ' + TOI_df['HOMEON_2'] + ', ' + TOI_df['HOMEON_3'] + ', ' + TOI_df['HOMEON_4'] + ', ' + TOI_df['HOMEON_5'] + ', ' + TOI_df['HOMEON_6']
    TOI_df['AWAYON'] = TOI_df['AWAYON_1'] + ', ' + TOI_df['AWAYON_2'] + ', ' + TOI_df['AWAYON_3'] + ', ' + TOI_df['AWAYON_4'] + ', ' + TOI_df['AWAYON_5'] + ', ' + TOI_df['AWAYON_6']
    
    toi_max = TOI_df['SECONDS_GONE'].max()
    
    ### create a dataframe for extracting play-by-play info; add a column with all of the on-ice players for expedited searching
    pbp_df = pd.read_csv(pbp)
    pbp_df = pbp_df[(pbp_df['PERIOD'] != 5)]
    
    pbp_df['HOMEON_5'].fillna('NaN', inplace = True)
    pbp_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    pbp_df['AWAYON_5'].fillna('NaN', inplace = True)
    pbp_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    pbp_df['HOMEON'] = pbp_df['HOMEON_1'] + ', ' + pbp_df['HOMEON_2'] + ', ' + pbp_df['HOMEON_3'] + ', ' + pbp_df['HOMEON_4'] + ', ' + pbp_df['HOMEON_5'] + ', ' + pbp_df['HOMEON_6']
    pbp_df['AWAYON'] = pbp_df['AWAYON_1'] + ', ' + pbp_df['AWAYON_2'] + ', ' + pbp_df['AWAYON_3'] + ', ' + pbp_df['AWAYON_4'] + ', ' + pbp_df['AWAYON_5'] + ', ' + pbp_df['AWAYON_6']
    
    ### trigger the csv files that will be written; write column titles to a header row 
    with open(stats_individual, 'w', newline = '') as players_individual, open(stats_onice, 'w', newline = '') as players_onice:
       
        individual_out = csv.writer(players_individual)
        individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'NO', 'PLAYER', 'POS', 'STATE', 'PERIOD', 'GP', 'TOI', 'G', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S', 'FO', 'FOW', 'PD', 'PT', 'BK'])
    
        onice_out = csv.writer(players_onice)
        onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'NO', 'PLAYER', 'POS', 'STATE', 'PERIOD', 'GP', 'TOI', 'GF', 'GA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'ONSD', 'USD', 'SD', 'FO'])
    
        ### access the game's roster file in order to create team-specific dicts for later use converting numbers to names 
        rosters_csv = files_root + 'rosters.csv'
    
        rosters_df = pd.read_csv(rosters_csv)
        
        rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]
    
        homeROS_df = rosters_table.copy()
        homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)].sort_values(by=['PLAYER_NO'])
        homeROS_list = homeROS_df['PLAYER_NAME'].tolist()
    
        awayROS_df = rosters_table.copy()
        awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)].sort_values(by=['PLAYER_NO'])
        awayROS_list = awayROS_df['PLAYER_NAME'].tolist() 
    
        ### begin looping by period   
        for period in periods:
                   
            if period == 1:
                period_name = '1st'
            elif period == 2:
                period_name = '2nd'
            elif period == 3:
                period_name = '3rd'
            elif period == 4:
                period_name = 'OT'
    
            ### duplicate the TOI dataframe for manipulation according to period status
            TOI_df_start = TOI_df.copy()
            
            if period == 1:
                TOI_period_df = TOI_df_start[(TOI_df_start['SECONDS_GONE'] < 1201)]
            elif period == 2:
                TOI_period_df = TOI_df_start[((TOI_df_start['SECONDS_GONE'] > 1200) & (TOI_df_start['SECONDS_GONE'] < 2401))]
            elif period == 3:
                TOI_period_df = TOI_df_start[((TOI_df_start['SECONDS_GONE'] > 2400) & (TOI_df_start['SECONDS_GONE'] < 3601))]
            elif period == 4:
                TOI_period_df = TOI_df_start[(TOI_df_start['SECONDS_GONE'] > 3600)]
    
            ### add a loop for teams
            for team in teams:
    
                if team == away:
                    team_text = 'AWAY'
                    team_state = team_text + '_STATE'
                    team_strength = team_text + '_STRENGTH'
                    team_zone = team_text + '_ZONE'
                    teamON = team_text + 'ON'          
                    team_players = awayROS_list
                    
                elif team == home:
                    team_text = 'HOME'
                    team_state = team_text + '_STATE'
                    team_strength = team_text + '_STRENGTH'
                    team_zone = team_text + '_ZONE'
                    teamON = team_text + 'ON'         
                    team_players = homeROS_list
    
                ### add a final loop for players
                for player in team_players:                               
           
                    player_no = rosters_table.loc[(rosters_table['TEAM'] == team) & (rosters_table['PLAYER_NAME'] == player)]['PLAYER_NO'].item()
                    player_pos = rosters_table.loc[(rosters_table['TEAM'] == team) & (rosters_table['PLAYER_NAME'] == player)]['PLAYER_POS'].item()
                    
                    ###
                    ### TIME ON ICE
                    ###
                    
                    toi_all_first = TOI_df[(TOI_df[teamON].str.contains(player))].count()
                    toi_all = round(toi_all_first[1] * 0.0166667, 1)
        
                    if toi_all == 0:
                        continue
    
                    toi_all_first = TOI_period_df[(TOI_period_df[teamON].str.contains(player))].count()
                    toi_all = round(toi_all_first[1] * 0.0166667, 1)                   
    
                    toi_5v5_first = TOI_period_df[(TOI_period_df[team_strength] == '5v5') & (TOI_period_df[teamON].str.contains(player))].count()
                    toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)
        
                    toi_PP_first = TOI_period_df[(TOI_period_df[team_state] == 'PP') & (TOI_period_df[teamON].str.contains(player))].count()
                    toi_PP = round(toi_PP_first[1] * 0.0166667, 1)
        
                    toi_SH_first = TOI_period_df[(TOI_period_df[team_state] == 'SH') & (TOI_period_df[teamON].str.contains(player))].count()
                    toi_SH = round(toi_SH_first[1] * 0.0166667, 1)
      
    
                    ###
                    ### PLAY-BY-PLAY
                    ###
     
                    ### duplicate the play-by-play dataframe for manipulation according to period status
                    pbp_df_start = pbp_df.copy()
                    
                    pbp_period_df = pbp_df_start[(pbp_df_start['PERIOD'] == period)]
       
                    ###
                    ### INDIVIDUAL
                    ###
                    
                    ### goals, assists and primary assists
                    event = 'Goal'
                    G_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    G_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
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
                    A_PP = A1_PP + A2_PP
                    A_SH = A1_SH + A2_SH
        
        
                    ### points and primary points
                    PTS_all = G_all + A_all
                    PTS_5v5 = G_5v5 + A_5v5
                    PTS_PP = G_PP + A_PP
                    PTS_SH = G_SH + A_SH
            
                    PTS1_all = G_all + A1_all
                    PTS1_5v5 = G_5v5 + A1_5v5
                    PTS1_PP = G_PP + A1_PP
                    PTS1_SH = G_SH + A1_SH
        
          
                    ### on-net (saved) shots
                    event = 'Save'
                    ONS_all = G_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    ONS_5v5 = G_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    ONS_PP = G_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    ONS_SH = G_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
            
            
                    ### unblocked shots
                    event = 'Miss'
                    US_all = ONS_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    US_5v5 = ONS_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    US_PP = ONS_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    US_SH = ONS_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
            
            
                    ### shots
                    event = 'Shot'
                    S_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    S_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    S_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    S_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
              

                    ### faceoffs
                    event = 'Faceoff'
                    FO_all = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    FO_5v5 = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    FO_PP = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
                    FO_SH = (pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1] +
                                pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1])
    
                    FOW_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    FOW_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    FOW_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    FOW_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
    
    
                    ### penalties
                    event = 'Penalty'
                    PD_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    PD_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    PD_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    PD_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
    
                    PT_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    PT_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    PT_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_A'] == player)].count()[1]
                    PT_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_A'] == player)].count()[1]


                    ### shot blocks
                    event = 'Block'
                    SB_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    SB_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    SB_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
                    SB_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df['PLAYER_B'] == player)].count()[1]
               
                
                    individual_all = (G_all, A_all, A1_all, PTS_all, PTS1_all, ONS_all, US_all, S_all, FO_all, FOW_all, PD_all, PT_all, SB_all)
                    individual_5v5 = (G_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5, FO_5v5, FOW_5v5, PD_5v5, PT_5v5, SB_5v5)
                    individual_PP = (G_PP, A_PP, A1_PP, PTS_PP, PTS1_PP, ONS_PP, US_PP, S_PP, FO_PP, FOW_PP, PD_PP, PT_PP, SB_PP)
                    individual_SH = (G_SH, A_SH, A1_SH, PTS_SH, PTS1_SH, ONS_SH, US_SH, S_SH, FO_SH, FOW_SH, PD_SH, PT_SH, SB_SH) 
            
            
                    ###
                    ### ON-ICE
                    ###
              
                    ### goals for and against
                    event = 'Goal'
                    GF_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    GF_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    GF_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    GF_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    GA_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
                  
                    GD_all = GF_all - GA_all
                    GD_5v5 = GF_5v5 - GA_5v5
                    GD_PP = GF_PP - GA_PP        
                    GD_SH = GF_SH - GA_SH        
        
        
                    ### on-net (saved) shots for and against
                    event = 'Save'
                    ONSF_all = GF_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_all = GA_all + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    ONSF_5v5 = GF_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_5v5 = GA_5v5 + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    ONSF_PP = GF_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_PP = GA_PP + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    ONSF_SH = GF_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    ONSA_SH = GA_SH + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
            
                    ONSD_all = ONSF_all - ONSA_all
                    ONSD_5v5 = ONSF_5v5 - ONSA_5v5
                    ONSD_PP = ONSF_PP - ONSA_PP        
                    ONSD_SH = ONSF_SH - ONSA_SH        
        
            
                    ### unblocked shots for and against
                    event = 'Miss'
                    USF_all = ONSF_all + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_all = ONSA_all + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    USF_5v5 = ONSF_5v5 + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_5v5 = ONSA_5v5 + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    USF_PP = ONSF_PP + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_PP = ONSA_PP + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    USF_SH = ONSF_SH + pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    USA_SH = ONSA_SH + pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT_TYPE'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
                    
                    USD_all = USF_all - USA_all
                    USD_5v5 = USF_5v5 - USA_5v5
                    USD_PP = USF_PP - USA_PP        
                    USD_SH = USF_SH - USA_SH        
         
            
                    ### shots for and against
                    event = 'Shot'
                    SF_all = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_all = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    SF_5v5 = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_5v5 = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    SF_PP = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_PP = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]
        
                    SF_SH = pbp_period_df[(pbp_period_df['TEAM'] == team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
                    SA_SH = pbp_period_df[(pbp_period_df['TEAM'] != team) & (pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]
                   
                    SD_all = SF_all - SA_all
                    SD_5v5 = SF_5v5 - SA_5v5
                    SD_PP = SF_PP - SA_PP        
                    SD_SH = SF_SH - SA_SH        
        
        
                    ### faceoffs
                    event = 'Faceoff'
                    FO_all = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[teamON].str.contains(player))].count()[1]          
        
                    FO_5v5 = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_strength] == '5v5') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
        
                    FO_PP = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'PP') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
        
                    FO_SH = pbp_period_df[(pbp_period_df['EVENT'] == event) & (pbp_period_df[team_state] == 'SH') & (pbp_period_df[teamON].str.contains(player))].count()[1]          
    
    
                    onice_all = (GF_all, GA_all, ONSF_all, ONSA_all, USF_all, USA_all, SF_all, SA_all, GD_all, ONSD_all, USD_all, SD_all, FO_all)
                    onice_5v5 = (GF_5v5, GA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, ONSD_5v5, USD_5v5, SD_5v5, FO_5v5)
                    onice_PP = (GF_PP, GA_PP, ONSF_PP, ONSA_PP, USF_PP, USA_PP, SF_PP, SA_PP, GD_PP, ONSD_PP, USD_PP, SD_PP, FO_PP)
                    onice_SH = (GF_SH, GA_SH, ONSF_SH, ONSA_SH, USF_SH, USA_SH, SF_SH, SA_SH, GD_SH, ONSD_SH, USD_SH, SD_SH, FO_SH)
                                                 
                    
                    ### begin writing to file
                    if team == away:
                        team_text = 'Away'
                    elif team == home:
                        team_text = 'Home'                    
    
                    ### write out individual player data by period
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'ALL', period_name, '1', toi_all) + individual_all)
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '5v5', period_name, '1', toi_5v5) + individual_5v5)
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'PP', period_name, '1', toi_PP) + individual_PP)
                    individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'SH', period_name, '1', toi_SH) + individual_SH)
                    
                    print('Processing ' + team + ' individual ' + period_name + ' period player stats for ' + player)                      
                    
                    ### write out on-ice player data by period
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'ALL', period_name, '1', toi_all) + onice_all)
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '5v5', period_name, '1', toi_5v5) + onice_5v5)
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'PP', period_name, '1', toi_PP) + onice_PP)
                    onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'SH', period_name, '1', toi_SH) + onice_SH)
                    
                    print('Processing ' + team + ' on-ice ' + period_name + ' period player stats for ' + player)
      
    
    print('Finished generating period player stats for ' + season_id + ' ' + game_id)