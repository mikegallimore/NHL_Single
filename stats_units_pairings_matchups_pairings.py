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
files_root = parameters.files_root

### establish file locations and destinations
TOI_matrix = files_root + 'TOI_matrix.csv'
pbp = files_root + 'pbp.csv'
stats_individual = files_root + 'stats_units_pairings_individual_matchups_pairings.csv'
stats_onice = files_root + 'stats_units_pairings_onice_matchups_pairings.csv'

### pull schedule info; generate key values
schedule_csv = files_root + season_id + "_schedule.csv"

schedule_df = pd.read_csv(schedule_csv)
schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]

date = schedule_date['DATE'].item()
home = schedule_date['HOME'].item()
away = schedule_date['AWAY'].item()
teams = [away, home]

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
    individual_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'DEFENDER_1', 'DEFENDER_2', 'PAIRING', 'OPPOSING_DEFENDER_1', 'OPPOSING_DEFENDER_2', 'MATCHUP', 'STATE', 'GP', 'TOI', 'G', 'A', '1_A', 'PTS', '1_PTS', 'ONS', 'US', 'S'])

    onice_out = csv.writer(players_onice)
    onice_out.writerow(['SEASON', 'GAME_ID', 'DATE', 'LOCATION', 'TEAM', 'DEFENDER_1', 'DEFENDER_2', 'PAIRING', 'OPPOSING_DEFENDER_1', 'OPPOSING_DEFENDER_2', 'MATCHUP', 'STATE', 'GP', 'TOI', 'GF', 'GA', 'ONSF', 'ONSA', 'USF', 'USA', 'SF', 'SA', 'GD', 'ONSD', 'USD', 'SD', 'FO'])

    ### access the game's roster file in order to create team-specific dicts and lists
    rosters_csv = files_root + 'rosters.csv'
    rosters_df = pd.read_csv(rosters_csv)
    rosters_table = rosters_df[['TEAM','PLAYER_NO', 'PLAYER_NAME', 'PLAYER_POS', 'PLAYER_POS_DETAIL']]

    homeROS_df = rosters_table.copy()
    homeROS_df = homeROS_df[(homeROS_df['TEAM'] == home)].sort_values(by=['PLAYER_NO'])
    homeD_df = homeROS_df[(homeROS_df['PLAYER_POS'] == 'D')]
    homeD_list = homeD_df['PLAYER_NAME'].tolist()

    awayROS_df = rosters_table.copy()
    awayROS_df = awayROS_df[(awayROS_df['TEAM'] == away)].sort_values(by=['PLAYER_NO'])
    awayD_df = awayROS_df[(awayROS_df['PLAYER_POS'] == 'D')]
    awayD_list = awayD_df['PLAYER_NAME'].tolist()
    
    ### begin looping by team
    for team in teams:

        if team == away:
            team_text = 'AWAY'
            team_state = team_text + '_STATE'
            team_strength = team_text + '_STRENGTH'
            team_zone = team_text + '_ZONE'
            teamON = team_text + 'ON'
            team_pairings = list(it.combinations(awayD_list, 2))
            opponent_text = 'HOME'
            opponent_state = opponent_text + '_STATE'
            opponent_strength = opponent_text + '_STRENGTH'
            opponent_zone = opponent_text + '_ZONE'
            opponentON = opponent_text + 'ON'
            opponent_pairings = list(it.combinations(homeD_list, 2))

        elif team == home:
            team_text = 'HOME'
            team_state = team_text + '_STATE'
            team_strength = team_text + '_STRENGTH'
            team_zone = team_text + '_ZONE'
            teamON = team_text + 'ON'
            team_pairings = list(it.combinations(homeD_list, 2))
            opponent_text = 'AWAY'
            opponent_state = opponent_text + '_STATE'
            opponent_strength = opponent_text + '_STRENGTH'
            opponent_zone = opponent_text + '_ZONE'
            opponentON = opponent_text + 'ON'
            opponent_pairings = list(it.combinations(awayD_list, 2))

        ### add a loop for defense pairs
        for t_pairing in team_pairings:

            team_defender_1 = t_pairing[0]
            team_defender_1_lastname = team_defender_1.rsplit('.', 1)[1]

            team_defender_2 = t_pairing[1]
            team_defender_2_lastname = team_defender_2.rsplit('.', 1)[1]

            team_pair = team_defender_1 + '-' + team_defender_2
            team_pair_lastname = team_defender_1_lastname + '-' + team_defender_2_lastname

            ###
            ### TEAM LINE TIME ON ICE CHECK
            ###

            team_toi_5v5_first = (TOI_df[(TOI_df[team_strength] == '5v5') &
                                    (TOI_df[teamON].str.contains(team_defender_1)) &
                                    (TOI_df[teamON].str.contains(team_defender_2))].count()
                                    )

            team_toi_5v5 = round(team_toi_5v5_first[1] * 0.0166667, 1)

            if team_toi_5v5 < 2:
                continue

            ### add another, final loop for defense pairs
            for o_pairing in opponent_pairings:

                opponent_defender_1 = o_pairing[0]
                opponent_defender_1_lastname = opponent_defender_1.rsplit('.', 1)[1]

                opponent_defender_2 = o_pairing[1]
                opponent_defender_2_lastname = opponent_defender_2.rsplit('.', 1)[1]

                opponent_pair = opponent_defender_1 + '-' + opponent_defender_2
                opponent_pair_lastname = opponent_defender_1_lastname + '-' + opponent_defender_2_lastname

                ###
                ### OPPONENT LINE TIME ON ICE CHECK
                ###

                opponent_toi_5v5_first = (TOI_df[(TOI_df[team_strength] == '5v5') &
                                        (TOI_df[opponentON].str.contains(opponent_defender_1)) &
                                        (TOI_df[opponentON].str.contains(opponent_defender_2))].count()
                                        )

                opponent_toi_5v5 = round(opponent_toi_5v5_first[1] * 0.0166667, 1)

                if opponent_toi_5v5 < 2:
                    continue

                ###
                ### TIME ON ICE
                ###

                toi_5v5_first = (TOI_df[(TOI_df[team_strength] == '5v5') &
                                (TOI_df[teamON].str.contains(team_defender_1)) &
                                (TOI_df[teamON].str.contains(team_defender_2)) &
                                (TOI_df[opponentON].str.contains(opponent_defender_1)) &
                                (TOI_df[opponentON].str.contains(opponent_defender_2))].count()
                                )

                toi_5v5 = round(toi_5v5_first[1] * 0.0166667, 1)

                if toi_5v5 < 1:
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
                        (pbp_df['PLAYER_A'] == team_defender_1) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1] +

                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df['PLAYER_A'] == team_defender_2) &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )


                try:
                    A1_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                            (pbp_df['PLAYER_B'] == team_defender_1) &
                            (pbp_df[teamON].str.contains(team_defender_2)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1] +

                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                            (pbp_df['PLAYER_B'] == team_defender_2) &
                            (pbp_df[teamON].str.contains(team_defender_1)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                            )
                except:
                    A1_5v5 = 0

                try:
                    A2_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                            (pbp_df['PLAYER_C'] == team_defender_1) &
                            (pbp_df[teamON].str.contains(team_defender_2)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1] +

                            pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                            (pbp_df['PLAYER_C'] == team_defender_2) &
                            (pbp_df[teamON].str.contains(team_defender_1)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                            (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
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
                                    (pbp_df['PLAYER_A'] == team_defender_1) &
                                    (pbp_df[teamON].str.contains(team_defender_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1] +

                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df['PLAYER_A'] == team_defender_2) &
                                    (pbp_df[teamON].str.contains(team_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                                    )

                ### unblocked shots
                event = 'Miss'
                US_5v5 = ONS_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df['PLAYER_A'] == team_defender_1) &
                                    (pbp_df[teamON].str.contains(team_defender_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1] +

                                    pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df['PLAYER_A'] == team_defender_2) &
                                    (pbp_df[teamON].str.contains(team_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                                    )

                ### shots
                event = 'Shot'
                S_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df['PLAYER_A'] == team_defender_1) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1] +

                        pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df['PLAYER_A'] == team_defender_2) &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )


                individual_5v5 = (G_5v5, A_5v5, A1_5v5, PTS_5v5, PTS1_5v5, ONS_5v5, US_5v5, S_5v5)


                ###
                ### ON-ICE
                ###

                ### goals for and against
                event = 'Goal'
                GF_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )

                GA_5v5 = (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )

                GD_5v5 = GF_5v5 - GA_5v5


                ### on-net (saved) shots for and against
                event = 'Save'
                ONSF_5v5 = GF_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df[teamON].str.contains(team_defender_1)) &
                                    (pbp_df[teamON].str.contains(team_defender_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                                    )

                ONSA_5v5 = GA_5v5 + (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df[teamON].str.contains(team_defender_1)) &
                                    (pbp_df[teamON].str.contains(team_defender_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                                    )

                ONSD_5v5 = ONSF_5v5 - ONSA_5v5


                ### unblocked shots for and against
                event = 'Miss'

                USF_5v5 = ONSF_5v5 + (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df[teamON].str.contains(team_defender_1)) &
                                    (pbp_df[teamON].str.contains(team_defender_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                                    )

                USA_5v5 = ONSA_5v5 + (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT_TYPE'] == event) & (pbp_df[team_strength] == '5v5') &
                                    (pbp_df[teamON].str.contains(team_defender_1)) &
                                    (pbp_df[teamON].str.contains(team_defender_2)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                                    (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                                    )

                USD_5v5 = USF_5v5 - USA_5v5


                ### shots for and against
                event = 'Shot'
                SF_5v5 = (pbp_df[(pbp_df['TEAM'] == team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )

                SA_5v5 = (pbp_df[(pbp_df['TEAM'] != team) & (pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )

                SD_5v5 = SF_5v5 - SA_5v5


                ### faceoffs
                event = 'Faceoff'
                FO_5v5 = (pbp_df[(pbp_df['EVENT'] == event) & (pbp_df[team_strength] == '5v5') &
                        (pbp_df[teamON].str.contains(team_defender_1)) &
                        (pbp_df[teamON].str.contains(team_defender_2)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_1)) &
                        (pbp_df[opponentON].str.contains(opponent_defender_2))].count()[1]
                        )


                onice_5v5 = (GF_5v5, GA_5v5, ONSF_5v5, ONSA_5v5, USF_5v5, USA_5v5, SF_5v5, SA_5v5, GD_5v5, ONSD_5v5, USD_5v5, SD_5v5, FO_5v5)


                ### begin writing to file
                if team == away:
                    team_text = 'Away'
                elif team == home:
                    team_text = 'Home'

                ### write out individual pairing matchup data
                individual_out.writerow((season_id, game_id, date, team_text, team, team_defender_1, team_defender_2, team_pair_lastname, opponent_defender_1, opponent_defender_2, opponent_pair_lastname, '5v5', '1', toi_5v5) + individual_5v5)

                print('Processing ' + team + ' individual stats for ' + team_pair_lastname + ' against ' + opponent_pair_lastname)

                ### write out on-ice pairing matchup data
                onice_out.writerow((season_id, game_id, date, team_text, team, team_defender_1, team_defender_2, team_pair_lastname, opponent_defender_1, opponent_defender_2, opponent_pair_lastname, '5v5', '1', toi_5v5) + onice_5v5)

                print('Processing ' + team + ' on-ice player stats for ' + team_pair_lastname + ' against ' + opponent_pair_lastname)


print('Finished generating pairing vs. pairing stats for ' + season_id + ' ' + game_id)