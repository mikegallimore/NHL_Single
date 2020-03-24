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
    stats_individual = files_root + 'stats_units_pairings_individual.csv'
    stats_onice = files_root + 'stats_units_pairings_onice.csv'
    
    # create a dataframe for extracting TOI info; add a column with all of the on-ice players for expedited searching; derive the last on-ice second recorded
    TOI_df = pd.read_csv(TOI_matrix).fillna("NaN")
    
    TOI_df['HOMEON_5'].fillna('NaN', inplace = True)
    TOI_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    TOI_df['AWAYON_5'].fillna('NaN', inplace = True)
    TOI_df['AWAYON_6'].fillna('NaN', inplace = True)
        
    TOI_df['HOMEON'] = TOI_df['HOMEON_1'] + ', ' + TOI_df['HOMEON_2'] + ', ' + TOI_df['HOMEON_3'] + ', ' + TOI_df['HOMEON_4'] + ', ' + TOI_df['HOMEON_5'] + ', ' + TOI_df['HOMEON_6']
    TOI_df['AWAYON'] = TOI_df['AWAYON_1'] + ', ' + TOI_df['AWAYON_2'] + ', ' + TOI_df['AWAYON_3'] + ', ' + TOI_df['AWAYON_4'] + ', ' + TOI_df['AWAYON_5'] + ', ' + TOI_df['AWAYON_6']
    
    # create a dataframe for extracting play-by-play info; add a column with all of the on-ice players for expedited searching
    pbp_df_start = pd.read_csv(pbp)
    
    pbp_df_start['HOMEON_5'].fillna('NaN', inplace = True)
    pbp_df_start['HOMEON_6'].fillna('NaN', inplace = True)
    
    pbp_df_start['AWAYON_5'].fillna('NaN', inplace = True)
    pbp_df_start['AWAYON_6'].fillna('NaN', inplace = True)
    
    pbp_df_start['HOMEON'] = pbp_df_start['HOMEON_1'] + ', ' + pbp_df_start['HOMEON_2'] + ', ' + pbp_df_start['HOMEON_3'] + ', ' + pbp_df_start['HOMEON_4'] + ', ' + pbp_df_start['HOMEON_5'] + ', ' + pbp_df_start['HOMEON_6']
    pbp_df_start['AWAYON'] = pbp_df_start['AWAYON_1'] + ', ' + pbp_df_start['AWAYON_2'] + ', ' + pbp_df_start['AWAYON_3'] + ', ' + pbp_df_start['AWAYON_4'] + ', ' + pbp_df_start['AWAYON_5'] + ', ' + pbp_df_start['AWAYON_6']
    
    # trigger the csv files that will be written; write column titles to a header row 
    with open(stats_individual, 'w', newline = '') as players_individual, open(stats_onice, 'w', newline = '') as players_onice:
    
        individual_out = csv.writer(players_individual)
        individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'DEFENDER_1', 'DEFENDER_2', 'PAIRING', 'STATE', 'GP', 'TOI', 'G', 'xG', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S'])
    
        onice_out = csv.writer(players_onice)
        onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'DEFENDER_1', 'DEFENDER_2', 'PAIRING', 'STATE', 'GP', 'TOI', 'GF', 'GA', 'xGF', 'xGA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'xGD', 'ONSD', 'USD', 'SD', 'FO'])
    
        ### access the game's roster file in order to create team-specific dicts for later use converting numbers to names
        rosters_csv = files_root + 'rosters.csv'
    
        rosters_df = pd.read_csv(rosters_csv)
    
        rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS']]
    
        homeROS_df = rosters_table.copy()
        homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)].sort_values(by=['PLAYER_NO'])
        homeD_df = homeROS_df[(homeROS_df['PLAYER_POS'] == 'D')]
        homeD_list = homeD_df['PLAYER_NAME'].tolist()
    
        awayROS_df = rosters_table.copy()
        awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)].sort_values(by=['PLAYER_NO'])
        awayD_df = awayROS_df[(awayROS_df['PLAYER_POS'] == 'D')]
        awayD_list = awayD_df['PLAYER_NAME'].tolist()
    
        # begin looping by team
        for team in teams:
    
            if team == away:
                team_text = 'AWAY'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'
                team_pairings = list(it.combinations(awayD_list, 2))
    
            elif team == home:
                team_text = 'HOME'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'
                team_pairings = list(it.combinations(homeD_list, 2))
    
            # add a loop for defense pairs
            for pair in team_pairings:
    
                defender_1 = pair[0:][0]
                defender_1_lastname = pair[0:][0].rsplit('.', 1)[1]
    
                defender_2 = pair[0:][1]
                defender_2_lastname = pair[0:][1].rsplit('.', 1)[1]
    
                pairing = defender_1 + '-' + defender_2
                pairing_lastname = defender_1_lastname + '-' + defender_2_lastname


                ###
                ### TIME ON ICE
                ###
    
                toi_5v5_first = TOI_df[(TOI_df[team_strength] == '5v5') & (TOI_df[teamON].str.contains(defender_1)) & (TOI_df[teamON].str.contains(defender_2))].count()
                toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)
    
                if toi_5v5 == 0:
                    continue

    
                ###
                ### PLAY-BY-PLAY
                ###

                pbp_df = pbp_df_start.copy()
                pbp_df = pbp_df[(pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))]               

                #
                # INDIVIDUAL
                #
                
                # 
                # shot-based metrics
                #
                
                # goals, assists and primary assists
                event = 'Goal'
                G_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_1) & (pbp_df[teamON].str.contains(defender_2))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_2) & (pbp_df[teamON].str.contains(defender_1))].count()[1]
                        )
    
                try:
                    A1_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_B'] == defender_1) & (pbp_df[teamON].str.contains(defender_2))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_B'] == defender_2) & (pbp_df[teamON].str.contains(defender_1))].count()[1]
                            )
                except:
                    A1_5v5 = 0
    
                try:
                    A2_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_C'] == defender_1) & (pbp_df[teamON].str.contains(defender_2))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_C'] == defender_2) & (pbp_df[teamON].str.contains(defender_1))].count()[1]
                            )
                except:
                    A2_5v5 = 0
    
                A_5v5 = A1_5v5 + A2_5v5
    
                # points and primary points
                PTS_5v5 = G_5v5 + A_5v5
    
                PTS1_5v5 = G_5v5 + A1_5v5
    
                # on-net shots (shots that scored or were saved)
                event = 'Save'
                ONS_5v5 = G_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_1) & (pbp_df[teamON].str.contains(defender_2))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_2) & (pbp_df[teamON].str.contains(defender_1))].count()[1]
                                    )
    
                # unblocked shots (shots that scored, were saved or missed)
                event = 'Miss'
                US_5v5 = ONS_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_1) & (pbp_df[teamON].str.contains(defender_2))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_2) & (pbp_df[teamON].str.contains(defender_1))].count()[1]
                                    )
                
                # shots (shots that scored, were saved, missed or were blocked)
                event = 'Shot'
                S_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_1) & (pbp_df[teamON].str.contains(defender_2))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_2) & (pbp_df[teamON].str.contains(defender_1))].count()[1]
                        )

                # expected goals
                xG_5v5 = (round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_1) & (pbp_df[teamON].str.contains(defender_2)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v5') & (pbp_df['PLAYER_A'] == defender_2) & (pbp_df[teamON].str.contains(defender_1)), pbp_df['xG'], 0).sum(), 2)
                                )

                # arrange individual pairing data to record
                individual_5v5 = (G_5v5, xG_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5)
    
                #
                # ON-ICE
                #
                
                #
                # shot-based metrics
                #

                # goals (shots that scored) for and against
                event = 'Goal'
                GF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
                GA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
    
                GD_5v5 = GF_5v5 - GA_5v5
    
                # on-net shots (shots that scored or were saved) for and against
                event = 'Save'
                ONSF_5v5 = GF_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
                ONSA_5v5 = GA_5v5 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
    
                ONSD_5v5 = ONSF_5v5 - ONSA_5v5
    
                # unblocked shots (shots that scored, were saved or missed) for and against
                event = 'Miss'
                USF_5v5 = ONSF_5v5 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
                USA_5v5 = ONSA_5v5 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
    
                USD_5v5 = USF_5v5 - USA_5v5
    
                # shots (shots that scored, were saved, missed or were blocked) for and against
                event = 'Shot'
                SF_5v5 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
                SA_5v5 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
    
                SD_5v5 = SF_5v5 - SA_5v5
    
                # expected goals for and against
                xGF_5v5 = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2)), pbp_df['xG'], 0).sum(), 2)
                xGA_5v5 = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v5') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2)), pbp_df['xG'], 0).sum(), 2)

                xGD_5v5 = xGF_5v5 - xGA_5v5                                
                
                #
                # non-shot or defending metrics
                #
                
                # faceoffs taken together
                event = 'Faceoff'
                FO_5v5 = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & (pbp_df[teamON].str.contains(defender_1)) & (pbp_df[teamON].str.contains(defender_2))].count()[1]
    
                # arrange on-ice pairing data to record  
                onice_5v5 = (GF_5v5, GA_5v5, xGF_5v5, xGA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, xGD_5v5, ONSD_5v5, USD_5v5, SD_5v5, FO_5v5)
    

                ###
                ### WRITE TO FILE
                ###
                
                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'
    
                # write out individual pairing data
                individual_out.writerow((season_id, game_id, date, team_text, team, defender_1, defender_2, pairing_lastname, '5v5', '1', toi_5v5) + individual_5v5)
                
                # status update
                print('Processing ' + team + ' individual stats for ' + pairing_lastname)
    
                # write out on-ice pairing data
                onice_out.writerow((season_id, game_id, date, team_text, team, defender_1, defender_2, pairing_lastname, '5v5', '1', toi_5v5) + onice_5v5)
                
                # status update
                print('Processing ' + team + ' on-ice player stats for ' + pairing_lastname)
    
    # status update
    print('Finished generating pairing stats for ' + season_id + ' ' + game_id)