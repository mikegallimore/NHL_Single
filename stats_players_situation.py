# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 00:10:44 2017

@author: @mikegallimore
"""

import csv
import pandas as pd
import parameters

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
files_root = parameters.files_root

### establish file locations and destinations
TOI_matrix = files_root + 'TOI_matrix.csv'
pbp = files_root + 'pbp.csv'
stats_individual = files_root + 'stats_players_individual_situation.csv'
stats_onice = files_root + 'stats_players_onice_situation.csv'

### pull schedule info; generate key values
schedule_csv = files_root + season_id + "_schedule.csv"

schedule_df = pd.read_csv(schedule_csv)
schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]

date = schedule_date['DATE'].item()
home = schedule_date['HOME'].item()
away = schedule_date['AWAY'].item()
teams = [away, home]

### create a list of game situations
situations = ['Leading','Tied','Trailing'] 

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
    individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'NO', 'PLAYER', 'POS', 'STATE', 'PERIOD', 'GP', 'TOI', 'G', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S'])

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
    
    ### begin looping by game situation   
    for situation in situations:
               
        ### duplicate the TOI dataframe for manipulation according to game situation
        TOI_df_start = TOI_df.copy()
        
        if situation == 'Leading':
            TOI_df_home = TOI_df_start[(TOI_df_start['HOME_SITUATION'] == 'LEADING')]
            TOI_df_away = TOI_df_start[(TOI_df_start['AWAY_SITUATION'] == 'LEADING')]
        elif situation == 'Tied':
            TOI_df_home = TOI_df_start[(TOI_df_start['HOME_SITUATION'] == 'TIED')]
            TOI_df_away = TOI_df_start[(TOI_df_start['AWAY_SITUATION'] == 'TIED')]
        elif situation == 'Trailing':
            TOI_df_home = TOI_df_start[(TOI_df_start['HOME_SITUATION'] == 'TRAILING')]
            TOI_df_away = TOI_df_start[(TOI_df_start['AWAY_SITUATION'] == 'TRAILING')] 

        ### add a loop for teams
        for team in teams:         
   
            if team == away:
                team_text = 'AWAY'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'          
                team_players = awayROS_list
                TOI_situation_df = TOI_df_away               
                
            elif team == home:
                team_text = 'HOME'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'         
                team_players = homeROS_list
                TOI_situation_df = TOI_df_home

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

                toi_all_first = TOI_situation_df[(TOI_situation_df[teamON].str.contains(player))].count()
                toi_all = round(toi_all_first[1] * 0.0166667, 1)                   

                toi_5v5_first = TOI_situation_df[(TOI_situation_df[team_strength] == '5v5') & (TOI_situation_df[teamON].str.contains(player))].count()
                toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)
    
                toi_PP_first = TOI_situation_df[(TOI_situation_df[team_state] == 'PP') & (TOI_situation_df[teamON].str.contains(player))].count()
                toi_PP = round(toi_PP_first[1] * 0.0166667, 1)
    
                toi_SH_first = TOI_situation_df[(TOI_situation_df[team_state] == 'SH') & (TOI_situation_df[teamON].str.contains(player))].count()
                toi_SH = round(toi_SH_first[1] * 0.0166667, 1)

                
                ###
                ### PLAY-BY-PLAY
                ###

                ### duplicate the play-by-play dataframe for manipulation according to game situation
                pbp_df_start = pbp_df.copy()
                
                pbp_df_home = pbp_df_start[(pbp_df_start['HOME_SITUATION'] == situation)]
                pbp_df_away = pbp_df_start[(pbp_df_start['AWAY_SITUATION'] == situation)]

                if team == away:
                    pbp_situation_df = pbp_df_away
                elif team == home:
                    pbp_situation_df = pbp_df_home

                ###
                ### INDIVIDUAL
                ###
                
                ### goals, assists and primary assists
                event = 'Goal'
                G_all = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                G_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                G_PP = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                G_SH = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
    
    
                try:
                    A1_all = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df['PLAYER_B'] == player)].count()[1]
                except:
                    A1_all = 0
                try:
                    A1_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df['PLAYER_B'] == player)].count()[1]
                except:
                    A1_5v5 = 0
                try:
                    A1_PP = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df['PLAYER_B'] == player)].count()[1]
                except:
                    A1_PP = 0
                try:
                    A1_SH = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df['PLAYER_B'] == player)].count()[1]
                except:
                    A1_SH = 0
        
                try:
                    A2_all = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df['PLAYER_C'] == player)].count()[1]
                except:
                    A2_all = 0
                try:
                    A2_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df['PLAYER_C'] == player)].count()[1]
                except:
                    A2_5v5 = 0
                try:
                    A2_PP = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df['PLAYER_C'] == player)].count()[1]
                except:
                    A2_PP = 0
                try:
                    A2_SH = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df['PLAYER_C'] == player)].count()[1]
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
                ONS_all = G_all + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                ONS_5v5 = G_5v5 + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                ONS_PP = G_PP + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                ONS_SH = G_SH + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
        
        
                ### unblocked shots
                event = 'Miss'
                US_all = ONS_all + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                US_5v5 = ONS_5v5 + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                US_PP = ONS_PP + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                US_SH = ONS_SH + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
        
        
                ### shots
                event = 'Shot'
                S_all = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                S_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                S_PP = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
                S_SH = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df['PLAYER_A'] == player)].count()[1]
          
            
                individual_all = (G_all, A_all, A1_all, PTS_all, PTS1_all, ONS_all, US_all, S_all)
                individual_5v5 = (G_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5)
                individual_PP = (G_PP, A_PP, A1_PP, PTS_PP, PTS1_PP, ONS_PP, US_PP, S_PP)
                individual_SH = (G_SH, A_SH, A1_SH, PTS_SH, PTS1_SH, ONS_SH, US_SH, S_SH)  
        
        
                ###
                ### ON-ICE
                ###
          
                ### goals for and against
                event = 'Goal'
                GF_all = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                GA_all = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                GF_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                GA_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                GF_PP = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                GA_PP = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                GF_SH = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                GA_SH = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
              
                GD_all = GF_all - GA_all
                GD_5v5 = GF_5v5 - GA_5v5
                GD_PP = GF_PP - GA_PP        
                GD_SH = GF_SH - GA_SH        
    
    
                ### on-net (saved) shots for and against
                event = 'Save'
                ONSF_all = GF_all + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                ONSA_all = GA_all + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                ONSF_5v5 = GF_5v5 + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                ONSA_5v5 = GA_5v5 + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                ONSF_PP = GF_PP + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                ONSA_PP = GA_PP + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                ONSF_SH = GF_SH + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                ONSA_SH = GA_SH + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
        
                ONSD_all = ONSF_all - ONSA_all
                ONSD_5v5 = ONSF_5v5 - ONSA_5v5
                ONSD_PP = ONSF_PP - ONSA_PP        
                ONSD_SH = ONSF_SH - ONSA_SH        
    
        
                ### unblocked shots for and against
                event = 'Miss'
                USF_all = ONSF_all + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                USA_all = ONSA_all + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                USF_5v5 = ONSF_5v5 + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                USA_5v5 = ONSA_5v5 + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                USF_PP = ONSF_PP + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                USA_PP = ONSA_PP + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                USF_SH = ONSF_SH + pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                USA_SH = ONSA_SH + pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT_TYPE'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
                
                USD_all = USF_all - USA_all
                USD_5v5 = USF_5v5 - USA_5v5
                USD_PP = USF_PP - USA_PP        
                USD_SH = USF_SH - USA_SH        
     
        
                ### shots for and against
                event = 'Shot'
                SF_all = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                SA_all = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                SF_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                SA_5v5 = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                SF_PP = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                SA_PP = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
    
                SF_SH = pbp_situation_df[(pbp_situation_df['TEAM'] == team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
                SA_SH = pbp_situation_df[(pbp_situation_df['TEAM'] != team) & (pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]
               
                SD_all = SF_all - SA_all
                SD_5v5 = SF_5v5 - SA_5v5
                SD_PP = SF_PP - SA_PP        
                SD_SH = SF_SH - SA_SH        
    
    
                ### faceoffs
                event = 'Faceoff'
                FO_all = pbp_situation_df[(pbp_situation_df['EVENT'] == event) & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
    
                FO_5v5 = pbp_situation_df[(pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_strength] == '5v5') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
    
                FO_PP = pbp_situation_df[(pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'PP') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          
    
                FO_SH = pbp_situation_df[(pbp_situation_df['EVENT'] == event) & (pbp_situation_df[team_state] == 'SH') & (pbp_situation_df[teamON].str.contains(player))].count()[1]          


                onice_all = (GF_all, GA_all, ONSF_all, ONSA_all, USF_all, USA_all, SF_all, SA_all, GD_all, ONSD_all, USD_all, SD_all, FO_all)
                onice_5v5 = (GF_5v5, GA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, ONSD_5v5, USD_5v5, SD_5v5, FO_5v5)
                onice_PP = (GF_PP, GA_PP, ONSF_PP, ONSA_PP, USF_PP, USA_PP, SF_PP, SA_PP, GD_PP, ONSD_PP, USD_PP, SD_PP, FO_PP)
                onice_SH = (GF_SH, GA_SH, ONSF_SH, ONSA_SH, USF_SH, USA_SH, SF_SH, SA_SH, GD_SH, ONSD_SH, USD_SH, SD_SH, FO_SH)
                                             
                
                ### begin writing to file
                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'                    

                ### write out individual player data by game situation
                individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'ALL', situation, '1', toi_all) + individual_all)
                individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '5v5', situation, '1', toi_5v5) + individual_5v5)
                individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'PP', situation, '1', toi_PP) + individual_PP)
                individual_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'SH', situation, '1', toi_SH) + individual_SH)
                
                print('Processing ' + team + ' individual ' + situation + ' player stats for ' + player)                      
                
                ### write out on-ice player data by game situation
                onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'ALL', situation, '1', toi_all) + onice_all)
                onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, '5v5', situation, '1', toi_5v5) + onice_5v5)
                onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'PP', situation, '1', toi_PP) + onice_PP)
                onice_out.writerow((season_id, game_id, date, team_text, team, player_no, player, player_pos, 'SH', situation, '1', toi_SH) + onice_SH)
                
                print('Processing ' + team + ' on-ice ' + situation + ' player stats for ' + player)


print('Finished generating situation player stats for ' + season_id + ' ' + game_id)