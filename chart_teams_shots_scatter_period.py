# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import parameters
import dict_team_colors
import mod_switch_colors

def parse_ids(season_id, game_id, images):

    # pull common variables from the parameters file
    charts_teams_period = parameters.charts_teams_period
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    # create variables that point to the .csv processed teams stats file and play-by-play file
    stats_teams_file = files_root + 'stats_teams_period.csv'
    pbp_file = files_root + 'pbp.csv'
    
    # create a dataframe object that reads in the team stats info
    stats_teams_df = pd.read_csv(stats_teams_file)
    
    # create a dataframe object that reads in the shots with expected goals info
    pbp_df = pd.read_csv(pbp_file)
    pbp_df['xG'] = round(pbp_df.xG.astype(float) * 100, 2)
    if int(season_id) >= 20102011:
        pbp_df['X_1'] *= -1
        pbp_df['Y_1'] *= -1

    # choose colors for each team and the legend; set them in a list
    legend_color = 'black'

    away_color = dict_team_colors.team_color_1st[away]
    home_color = dict_team_colors.team_color_1st[home]

    # change one team's color from its primary option to, depending on the opponent, either a second, third or fourth option
    try:
        away_color = mod_switch_colors.switch_team_colors(away, home)[0]
        home_color = mod_switch_colors.switch_team_colors(away, home)[1]
    except:
        pass   
    
    colors = [away_color, home_color, legend_color]

    periods = [1, 2, 3, 4]

    for period in periods:       

        if period == 1:
            period_name = '1st'

        if period == 2:
            period_name = '2nd'

        if period == 3:
            period_name = '3rd'

        if period >= 4:
            period_name = 'OT'
        
        states = ['ALL', '5v5', 'PP', 'SH']
        
        for state in states:
           
            # pull the time on ice recorded for the home team from the team stats file
            if state == 'ALL':
                try:
                    toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['PERIOD'] == period_name)]
                    toi = toi_df['TOI'].item()
                except:
                    toi = 0.0

            if state == '5v5' and period < 4 or state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:
                try:
                    toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['PERIOD'] == period_name)]
                    toi = toi_df['TOI'].item()
                except:
                    toi = 0.0

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                try:
                    toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '4v4') & (stats_teams_df['PERIOD'] == period_name)]
                    toi = toi_df['TOI'].item()
                except:
                    toi = 0.0

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                try:
                    toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '3v3') & (stats_teams_df['PERIOD'] == period_name)]
                    toi = toi_df['TOI'].item()
                except:
                    toi = 0.0

            if state == 'PP':
                try:
                    toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['PERIOD'] == period_name)]
                    toi = toi_df['TOI'].item()
                except:
                    toi = 0.0

            if state == 'SH':
                try:
                    toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['PERIOD'] == period_name)]
                    toi = toi_df['TOI'].item()
                except:
                    toi = 0.0
            
            # get a count of the number of unblocked shots and goals for each team
            if state == 'ALL':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)].count()[1])

            if state == '5v5' and period < 4:
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')].count()[1])

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')].count()[1])

            if state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:           
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])

            if state == 'PP':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')].count()[1])

            if state == 'SH':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
                away_G_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
                home_G_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
        
            # get the sum xG value of unblocked shots for each team
            if state == 'ALL':
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))

            if state == '5v5' and period < 4:           
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))

            if state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:           
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))

            if state == 'PP':
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))

            if state == 'SH':
                away_xG = str(round((np.where((pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                home_xG = str(round((np.where((pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP'), pbp_df['xG'], 0).sum(), 1)[0] / 100, 2))
                    
            # create subsets of the distinct types of unblocked shots for each team from the play-by-play file  
            if state == 'ALL':
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]

            if state == '5v5' and period < 4:           
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '4v4') & (pbp_df['AWAY_STRENGTH'] == '4v4')]

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STRENGTH'] == '3v3') & (pbp_df['AWAY_STRENGTH'] == '3v3')]

            if state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:           
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] >= period) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

            if state == 'PP':
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]

            if state == 'SH':
                away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
                away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
                away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]

                home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
                home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
                home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
      
            # create lists of the expected goals values for each type of unblocked shot
            away_scored_list = away_df_scored['xG'].tolist()
            away_saved_list = away_df_saved['xG'].tolist()
            away_missed_list = away_df_missed['xG'].tolist()
         
            home_scored_list = home_df_scored['xG'].tolist()
            home_saved_list = home_df_saved['xG'].tolist()
            home_missed_list = home_df_missed['xG'].tolist()   
            
            # create a figure to plot
            fig, ax = plt.subplots(figsize=(8,6))
                
            # plot the distinct types of unblocked shot events for each team in order to create labels
            teams_df_scored = pd.concat([away_df_scored, home_df_scored])
            teams_df_saved = pd.concat([away_df_saved, home_df_saved])
            teams_df_missed = pd.concat([away_df_missed, home_df_missed])
        
            try:
                scored_marker = teams_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='D', s=60, c='None', edgecolors='black', linewidth=2, alpha=1, label='Scored', ax=ax);
            except:
                pass
            try:
                saved_marker = teams_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=40, c='None', edgecolors='black', linewidth=1, alpha=1, label='Saved', ax=ax);
            except:
                pass
            try:
                missed_marker = teams_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c='black', edgecolors='None', alpha=1, label='Missed', ax=ax);
            except:
                pass
            
            # plot the distinct types of unblocked shot events for each team 
            try:
                away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker='D', s=[5*i for i in away_scored_list], c='None', edgecolors=colors[0], linewidth=2, alpha=1, ax=ax);
            except:
                pass
            try:
                away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=[5*i for i in away_saved_list], c='None', edgecolors=colors[0], linewidth=1, alpha=0.5, ax=ax);
            except:
                pass
            try:
                away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=[5*i for i in away_missed_list], c=colors[0], edgecolors='None', alpha=0.5, ax=ax);
            except:
                pass
               
            try:
                home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker='D', s=[5*i for i in home_scored_list], c='None', edgecolors=colors[1], linewidth=2, alpha=1, ax=ax);
            except:
                pass
            try:
                home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=[5*i for i in home_saved_list], c='None', edgecolors=colors[1], linewidth=1, alpha=0.5, ax=ax);
            except:
                pass
            try:
                home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=[5*i for i in home_missed_list], c=colors[1], edgecolors='none', alpha=0.5, ax=ax);
            except:
                pass
            
            # set the background image of what will be the plot to the 'rink_image.png' file
            rink_img = plt.imread("rink_image.png")
            plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
            
            # eliminate the axis labels
            plt.axis('off')
            
            # add text boxes to indicate home and away sides
            plt.text(58, 45, home_count + ' USF\n' + home_xG + ' xGF, ' + home_G_count + ' GF', color=colors[1], fontsize=12, ha='center')
            plt.text(-58, 45, away_count + ' USF\n' + away_xG + ' xGF, ' + away_G_count + ' GF', color=colors[0], fontsize=12, ha='center')
        
            # set the plot title
            if state == 'ALL':
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' Minutes\n\n')

            if state == '5v5' and period < 4:           
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' 5v5 Minutes\n\n')

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' 4v4 Minutes\n\n')

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' 3v3 Minutes\n\n')

            if state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:           
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' 5v5 Minutes\n\n')

            if state == 'PP':
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' Home PP Minutes\n\n')

            if state == 'SH':
                plt.title(date + ' ' + period_name + ' Period Unblocked Shots\n' + str(toi) + ' Away PP Minutes\n\n')
            
            # set the location of the plot legend
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
        
            # add text boxes with team names in white and with the team's color in the background  
            fig.text(.435, 0.744, ' ' + away + ' ', fontsize='12', color='white', bbox=dict(facecolor=away_color, edgecolor='None'))
            fig.text(.535, 0.744, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
            fig.text(.501, 0.744, '@', fontsize='12', color='black', bbox=dict(facecolor='white', edgecolor='None'))
            
            # eliminate unnecessary whitespace
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            
            
            ###
            ### SAVE TO FILE
            ###
            
            if state == 'ALL':           
                plt.savefig(charts_teams_period + 'shots_scatter_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)

            if state == '5v5' and period < 4 or state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:
                plt.savefig(charts_teams_period + 'shots_scatter_5v5_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                plt.savefig(charts_teams_period + 'shots_scatter_4v4_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)                

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                plt.savefig(charts_teams_period + 'shots_scatter_3v3_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)                

            if state == 'PP':
                plt.savefig(charts_teams_period + 'shots_scatter_pp_home_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)

            if state == 'SH':
                plt.savefig(charts_teams_period + 'shots_scatter_pp_away_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)

            # exercise a command-line option to show the current figure
            if images == 'show':
                plt.show()
            
            
            ###
            ### CLOSE
            ###
            
            plt.close(fig)
            
            # status update
            if state == 'ALL':
                print('Finished scatter plot for all ' + period_name + ' period unblocked shots.')              

            if state == '5v5' and period < 4 or state == '5v5' and int(season_id) != 20192020 and period == 4 and int(game_id) >= 30000 or state == '5v5' and int(season_id) == 20192020 and period == 4 and int(game_id) >= 30021:
                print('Finished scatter plot for ' + period_name + ' period unblocked 5v5 shots.')            

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                print('Finished scatter plot for ' + period_name + ' period unblocked 4v4 shots.')            

            if state == '5v5' and period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016 or state == '5v5' and season_id == 20192020 and period == 4 and int(game_id) > 30000 and int(game_id) <= 30020:
                print('Finished scatter plot for ' + period_name + ' period unblocked 3v3 shots.')  

            if state == 'PP':
                print('Finished scatter plot for all ' + period_name + ' period unblocked shots during a home PP.')

            if state == 'SH':
                print('Finished scatter plot for all ' + period_name + ' period unblocked shots during an away PP.')