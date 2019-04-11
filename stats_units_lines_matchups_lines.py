# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 00:10:44 2017

@author: @mikegallimore
"""

import csv
import pandas as pd
import itertools as it
import parameters

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
date = parameters.date
home = parameters.home
away = parameters.away
teams = parameters.teams
files_root = parameters.files_root

### establish file locations and destinations
TOI_matrix = files_root + 'TOI_matrix.csv'
pbp = files_root + 'pbp.csv'
stats_individual = files_root + 'stats_units_lines_individual_matchups_lines.csv'
stats_onice = files_root + 'stats_units_lines_onice_matchups_lines.csv'

### create a dataframe for extracting TOI info; add a column with all of the on-ice players for expedited searching; derive the last on-ice second recorded
TOI_df = pd.read_csv(TOI_matrix).fillna("NaN")

TOI_df['HOMEON_5'].fillna('NaN', inplace = True)
TOI_df['HOMEON_6'].fillna('NaN', inplace = True)

TOI_df['AWAYON_5'].fillna('NaN', inplace = True)
TOI_df['AWAYON_6'].fillna('NaN', inplace = True)

TOI_df['HOMEON'] = TOI_df['HOMEON_1'] + ', ' + TOI_df['HOMEON_2'] + ', ' + TOI_df['HOMEON_3'] + ', ' + TOI_df['HOMEON_4'] + ', ' + TOI_df['HOMEON_5'] + ', ' + TOI_df['HOMEON_6']
TOI_df['AWAYON'] = TOI_df['AWAYON_1'] + ', ' + TOI_df['AWAYON_2'] + ', ' + TOI_df['AWAYON_3'] + ', ' + TOI_df['AWAYON_4'] + ', ' + TOI_df['AWAYON_5'] + ', ' + TOI_df['AWAYON_6']

toi_max = TOI_df['SECONDS_GONE'].max()

### create a dataframe for extracting play-by-play info; add a column with all of the on-ice players for expedited searching
pbp_df = pd.read_csv(pbp)

pbp_df['HOMEON_5'].fillna('NaN', inplace = True)
pbp_df['HOMEON_6'].fillna('NaN', inplace = True)

pbp_df['AWAYON_5'].fillna('NaN', inplace = True)
pbp_df['AWAYON_6'].fillna('NaN', inplace = True)

pbp_df['HOMEON'] = pbp_df['HOMEON_1'] + ', ' + pbp_df['HOMEON_2'] + ', ' + pbp_df['HOMEON_3'] + ', ' + pbp_df['HOMEON_4'] + ', ' + pbp_df['HOMEON_5'] + ', ' + pbp_df['HOMEON_6']
pbp_df['AWAYON'] = pbp_df['AWAYON_1'] + ', ' + pbp_df['AWAYON_2'] + ', ' + pbp_df['AWAYON_3'] + ', ' + pbp_df['AWAYON_4'] + ', ' + pbp_df['AWAYON_5'] + ', ' + pbp_df['AWAYON_6']

### trigger the csv files that will be written; write column titles to a header row 
with open(stats_individual, 'w', newline = '') as players_individual, open(stats_onice, 'w', newline = '') as players_onice:

    individual_out = csv.writer(players_individual)
    individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'FORWARD_1', 'FORWARD_2', 'FORWARD_3', 'LINE', 'OPPOSING_FORWARD_1', 'OPPOSING_FORWARD_2', 'OPPOSING_FORWARD_3', 'MATCHUP', 'STATE', 'GP', 'TOI', 'G', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S'])

    onice_out = csv.writer(players_onice)
    onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'FORWARD_1', 'FORWARD_2', 'FORWARD_3', 'LINE', 'OPPOSING_FORWARD_1', 'OPPOSING_FORWARD_2', 'OPPOSING_FORWARD_3', 'MATCHUP', 'STATE', 'GP', 'TOI', 'GF', 'GA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'ONSD', 'USD', 'SD', 'FO'])

    ### access the game's roster file in order to create team-specific dicts and lists
    rosters_csv = files_root + 'rosters.csv'
    rosters_df = pd.read_csv(rosters_csv)
    rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS', 'PLAYER_POS_DETAIL']]

    homeROS_df = rosters_table.copy()
    homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)].sort_values(by=['PLAYER_NO'])
    homeF_df = homeROS_df[(homeROS_df['PLAYER_POS'] == 'F')]
    homeF_list = homeF_df['PLAYER_NAME'].tolist()

    awayROS_df = rosters_table.copy()
    awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)].sort_values(by=['PLAYER_NO'])
    awayF_df = awayROS_df[(awayROS_df['PLAYER_POS'] == 'F')]
    awayF_list = awayF_df['PLAYER_NAME'].tolist()
    
    ### begin looping by team
    for team in teams:

        if team == away:
            team_text = 'AWAY'
            team_state = team_text + '_STATE'
            team_strength = team_text + '_STRENGTH'
            team_zone = team_text + '_ZONE'
            teamON = team_text + 'ON'
            team_lines = list(it.combinations(awayF_list, 3))
            opponent_text = 'HOME'
            opponent_state = opponent_text + '_STATE'
            opponent_strength = opponent_text + '_STRENGTH'
            opponent_zone = opponent_text + '_ZONE'
            opponentON = opponent_text + 'ON'
            opponent_lines = list(it.combinations(homeF_list, 3))

        elif team == home:
            team_text = 'HOME'
            team_state = team_text + '_STATE'
            team_strength = team_text + '_STRENGTH'
            team_zone = team_text + '_ZONE'
            teamON = team_text + 'ON'
            team_lines = list(it.combinations(homeF_list, 3)) 
            opponent_text = 'AWAY'
            opponent_state = opponent_text + '_STATE'
            opponent_strength = opponent_text + '_STRENGTH'
            opponent_zone = opponent_text + '_ZONE'
            opponentON = opponent_text + 'ON'
            opponent_lines = list(it.combinations(awayF_list, 3))

        ### add a loop for forward lines
        for t_line in team_lines:

            team_forward_1 = t_line[0]
            team_forward_1_lastname = team_forward_1.rsplit('.', 1)[1]
            
            team_forward_2 = t_line[1]
            team_forward_2_lastname = team_forward_2.rsplit('.', 1)[1]

            team_forward_3 = t_line[2]
            team_forward_3_lastname = team_forward_3.rsplit('.', 1)[1]

            team_line = team_forward_1 + '-' + team_forward_2 + '-' + team_forward_3
            team_line_lastname = team_forward_1_lastname + '-' + team_forward_2_lastname + '-' + team_forward_3_lastname

            ###
            ### TEAM LINE TIME ON ICE CHECK
            ###
            
            team_toi_5v5_first = (TOI_df[(TOI_df[team_strength] == '5v5') & 
                                    (TOI_df[teamON].str.contains(team_forward_1)) &
                                    (TOI_df[teamON].str.contains(team_forward_2)) &
                                    (TOI_df[teamON].str.contains(team_forward_3))].count()
                                    )
    
            team_toi_5v5 = round(team_toi_5v5_first[1] * 0.0166667, 1)

            if team_toi_5v5 < 2:
                continue   

           ### add another, final loop for forward lines
            for o_line in opponent_lines:

                opponent_forward_1 = o_line[0]
                opponent_forward_1_lastname = opponent_forward_1.rsplit('.', 1)[1]
                
                opponent_forward_2 = o_line[1]
                opponent_forward_2_lastname = opponent_forward_2.rsplit('.', 1)[1]
    
                opponent_forward_3 = o_line[2]
                opponent_forward_3_lastname = opponent_forward_3.rsplit('.', 1)[1]
    
                opponent_line = opponent_forward_1 + '-' + opponent_forward_2 + '-' + opponent_forward_3
                opponent_line_lastname = opponent_forward_1_lastname + '-' + opponent_forward_2_lastname + '-' + opponent_forward_3_lastname

                ###
                ### OPPONENT LINE TIME ON ICE CHECK
                ###
                
                opponent_toi_5v5_first = (TOI_df[(TOI_df[team_strength] == '5v5') & 
                                        (TOI_df[opponentON].str.contains(opponent_forward_1)) &
                                        (TOI_df[opponentON].str.contains(opponent_forward_2)) &
                                        (TOI_df[opponentON].str.contains(opponent_forward_3))].count()
                                        )
        
                opponent_toi_5v5 = round(opponent_toi_5v5_first[1] * 0.0166667, 1)
    
                if opponent_toi_5v5 < 2:
                    continue   
    
                ###
                ### TIME ON ICE
                ###
                
                toi_5v5_first = (TOI_df[(TOI_df[team_strength] == '5v5') & 
                                (TOI_df[teamON].str.contains(team_forward_1)) &
                                (TOI_df[teamON].str.contains(team_forward_2)) &
                                (TOI_df[teamON].str.contains(team_forward_3)) &
                                (TOI_df[opponentON].str.contains(opponent_forward_1)) &
                                (TOI_df[opponentON].str.contains(opponent_forward_2)) &
                                (TOI_df[opponentON].str.contains(opponent_forward_3))].count()
                                )
    
                toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)
    
                if toi_5v5 == 0:
                    continue   


                ###
                ### PLAY-BY-PLAY
                ###
                               
                ###
                ### INDIVIDUAL
                ###
    
                ### goals, assists and primary assists
                event = 'Goal'
                G_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df['PLAYER_A'] == team_forward_1) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df['PLAYER_A'] == team_forward_2) &
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df['PLAYER_A'] == team_forward_3) &
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]   
                        )
                    
                
                try:
                    A1_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                            (pbp_df['PLAYER_B'] == team_forward_1) &
                            (pbp_df[teamON].str.contains(team_forward_2)) &
                            (pbp_df[teamON].str.contains(team_forward_3)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +
    
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                            (pbp_df['PLAYER_B'] == team_forward_2) &
                            (pbp_df[teamON].str.contains(team_forward_1)) &
                            (pbp_df[teamON].str.contains(team_forward_3)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +
    
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                            (pbp_df['PLAYER_B'] == team_forward_3) &
                            (pbp_df[teamON].str.contains(team_forward_1)) &
                            (pbp_df[teamON].str.contains(team_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]   
                            )
                except:
                    A1_5v5 = 0
    
                try:
                    A2_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                            (pbp_df['PLAYER_C'] == team_forward_1) &
                            (pbp_df[teamON].str.contains(team_forward_2)) &
                            (pbp_df[teamON].str.contains(team_forward_3)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +
    
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                            (pbp_df['PLAYER_C'] == team_forward_2) &
                            (pbp_df[teamON].str.contains(team_forward_1)) &
                            (pbp_df[teamON].str.contains(team_forward_3)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +
    
                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                            (pbp_df['PLAYER_C'] == team_forward_3) &
                            (pbp_df[teamON].str.contains(team_forward_1)) &
                            (pbp_df[teamON].str.contains(team_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                            (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                            )
                except:
                    A2_5v5 = 0
    
                A_5v5 = A1_5v5 + A2_5v5
    
    
                ### points and primary points
                PTS_5v5 = G_5v5 + A_5v5
    
                PTS1_5v5 = G_5v5 + A1_5v5
    
    
                ### on-net (saved) shots
                event = 'Save'
                ONS_5v5 = G_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df['PLAYER_A'] == team_forward_1) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df['PLAYER_A'] == team_forward_2) &
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df['PLAYER_A'] == team_forward_3) &
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]   
                                    )
    
    
                ### unblocked shots
                event = 'Miss'
                US_5v5 = ONS_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df['PLAYER_A'] == team_forward_1) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df['PLAYER_A'] == team_forward_2) &
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df['PLAYER_A'] == team_forward_3) &
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]   
                                    )    
    
                ### shots
                event = 'Shot'
                S_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df['PLAYER_A'] == team_forward_1) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df['PLAYER_A'] == team_forward_2) &
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1] +

                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df['PLAYER_A'] == team_forward_3) &
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]   
                        )

    
                individual_5v5 = (G_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5)
    
    
                ###
                ### ON-ICE
                ###
    
                ### goals for and against
                event = 'Goal'              
                GF_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                        )

                GA_5v5 = (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                        )
                
                GD_5v5 = GF_5v5 - GA_5v5
    
    
                ### on-net (saved) shots for and against
                event = 'Save'               
                ONSF_5v5 = GF_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                                    )

                ONSA_5v5 = GA_5v5 + (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                                    )
                
                ONSD_5v5 = ONSF_5v5 - ONSA_5v5
    
    
                ### unblocked shots for and against
                event = 'Miss'
                
                USF_5v5 = ONSF_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                                    )

                USA_5v5 = ONSA_5v5 + (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') & 
                                    (pbp_df[teamON].str.contains(team_forward_1)) &
                                    (pbp_df[teamON].str.contains(team_forward_2)) &
                                    (pbp_df[teamON].str.contains(team_forward_3)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                                    )
    
                USD_5v5 = USF_5v5 - USA_5v5
    
    
                ### shots for and against
                event = 'Shot'
                SF_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                        )

                SA_5v5 = (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                        )
                
                SD_5v5 = SF_5v5 - SA_5v5


                ### faceoffs
                event = 'Faceoff'               
                FO_5v5 = (pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') & 
                        (pbp_df[teamON].str.contains(team_forward_1)) &
                        (pbp_df[teamON].str.contains(team_forward_2)) &
                        (pbp_df[teamON].str.contains(team_forward_3)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_1)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_2)) &
                        (pbp_df[opponentON].str.contains(opponent_forward_3))].count()[1]
                        )


                onice_5v5 = (GF_5v5, GA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, ONSD_5v5, USD_5v5, SD_5v5, FO_5v5)
    
    
                ### begin writing to file
                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'

                ### write out individual line matchup data
                individual_out.writerow((season_id, game_id, date, team_text, team, team_forward_1, team_forward_2, team_forward_3, team_line_lastname, opponent_forward_1, opponent_forward_2, opponent_forward_3, opponent_line_lastname, '5v5', '1', toi_5v5) + individual_5v5)
    
                print('Processing ' + team + ' individual stats for ' + team_line_lastname + ' against ' + opponent_line_lastname)
    
                ### write out on-ice line matchup data
                onice_out.writerow((season_id, game_id, date, team_text, team, team_forward_1, team_forward_2, team_forward_3, team_line_lastname, opponent_forward_1, opponent_forward_2, opponent_forward_3, opponent_line_lastname, '5v5', '1', toi_5v5) + onice_5v5)
    
                print('Processing ' + team + ' on-ice player stats for ' + team_line_lastname + ' against ' + opponent_line_lastname)

               
print('Finished generating line vs. line stats for ' + season_id + ' ' + game_id)