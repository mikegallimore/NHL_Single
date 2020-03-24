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
    stats_players_individual = files_root + 'stats_players_individual.csv'
    stats_units_individual = files_root + 'stats_units_pp_individual.csv'
    stats_units_onice = files_root + 'stats_units_pp_onice.csv'
    
    # create a dataframe for extracting TOI info; add a column with all of the on-ice players for expedited searching; derive the last on-ice second recorded
    TOI_df = pd.read_csv(TOI_matrix).fillna("NaN")
    TOI_df = TOI_df[(TOI_df['HOME_STATE'] == 'PP') | (TOI_df['AWAY_STATE'] == 'PP')]

    TOI_df['HOMEON_5'].fillna('NaN', inplace = True)
    TOI_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    TOI_df['AWAYON_5'].fillna('NaN', inplace = True)
    TOI_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    TOI_df['HOMEON'] = TOI_df['HOMEON_1'] + ', ' + TOI_df['HOMEON_2'] + ', ' + TOI_df['HOMEON_3'] + ', ' + TOI_df['HOMEON_4'] + ', ' + TOI_df['HOMEON_5'] + ', ' + TOI_df['HOMEON_6']
    TOI_df['AWAYON'] = TOI_df['AWAYON_1'] + ', ' + TOI_df['AWAYON_2'] + ', ' + TOI_df['AWAYON_3'] + ', ' + TOI_df['AWAYON_4'] + ', ' + TOI_df['AWAYON_5'] + ', ' + TOI_df['AWAYON_6']
     
    # create a dataframe for extracting play-by-play info; add a column with all of the on-ice players for expedited searching
    pbp_df = pd.read_csv(pbp)
    pbp_df = pbp_df[(pbp_df['HOME_STATE'] == 'PP') | (pbp_df['AWAY_STATE'] == 'PP')]
    
    pbp_df['HOMEON_5'].fillna('NaN', inplace = True)
    pbp_df['HOMEON_6'].fillna('NaN', inplace = True)
    
    pbp_df['AWAYON_5'].fillna('NaN', inplace = True)
    pbp_df['AWAYON_6'].fillna('NaN', inplace = True)
    
    pbp_df['HOMEON'] = pbp_df['HOMEON_1'] + ', ' + pbp_df['HOMEON_2'] + ', ' + pbp_df['HOMEON_3'] + ', ' + pbp_df['HOMEON_4'] + ', ' + pbp_df['HOMEON_5'] + ', ' + pbp_df['HOMEON_6']
    pbp_df['AWAYON'] = pbp_df['AWAYON_1'] + ', ' + pbp_df['AWAYON_2'] + ', ' + pbp_df['AWAYON_3'] + ', ' + pbp_df['AWAYON_4'] + ', ' + pbp_df['AWAYON_5'] + ', ' + pbp_df['AWAYON_6']
       
    # trigger the csv files that will be written; write column titles to a header row 
    with open(stats_units_individual, 'w', newline = '') as units_individual, open(stats_units_onice, 'w', newline = '') as units_onice:
    
        individual_out = csv.writer(units_individual)
        individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER_1', 'PLAYER_2', 'PLAYER_3', 'PLAYER_4', 'PLAYER_5', 'UNIT', 'STATE', 'STRENGTH', 'GP', 'TOI', 'G', 'xG', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S'])
    
        onice_out = csv.writer(units_onice)
        onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'PLAYER_1', 'PLAYER_2', 'PLAYER_3', 'PLAYER_4', 'PLAYER_5', 'UNIT', 'STATE', 'STRENGTH', 'GP', 'TOI', 'GF', 'GA', 'xGF', 'xGA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'xGD', 'ONSD', 'USD', 'SD', 'FO'])
    
        # access the game's roster file in order to create team-specific dicts for later use converting numbers to names
        players_df = pd.read_csv(stats_players_individual)
        players_df = players_df[(players_df['STATE'] == 'PP') & (players_df['TOI'] > 0)]
               
        players_table = players_df[['TEAM','NO', 'PLAYER', 'POS']]
   
        home_players_df = players_table.copy()
        home_players_df = home_players_df[(home_players_df['TEAM'] == home)].sort_values(by=['NO'])
        home_skaters_df = home_players_df[(home_players_df['POS'] != 'G')]
        home_skaters_list = home_skaters_df['PLAYER'].tolist()

        away_players_df = players_table.copy()
        away_players_df = away_players_df[(away_players_df['TEAM'] == away)].sort_values(by=['NO'])
        away_skaters_df = away_players_df[(away_players_df['POS'] != 'G')]
        away_skaters_list = away_skaters_df['PLAYER'].tolist()
   
        # begin looping by team
        for team in teams:
    
            if team == away:
                team_text = 'AWAY'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'
                team_units = list(it.combinations(away_skaters_list, 5))
    
            elif team == home:
                team_text = 'HOME'
                team_state = team_text + '_STATE'
                team_strength = team_text + '_STRENGTH'
                team_zone = team_text + '_ZONE'
                teamON = team_text + 'ON'
                team_units = list(it.combinations(home_skaters_list, 5))

            if len(team_units) == 0:
                continue
            
            # add a loop for power play units
            for unit in team_units:
    
                skater_1 = unit[0]
                skater_1_lastname = skater_1.rsplit('.', 1)[1]
    
                skater_2 = unit[1]
                skater_2_lastname = skater_2.rsplit('.', 1)[1]
    
                skater_3 = unit[2]
                skater_3_lastname = skater_3.rsplit('.', 1)[1]
 
                skater_4 = unit[3]
                skater_4_lastname = skater_4.rsplit('.', 1)[1]

                skater_5 = unit[4]
                skater_5_lastname = skater_5.rsplit('.', 1)[1]
               
                unit = skater_1 + '-' + skater_2 + '-' + skater_3 + '-' + skater_4 + '-' + skater_5
                unit_lastname = skater_1_lastname + '-' + skater_2_lastname + '-' + skater_3_lastname + '-' + skater_4_lastname + '-' + skater_5_lastname
              
                ###
                ### TIME ON ICE
                ###
    
                toi_PP_first = TOI_df[(TOI_df[team_state] == 'PP') & (TOI_df[teamON].str.contains(skater_1)) & (TOI_df[teamON].str.contains(skater_2)) & (TOI_df[teamON].str.contains(skater_3)) & (TOI_df[teamON].str.contains(skater_4)) & (TOI_df[teamON].str.contains(skater_5))].count()
                toi_PP = round(toi_PP_first[1] * 0.0166667, 1)
    
                if toi_PP == 0:
                    continue

                toi_5v4_first = TOI_df[(TOI_df[team_strength] == '5v4') & (TOI_df[teamON].str.contains(skater_1)) & (TOI_df[teamON].str.contains(skater_2)) & (TOI_df[teamON].str.contains(skater_3)) & (TOI_df[teamON].str.contains(skater_4)) & (TOI_df[teamON].str.contains(skater_5))].count()
                toi_5v4 = round(toi_5v4_first[1] * 0.0166667, 1)
                
                toi_5v3_first = TOI_df[(TOI_df[team_strength] == '5v3') & (TOI_df[teamON].str.contains(skater_1)) & (TOI_df[teamON].str.contains(skater_2)) & (TOI_df[teamON].str.contains(skater_3)) & (TOI_df[teamON].str.contains(skater_4)) & (TOI_df[teamON].str.contains(skater_5))].count()
                toi_5v3 = round(toi_5v3_first[1] * 0.0166667, 1)

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
                G_5v4 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                        )

                G_5v3 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                        )
    
                try:
                    A1_5v4 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                            )
                except:
                    A1_5v4 = 0
                try:
                    A1_5v3 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                            )
                except:
                    A1_5v3 = 0
    
                try:
                    A2_5v4 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_B'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                            )
                except:
                    A2_5v4 = 0
                try:
                    A2_5v3 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_B'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                            )
                except:
                    A2_5v3 = 0
    
                A_5v4 = A1_5v4 + A2_5v4
                A_5v3 = A1_5v3 + A2_5v3
    
                # points and primary points
                PTS_5v4 = G_5v4 + A_5v4   
                PTS1_5v4 = G_5v4 + A1_5v4

                PTS_5v3 = G_5v3 + A_5v3   
                PTS1_5v3 = G_5v3 + A1_5v3
    
                # on-net shots (shots that scored or were saved)
                event = 'Save'
                ONS_5v4 = G_5v4 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                                    )

                ONS_5v3 = G_5v3 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                                    )
    
                # unblocked shots (shots that scored, were saved or missed)
                event = 'Miss'
                US_5v4 = ONS_5v4 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                                    )

                US_5v3 = ONS_5v3 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                                    )
    
                # shots (shots that scored, were saved, missed or were blocked)
                event = 'Shot'
                S_5v4 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                        )

                S_5v3 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5))].count()[1] +
                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4))].count()[1]
                        )

                # expected goals
                xG_5v4 = (round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v4') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)), pbp_df['xG'], 0).sum(), 2)
                                )

                xG_5v3 = (round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_1) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_2) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_3) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_4) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum() +
                                np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[team_strength] == '5v3') & (pbp_df['PLAYER_A'] == skater_5) & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)), pbp_df['xG'], 0).sum(), 2)
                                )
                
                # arrange individual line data to record
                individual_5v4 = (G_5v4, xG_5v4, A_5v4, A1_5v4, PTS_5v4, PTS1_5v4, ONS_5v4, US_5v4, S_5v4)
                individual_5v3 = (G_5v3, xG_5v3, A_5v3, A1_5v3, PTS_5v3, PTS1_5v3, ONS_5v3, US_5v3, S_5v3)
    
                #
                # ON-ICE
                #

                #
                # shot-based metrics
                #

                # goals (shots that scored) for and against
                event = 'Goal'
                GF_5v4 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                GA_5v4 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                GD_5v4 = GF_5v4 - GA_5v4
 
                GF_5v3 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                GA_5v3 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                GD_5v3 = GF_5v3 - GA_5v3
    
                # on-net shots (shots that scored or were saved) for and against
                event = 'Save'
                ONSF_5v4 = GF_5v4 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                ONSA_5v4 = GA_5v4 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                ONSD_5v4 = ONSF_5v4 - ONSA_5v4

                ONSF_5v3 = GF_5v3 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                ONSA_5v3 = GA_5v3 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                ONSD_5v3 = ONSF_5v3 - ONSA_5v3
    
                # unblocked shots (shots that scored, were saved or missed) for and against
                event = 'Miss'
                USF_5v4 = ONSF_5v4 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                USA_5v4 = ONSA_5v4 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                USD_5v4 = USF_5v4 - USA_5v4

                USF_5v3 = ONSF_5v3 + pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                USA_5v3 = ONSA_5v3 + pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                USD_5v3 = USF_5v3 - USA_5v3
    
                # shots (shots that scored, were saved, missed or were blocked) for and against
                event = 'Shot'
                SF_5v4 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                SA_5v4 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                SD_5v4 = SF_5v4 - SA_5v4

                SF_5v3 = pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                SA_5v3 = pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
    
                SD_5v3 = SF_5v3 - SA_5v3

                # expected goals for and against
                xGF_5v4 = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v4') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum(), 2)
                xGA_5v4 = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v4') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum(), 2)

                xGD_5v4 = xGF_5v4 - xGA_5v4

                xGF_5v3 = round(np.where((pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v3') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum(), 2)
                xGA_5v3 = round(np.where((pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == 'Shot')  & (pbp_df[team_strength] == '5v3') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5)), pbp_df['xG'], 0).sum(), 2)

                xGD_5v3 = xGF_5v3 - xGA_5v3

                #
                # non-shot or defending metrics
                #
                
                # faceoffs taken together
                event = 'Faceoff'
                FO_5v4 = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v4') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                FO_5v3 = pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v3') & (pbp_df[teamON].str.contains(skater_1)) & (pbp_df[teamON].str.contains(skater_2)) & (pbp_df[teamON].str.contains(skater_3)) & (pbp_df[teamON].str.contains(skater_4)) & (pbp_df[teamON].str.contains(skater_5))].count()[1]
                
                # arrange on-ice line data to record                
                onice_5v4 = (GF_5v4, GA_5v4, xGF_5v4, xGA_5v4, ONSF_5v4, ONSA_5v4, USF_5v4, USA_5v4, SF_5v4, SA_5v4, GD_5v4, xGD_5v4, ONSD_5v4, USD_5v4, SD_5v4, FO_5v4)
                onice_5v3 = (GF_5v3, GA_5v3, xGF_5v3, xGA_5v3, ONSF_5v3, ONSA_5v3, USF_5v3, USA_5v3, SF_5v3, SA_5v3, GD_5v3, xGD_5v3, ONSD_5v3, USD_5v3, SD_5v3, FO_5v3)


                ###
                ### WRITE TO FILE
                ###
                
                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'
    
                # write out individual line data
                individual_out.writerow((season_id, game_id, date, team_text, team, skater_1, skater_2, skater_3, skater_4, skater_5, unit_lastname, 'PP', '5v4', '1', toi_5v4) + individual_5v4)
                individual_out.writerow((season_id, game_id, date, team_text, team, skater_1, skater_2, skater_3, skater_4, skater_5, unit_lastname, 'PP', '5v3', '1', toi_5v3) + individual_5v3)
                
                # status update
                print('Processing ' + team + ' individual stats for ' + unit_lastname)
    
                # write out on-ice line data
                onice_out.writerow((season_id, game_id, date, team_text, team, skater_1, skater_2, skater_3, skater_4, skater_5, unit_lastname, 'PP', '5v4', '1', toi_5v4) + onice_5v4)
                onice_out.writerow((season_id, game_id, date, team_text, team, skater_1, skater_2, skater_3, skater_4, skater_5, unit_lastname, 'PP', '5v3', '1', toi_5v3) + onice_5v3)
                
                # status update
                print('Processing ' + team + ' on-ice stats for ' + unit_lastname)
    
    # status update
    print('Finished generating power play unit stats for ' + season_id + ' ' + game_id)