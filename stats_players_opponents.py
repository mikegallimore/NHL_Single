# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import csv
import pandas as pd
import numpy as np
import itertools as it
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
    stats_individual = files_root + 'stats_players_individual_opponents.csv'
    stats_onice = files_root + 'stats_players_onice_opponents.csv'
    
    # create a dataframe for extracting TOI info; add a column with all of the on-ice players for expedited searching; derive the last on-ice second recorded
    TOI_df = pd.read_csv(TOI_matrix)
    
    TOI_df['HOMEON_5'].fillna('NaN', inplace = True)
    TOI_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    TOI_df['AWAYON_5'].fillna('NaN', inplace = True)
    TOI_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    TOI_df['HOMEON'] = TOI_df['HOMEON_1'] + ', ' + TOI_df['HOMEON_2'] + ', ' + TOI_df['HOMEON_3'] + ', ' + TOI_df['HOMEON_4'] + ', ' + TOI_df['HOMEON_5'] + ', ' + TOI_df['HOMEON_6']
    TOI_df['AWAYON'] = TOI_df['AWAYON_1'] + ', ' + TOI_df['AWAYON_2'] + ', ' + TOI_df['AWAYON_3'] + ', ' + TOI_df['AWAYON_4'] + ', ' + TOI_df['AWAYON_5'] + ', ' + TOI_df['AWAYON_6']
   
    # create a dataframe for extracting play-by-play info; add a column with all of the on-ice players for expedited searching
    pbp_df_start = pd.read_csv(pbp)
    pbp_df_start = pbp_df_start[(pbp_df_start['PERIOD'] != 5)]
      
    pbp_df_start['HOMEON_5'].fillna('NaN', inplace = True)
    pbp_df_start['HOMEON_6'].fillna('NaN', inplace = True)
    
    pbp_df_start['AWAYON_5'].fillna('NaN', inplace = True)
    pbp_df_start['AWAYON_6'].fillna('NaN', inplace = True)
    
    pbp_df_start['HOMEON'] = pbp_df_start['HOMEON_1'] + ', ' + pbp_df_start['HOMEON_2'] + ', ' + pbp_df_start['HOMEON_3'] + ', ' + pbp_df_start['HOMEON_4'] + ', ' + pbp_df_start['HOMEON_5'] + ', ' + pbp_df_start['HOMEON_6']
    pbp_df_start['AWAYON'] = pbp_df_start['AWAYON_1'] + ', ' + pbp_df_start['AWAYON_2'] + ', ' + pbp_df_start['AWAYON_3'] + ', ' + pbp_df_start['AWAYON_4'] + ', ' + pbp_df_start['AWAYON_5'] + ', ' + pbp_df_start['AWAYON_6']
    
    # trigger the csv files that will be written; write column titles to a header row 
    with open(stats_individual, 'w', newline = '') as players_individual, open(stats_onice, 'w', newline = '') as players_onice:
    
        individual_out = csv.writer(players_individual)
        individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER', 'OPPONENT', 'STATE', 'GP', 'TOI', 'G', 'xG', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S', 'FO', 'FOW', 'PD', 'PT', 'BK'])
    
        onice_out = csv.writer(players_onice)
        onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER', 'OPPONENT', 'STATE', 'GP', 'TOI', 'GF', 'GA', 'xGF', 'xGA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'xGD', 'ONSD', 'USD', 'SD', 'FO'])
    
        # access the game's roster file in order to create team-specific dicts and lists
        rosters_csv = files_root + 'rosters.csv'
        rosters_df = pd.read_csv(rosters_csv)
        rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS', 'PLAYER_POS_DETAIL']]
    
        awayROS = rosters_table.copy()   
        awayROS = awayROS[(awayROS['TEAM'] == away)].sort_values(by=['PLAYER_NO'])
        awayROS_list = awayROS['PLAYER_NAME'].tolist()
    
        homeROS = rosters_table.copy()   
        homeROS = homeROS[(homeROS['TEAM'] == home)].sort_values(by=['PLAYER_NO'])
        homeROS_list = homeROS['PLAYER_NAME'].tolist()
    
        away_players_opponents = list(it.product(awayROS_list, homeROS_list))
    
        home_players_opponents = list(it.product(homeROS_list, awayROS_list))
    
        # begin looping by team   
        for team in teams:
    
            if team == away:
                team_text = 'AWAY'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'
                opponent_text = 'HOME'
                opponentON = opponent_text + 'ON'             
                team_players_opponents = away_players_opponents
    
    
            elif team == home:
                team_text = 'HOME'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'
                opponent_text = 'AWAY'
                opponentON = opponent_text + 'ON'            
                team_players_opponents = home_players_opponents

    
            ###
            ### ALL
            ###
    
            # add a loop for players-opponents
            for player_opponent in team_players_opponents:
    
                player = player_opponent[0:][0]
                player_lastname = player.rsplit('.', 1)[1]
                
                opponent = player_opponent[0:][1]
                opponent_lastname = opponent.rsplit('.', 1)[1]

                              
                ###
                ### TIME ON ICE
                ###
                
                toi_all_first = TOI_df[(TOI_df[teamON].str.contains(player)) & (TOI_df[opponentON].str.contains(opponent))].count()                      
                toi_all = round(toi_all_first[1] * 0.0166667, 1)
    
                if toi_all == 0:
                    continue

    
                ###
                ### PLAY-BY-PLAY
                ###      
                
                pbp_df = pbp_df_start.copy()
                pbp_df = pbp_df[(pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))]
                
                #
                # INDIVIDUAL
                #

                #
                # shot-based metrics
                #

                # goals, assists and primary assists
                event = 'Goal'
                G_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                try:
                    A1_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A1_all = 0
    
                try:
                    A2_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df['PLAYER_C'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A2_all = 0
    
                A_all = A1_all + A2_all
    
                # points and primary points
                PTS_all = G_all + A_all
                PTS1_all = G_all + A1_all          
                
                # on-net shots (shots that scored or were saved)
                event = 'Save'
                ONS_all = G_all + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]           
    
                # unblocked shots (shots that scored, were saved or missed)
                event = 'Miss'
                US_all = ONS_all + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
               
                # shots (shots that scored, were saved, missed or were blocked)
                event = 'Shot'
                S_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                
                # expected goals               
                xG_all = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                #
                # non-shot or defending metrics
                #
                
                # faceoffs
                event = 'Faceoff'
                FO_all = (pbp_df[(pbp_df['EVENT'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1] +
                            pbp_df[(pbp_df['EVENT'] == event) & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1])

                FOW_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # penalties
                event = 'Penalty'
                PD_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                PT_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # shot blocks
                event = 'Block'
                SB_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # arrange individual player data to record                
                individual_all = (G_all, xG_all, A_all, A1_all, PTS_all, PTS1_all, ONS_all, US_all, S_all, FO_all, FOW_all, PD_all, PT_all, SB_all)
                
                #
                # ON-ICE
                #
                
                #
                # shot-based metrics
                #

                # goals (shots that scored) for and against
                event = 'Goal'
                GF_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                GA_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                            
                GD_all = GF_all - GA_all
    
                # on-net shots (shots that scored or were saved) for and against
                event = 'Save'
                ONSF_all = GF_all + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                ONSA_all = GA_all + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                ONSD_all = ONSF_all - ONSA_all
    
                # unblocked shots (shots that scored, were saved or missed) for and against
                event = 'Miss'
                USF_all = ONSF_all + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                USA_all = ONSA_all + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                USD_all = USF_all - USA_all
    
                ### shots (shots that scored, were saved, missed or were blocked) for and against
                event = 'Shot'
                SF_all = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                SA_all = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                SD_all = SF_all - SA_all
                
                # expected goals for and against
                xGF_all = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)
                xGA_all = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)
               
                xGD_all = xGF_all - xGA_all                             
                
                #
                # non-shot or defending metrics
                #
                
                # faceoffs taken together
                event = 'Faceoff'
                FO_all = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                # arrange on-ice player data to record    
                onice_all = (GF_all, GA_all, xGF_all, xGA_all, ONSF_all, ONSA_all, USF_all, USA_all, SF_all, SA_all, GD_all, xGD_all, ONSD_all, USD_all, SD_all, FO_all)


                ###
                ### WRITE TO FILE
                ###
                
                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'
    
                # write out individual player data vs. opponent
                individual_out.writerow((season_id, game_id, date, team_text, team, player, opponent, 'ALL', '1', toi_all) + individual_all)
                
                # status update
                print('Processing ' + team + ' individual (All) stats for ' + player + ' with ' + opponent)
    
                # write out on-ice player data vs. opponent
                onice_out.writerow((season_id, game_id, date, team_text, team, player, opponent, 'ALL', '1', toi_all) + onice_all)
                
                # status update
                print('Processing ' + team + ' on-ice (All) player stats for ' + player + ' with ' + opponent)
    
    
            ###
            ### 5v5
            ###
    
            # loop through players-opponents again
            for player_opponent in team_players_opponents:
    
                player = player_opponent[0:][0]
                player_lastname = player.rsplit('.', 1)[1]
                
                opponent = player_opponent[0:][1]
                opponent_lastname = opponent.rsplit('.', 1)[1]


                ###
                ### TIME ON ICE
                ###
                
                toi_5v5_first = TOI_df[(TOI_df[team_strength] == '5v5') & (TOI_df[teamON].str.contains(player)) & (TOI_df[opponentON].str.contains(opponent))].count()                      
                toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)
    
                if toi_5v5 == 0:
                    continue

    
                ###
                ### PLAY-BY-PLAY
                ###      
               
                #
                # INDIVIDUAL
                #

                #
                # shot-based metrics
                #

                # goals, assists and primary assists
                event = 'Goal'
                G_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                try:
                    A1_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A1_5v5 = 0
    
                try:
                    A2_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_C'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A2_5v5 = 0
    
                A_5v5 = A1_5v5 + A2_5v5
    
                # points and primary points
                PTS_5v5 = G_5v5 + A_5v5
                PTS1_5v5 = G_5v5 + A1_5v5           
                
                # on-net shots (shots that scored or were saved)
                event = 'Save'
                ONS_5v5 = G_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]           
    
                # unblocked shots (shots that scored, were saved or missed)
                event = 'Miss'
                US_5v5 = ONS_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
               
                # shots (shots that scored, were saved, missed or were blocked)
                event = 'Shot'
                S_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # expected goals
                xG_5v5 = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                #
                # non-shot or defending metrics
                #
                
                # faceoffs
                event = 'Faceoff'
                FO_5v5 = (pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1] +
                            pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1])

                FOW_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # penalties
                event = 'Penalty'
                PD_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                PT_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # shot blocks
                event = 'Block'
                SB_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
 
                # arrange individual player data to record                                
                individual_5v5 = (G_5v5, xG_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5, FO_5v5, FOW_5v5, PD_5v5, PT_5v5, SB_5v5)
                               
                #
                # ON-ICE
                #
    
                #
                # shot-based metrics
                #
    
                # goals (shots that scored) for and against
                event = 'Goal'
                GF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                GA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                            
                GD_5v5 = GF_5v5 - GA_5v5  
    
                ### on-net shots (shots that scored or were saved) for and against
                event = 'Save'
                ONSF_5v5 = GF_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                ONSA_5v5 = GA_5v5 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                ONSD_5v5 = ONSF_5v5 - ONSA_5v5
    
                # unblocked shots (shots that scored, were saved or missed) for and against
                event = 'Miss'
                USF_5v5 = ONSF_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                USA_5v5 = ONSA_5v5 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                USD_5v5 = USF_5v5 - USA_5v5
    
                # shots (shots that scored, were saved, missed or were blocked) for and against
                event = 'Shot'
                SF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                SA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                SD_5v5 = SF_5v5 - SA_5v5

                # expected goals for and against
                xGF_5v5 = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)
                xGA_5v5 = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                xGD_5v5 = xGF_5v5 - xGA_5v5                
                
                #
                # non-shot or defending metrics
                #
               
                # faceoffs taken together
                event = 'Faceoff'
                FO_5v5 = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                # arrange on-ice player data to record    
                onice_5v5 = (GF_5v5, GA_5v5, xGF_5v5, xGA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, xGD_5v5, ONSD_5v5, USD_5v5, SD_5v5, FO_5v5)
    
    
                ###
                ### WRITE TO FILE
                ###

                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'
    
                # write out individual player data vs. opponent
                individual_out.writerow((season_id, game_id, date, team_text, team, player, opponent, '5v5', '1', toi_5v5) + individual_5v5)
                
                # status update
                print('Processing ' + team + ' individual (5v5) stats for ' + player + ' with ' + opponent)
    
                # write out on-ice player data vs. opponent
                onice_out.writerow((season_id, game_id, date, team_text, team, player, opponent, '5v5', '1', toi_5v5) + onice_5v5)
                
                # status update
                print('Processing ' + team + ' on-ice (5v5) player stats for ' + player + ' with ' + opponent)
    
    
            ###
            ### POWER PLAY
            ###
    
            # loop through players-opponents again
            for player_opponent in team_players_opponents:
    
                player = player_opponent[0:][0]
                player_lastname = player.rsplit('.', 1)[1]
                
                opponent = player_opponent[0:][1]
                opponent_lastname = opponent.rsplit('.', 1)[1]


                ###
                ### TIME ON ICE
                ###
                
                toi_PP_first = TOI_df[(TOI_df[team_state] == 'PP') & (TOI_df[teamON].str.contains(player)) & (TOI_df[teamON].str.contains(opponent))].count()                       
                toi_PP = round(toi_PP_first[1] * 0.0166667, 1)
    
                if toi_PP == 0:
                    continue

    
                ###
                ### PLAY-BY-PLAY
                ###      
               
                #
                # INDIVIDUAL
                #

                #
                # shot-based metrics
                #

                # goals, assists and primary assists
                event = 'Goal'
                G_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == '5v5') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                try:
                    A1_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A1_PP = 0
    
                try:
                    A2_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_C'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A2_PP = 0
    
                A_PP = A1_PP + A2_PP
    
                # points and primary points
                PTS_PP = G_PP + A_PP
                PTS1_PP = G_PP + A1_PP           
                
                # on-net shots (shots that scored or were saved)
                event = 'Save'
                ONS_PP = G_PP + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]           
    
                # unblocked shots (shots that scored, were saved or missed)
                event = 'Miss'
                US_PP = ONS_PP + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
               
                # shots (shots that scored, were saved, missed or were blocked)
                event = 'Shot'
                S_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # expected goals
                xG_PP = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                #
                # non-shot or defending metrics
                #
                
                # faceoffs
                event = 'Faceoff'
                FO_PP = (pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1] +
                            pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1])

                FOW_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # penalties
                event = 'Penalty'
                PD_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                PT_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # shot blocks
                event = 'Block'
                SB_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                # arrange individual player data to record
                individual_PP = (G_PP, xG_PP, A_PP, A1_PP, PTS_PP, PTS1_PP, ONS_PP, US_PP, S_PP, FO_PP, FOW_PP, PD_PP, PT_PP, SB_PP)
                
                #
                # ON-ICE
                #

                #
                # shot-based metrics
                #

                # goals (shots that scored) for and against
                event = 'Goal'
                GF_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                GA_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                            
                GD_PP = GF_PP - GA_PP  
    
                # on-net shots (shots that scored or were saved) for and against
                event = 'Save'
                ONSF_PP = GF_PP + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                ONSA_PP = GA_PP + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                ONSD_PP = ONSF_PP - ONSA_PP
    
                # unblocked shots (shots that scored, were saved or missed) for and against
                event = 'Miss'
                USF_PP = ONSF_PP + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                USA_PP = ONSA_PP + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                USD_PP = USF_PP - USA_PP
    
                # shots (shots that scored, were saved, missed or were blocked) for and against
                event = 'Shot'
                SF_PP = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                SA_PP = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                SD_PP = SF_PP - SA_PP

                # expected goals for and against
                xGF_PP = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)
                xGA_PP = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_state] == 'PP') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                xGD_PP = xGF_PP - xGA_PP
                
                #
                # non-shot or defending metrics
                #
                
                # faceoffs taken together
                event = 'Faceoff'
                FO_PP = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'PP') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                # arrange on-ice player data to record    
                onice_PP = (GF_PP, GA_PP, xGF_PP, xGA_PP, ONSF_PP, ONSA_PP, USF_PP, USA_PP, SF_PP, SA_PP, GD_PP, xGD_PP, ONSD_PP, USD_PP, SD_PP, FO_PP)
    

                ###
                ### WRITE TO FILE
                ###

                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'
    
                # write out individual player data vs. opponent
                individual_out.writerow((season_id, game_id, date, team_text, team, player, opponent, 'PP', '1', toi_PP) + individual_PP)
                
                # status update
                print('Processing ' + team + ' individual (PP) stats for ' + player + ' with ' + opponent)
    
                # write out on-ice player data vs. opponent
                onice_out.writerow((season_id, game_id, date, team_text, team, player, opponent, 'PP', '1', toi_PP) + onice_PP)
                
                # status update
                print('Processing ' + team + ' on-ice (PP) player stats for ' + player + ' with ' + opponent)
    
    
            ###
            ### SHORTHANDED
            ###
    
            # loop through players-opponents a final time
            for player_opponent in team_players_opponents:
    
                player = player_opponent[0:][0]
                player_lastname = player.rsplit('.', 1)[1]
                
                opponent = player_opponent[0:][1]
                opponent_lastname = opponent.rsplit('.', 1)[1]


                ###
                ### TIME ON ICE
                ###
                
                toi_SH_first = TOI_df[(TOI_df[team_state] == 'SH') & (TOI_df[teamON].str.contains(player)) & (TOI_df[opponentON].str.contains(opponent))].count()                       
                toi_SH = round(toi_SH_first[1] * 0.0166667, 1)
    
                if toi_SH == 0:
                    continue

    
                ###
                ### PLAY-BY-PLAY
                ###      
               
                #
                # INDIVIDUAL
                #

                #
                # shot-based metrics
                #

                # goals, assists and primary assists
                event = 'Goal'
                G_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                try:
                    A1_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A1_SH = 0
    
                try:
                    A2_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_C'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                except:
                    A2_SH = 0
    
                A_SH = A1_SH + A2_SH
    
                # points and primary points
                PTS_SH = G_SH + A_SH
                PTS1_SH = G_SH + A1_SH    
                  
                # on-net shots (shots that scored or were saved)
                event = 'Save'
                ONS_SH = G_SH + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]           
    
                # unblocked shots (shots that scored, were saved or missed)
                event = 'Miss'
                US_SH = ONS_SH + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
               
                # shots (shots that scored, were saved, missed or were blocked)
                event = 'Shot'
                S_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # expected goals
                xG_SH = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                #
                # non-shot or defending metrics
                #
                
                # faceoffs
                event = 'Faceoff'
                FO_SH = (pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1] +
                            pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1])

                FOW_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # penalties
                event = 'Penalty'
                PD_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                PT_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_A'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # shot blocks
                event = 'Block'
                SB_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df['PLAYER_B'] == player) & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]

                # arrange individual player data to record
                individual_SH = (G_SH, xG_SH, A_SH, A1_SH, PTS_SH, PTS1_SH, ONS_SH, US_SH, S_SH, FO_SH, FOW_SH, PD_SH, PT_SH, SB_SH)
                
                #
                # ON-ICE
                #

                #
                # shot-based metrics
                #

                # goals (shots that scored) for and against
                event = 'Goal'
                GF_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                GA_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                            
                GD_SH = GF_SH - GA_SH  
    
                # on-net shots (shots that scored or were saved) for and against
                event = 'Save'
                ONSF_SH = GF_SH + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                ONSA_SH = GA_SH + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                ONSD_SH = ONSF_SH - ONSA_SH
    
                # unblocked shots (shots that scored, were saved or missed) for and against
                event = 'Miss'
                USF_SH = ONSF_SH + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                USA_SH = ONSA_SH + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                USD_SH = USF_SH - USA_SH
    
                # shots (shots that scored, were saved, missed or were blocked) for and against
                event = 'Shot'
                SF_SH = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
                SA_SH = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                SD_SH = SF_SH - SA_SH
                
                # expected goals for and against
                xGF_SH = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)
                xGA_SH = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_state] == 'SH') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent)), pbp_df['xG'], 0).sum(), 2)

                xGD_SH = xGF_SH - xGA_SH
                
                #
                # non-shot or defending metrics
                #
                
                # faceoffs taken together
                event = 'Faceoff'
                FO_SH = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_state] == 'SH') & (pbp_df[teamON].str.contains(player)) & (pbp_df[opponentON].str.contains(opponent))].count()[1]
    
                # arrange on-ice player data to record                    
                onice_SH = (GF_SH, GA_SH, xGF_SH, xGA_SH, ONSF_SH, ONSA_SH, USF_SH, USA_SH, SF_SH, SA_SH, GD_SH, xGD_SH, ONSD_SH, USD_SH, SD_SH, FO_SH)
    
    
                ###
                ### WRITE TO FILE
                ###

                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'
    
                # write out individual player data vs. opponent
                individual_out.writerow((season_id, game_id, date, team_text, team, player, opponent, 'SH', '1', toi_SH) + individual_SH)

                # status update
                print('Processing ' + team + ' individual (SH) stats for ' + player + ' with ' + opponent)
    
                # write out on-ice player data vs. opponent
                onice_out.writerow((season_id, game_id, date, team_text, team, player, opponent, 'SH', '1', toi_SH) + onice_SH)
                
                # status update
                print('Processing ' + team + ' on-ice (SH) player stats for ' + player + ' with ' + opponent)
                
    # status update
    print('Finished generating player with opponent stats for ' + season_id + ' ' + game_id)