# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parameters
import dict_team_colors
import mod_switch_colors

def parse_ids(season_id, game_id, images):

    # pull common variables from the parameters file
    charts_players_individual_period = parameters.charts_players_individual_period
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    # create variables that point to the .csv processed stats files for the team and players
    team_file = files_root + 'stats_teams_period.csv'
    players_file = files_root + 'stats_players_individual_period.csv'
    
    # create dataframe objects that read in info from the .csv files
    team_stats_df = pd.read_csv(team_file)
    players_df = pd.read_csv(players_file)
    
    # choose colors for each team; set them in a list; generate a custom colormap for each team
    away_color = dict_team_colors.team_color_1st[away]
    home_color = dict_team_colors.team_color_1st[home]
 
    # change one team's color from its primary option to, depending on the opponent, either a second, third or fourth option
    try:
        away_color = mod_switch_colors.switch_team_colors(away, home)[0]
        home_color = mod_switch_colors.switch_team_colors(away, home)[1]
    except:
        pass
    
    team_colors = [away_color, home_color]


    ###
    ### 5v5 (3v3 in Regulation OT), PP, SH
    ###

    periods = [1, 2, 3, 4]

    # loop through each period
    for period in periods:

        if period == 1:
            period_name = '1st'

        if period == 2:
            period_name = '2nd'

        if period == 3:
            period_name = '3rd'

        if period == 4:
            period_name = 'OT'

        skaters_PP_df = players_df.copy()
        skaters_PP_df = skaters_PP_df[(skaters_PP_df['STATE'] == 'PP') & (skaters_PP_df['PERIOD'] == period_name) & (skaters_PP_df['POS'] != 'G')]
        max_PP_toi = skaters_PP_df['TOI'].max()

        skaters_SH_df = players_df.copy()
        skaters_SH_df = skaters_SH_df[(skaters_SH_df['STATE'] == 'SH') & (skaters_SH_df['PERIOD'] == period_name) & (skaters_PP_df['POS'] != 'G')]
        max_SH_toi = skaters_SH_df['TOI'].max()
        
        # loop through each team
        for team in teams:
            
            if team == away:
                team_color = team_colors[0]
        
            if team == home:
                team_color = team_colors[1]
                
            # create a dataframe from the team stats file for generating toi values for the different game states
            team_toi_df = team_stats_df.copy()

            team_all_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == 'ALL') & (team_toi_df['PERIOD'] == period_name)]
            team_all_toi = team_all_toi['TOI'].item()

            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                        
                team_5v5_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == '5v5') & (team_toi_df['PERIOD'] == period_name)]
                team_5v5_toi = team_5v5_toi['TOI'].item()

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                team_4v4_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == '4v4') & (team_toi_df['PERIOD'] == period_name)]
                team_4v4_toi = team_4v4_toi['TOI'].item()

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                team_3v3_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == '3v3') & (team_toi_df['PERIOD'] == period_name)]
                team_3v3_toi = team_3v3_toi['TOI'].item()

            team_PP_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == 'PP') & (team_toi_df['PERIOD'] == period_name)]
            team_PP_toi = team_PP_toi['TOI'].item()

            team_SH_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == 'SH') & (team_toi_df['PERIOD'] == period_name)]
            team_SH_toi = team_SH_toi['TOI'].item()

            # create a dataframe; filter for team; sort by team, game state and position; rank by time on ice and then invert the rankings
            team_df = players_df.copy()
            team_df = team_df[(team_df['TEAM'] == team) & (team_df['POS'] != 'G') & (team_df['PERIOD'] == period_name)]
    
            # create columns for saved, missed and blocked shots; remove zeros from all the columns intended for plotting
            team_df['SS'] = team_df['ONS'] - team_df['G']
            team_df['MS'] = team_df['US'] - team_df['ONS']
            team_df['BS'] = team_df['S'] - team_df['US']
            
            team_df['G'] = team_df['G'].replace(0, np.NaN)
            team_df['SS'] = team_df['SS'].replace(0, np.NaN)
            team_df['MS'] = team_df['MS'].replace(0, np.NaN)
            team_df['BS'] = team_df['BS'].replace(0, np.NaN)

            # create a filtered dataframe for each game state; sort by team, game state and position; rank by time on ice and then invert the rankings
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                   
                team_5v5_df = team_df.copy()
                team_5v5_df = team_5v5_df[(team_5v5_df['STATE'] == '5v5')]
                team_5v5_df = team_5v5_df.sort_values(by=['TOI'], ascending = True)
                team_5v5_df['RANK'] = team_5v5_df['TOI'].rank(method='first')
                team_5v5_df['RANK'] -= 1

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                team_4v4_df = team_df.copy()
                team_4v4_df = team_4v4_df[(team_4v4_df['STATE'] == '4v4')]
                team_4v4_df = team_4v4_df.sort_values(by=['TOI'], ascending = True)
                team_4v4_df['RANK'] = team_4v4_df['TOI'].rank(method='first')
                team_4v4_df['RANK'] -= 1

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                team_3v3_df = team_df.copy()
                team_3v3_df = team_3v3_df[(team_3v3_df['STATE'] == '3v3')]
                team_3v3_df = team_3v3_df.sort_values(by=['TOI'], ascending = True)
                team_3v3_df['RANK'] = team_3v3_df['TOI'].rank(method='first')
                team_3v3_df['RANK'] -= 1
            
            team_PP_df = team_df.copy()
            team_PP_df = team_PP_df[(team_PP_df['STATE'] == 'PP') & team_PP_df['TOI'] > 0]
            team_PP_df = team_PP_df.sort_values(by=['TOI'], ascending = True)
            team_PP_df = team_PP_df.iloc[-10:]  
            team_PP_df['RANK'] = team_PP_df['TOI'].rank(method='first')
            team_PP_df['RANK'] -= 1
    
            team_SH_df = team_df.copy()
            team_SH_df = team_SH_df[(team_SH_df['STATE'] == 'SH') & team_SH_df['TOI'] > 0]
            team_SH_df = team_SH_df.sort_values(by=['TOI'], ascending = True)
            team_SH_df = team_SH_df.iloc[-10:]  
            team_SH_df['RANK'] = team_SH_df['TOI'].rank(method='first')
            team_SH_df['RANK'] -= 1
    
            # for each game state, create a dataframe with just the time on ice column; set a max value; scale each player's time on ice relative to the max
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                   
                toi_5v5 = team_5v5_df['TOI']        
                max_toi_5v5 = toi_5v5.max()

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                toi_4v4 = team_4v4_df['TOI']        
                max_toi_4v4 = toi_4v4.max()

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                toi_3v3 = team_3v3_df['TOI']        
                max_toi_3v3 = toi_3v3.max()
            
            toi_PP = team_PP_df['TOI']
            max_toi_PP = toi_PP.max()
    
            toi_SH = team_SH_df['TOI']    
            max_toi_SH = toi_SH.max()
            
            # create a figure with six subplots arrangled complexly using a grid structure
            fig = plt.figure(figsize=(8,8))
            grid = plt.GridSpec(5, 8,  hspace=0.75, wspace=0.75)

            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                   
                ax_5v5_shots = fig.add_subplot(grid[0:-2, :-1])
                ax_5v5_toi = fig.add_subplot(grid[0:-2, 7])        

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots = fig.add_subplot(grid[0:-2, :-1])
                ax_4v4_toi = fig.add_subplot(grid[0:-2, 7]) 

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots = fig.add_subplot(grid[0:-2, :-1])
                ax_3v3_toi = fig.add_subplot(grid[0:-2, 7])        
    
            ax_PP_shots = fig.add_subplot(grid[3:, :2])
            ax_PP_toi = fig.add_subplot(grid[3:, 2]) 
    
            ax_SH_shots = fig.add_subplot(grid[3:, 5:-1])
            ax_SH_toi = fig.add_subplot(grid[3:, 7]) 
            
            # set the plot title
            fig.suptitle(date + ' Skaters Individual Shots (' + period_name + ' Period)\n\n')       
    
            # set the axes titles
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.set_title('5v5 S', fontsize=10)
                ax_5v5_toi.set_title('5v5 TOI', fontsize=10)

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20152016:
                ax_4v4_shots.set_title('4v4 S', fontsize=10)
                ax_4v4_toi.set_title('4v4 TOI', fontsize=10)

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.set_title('3v3 S', fontsize=10)
                ax_3v3_toi.set_title('3v3 TOI', fontsize=10)

            ax_PP_shots.set_title('PP S', fontsize=10)
            ax_PP_toi.set_title('PP TOI', fontsize=10)

            ax_SH_shots.set_title('SH S', fontsize=10)
            ax_SH_toi.set_title('SH TOI', fontsize=10)
            
            # create markers for the plot legend
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                try:
                    G_marker = team_5v5_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, legend='Scored', label='Scored', ax=ax_5v5_shots);
                except:
                    pass   
                try:
                    SS_marker = team_5v5_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, legend='Saved', label='Saved', ax=ax_5v5_shots);
                except:
                    pass 
                try:
                    MS_marker = team_5v5_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='black', linewidth=0, alpha=1, legend='Missed', label='Missed', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    BS_marker = team_5v5_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='black', linewidth=0, alpha=1, legend='Blocked', label='Blocked', ax=ax_5v5_shots);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20142015:
                try:
                    G_marker = team_4v4_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, legend='Scored', label='Scored', ax=ax_4v4_shots);
                except:
                    pass   
                try:
                    SS_marker = team_4v4_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, legend='Saved', label='Saved', ax=ax_4v4_shots);
                except:
                    pass 
                try:
                    MS_marker = team_4v4_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='black', linewidth=0, alpha=1, legend='Missed', label='Missed', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    BS_marker = team_4v4_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='black', linewidth=0, alpha=1, legend='Blocked', label='Blocked', ax=ax_4v4_shots);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                try:
                    G_marker = team_3v3_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, legend='Scored', label='Scored', ax=ax_3v3_shots);
                except:
                    pass   
                try:
                    SS_marker = team_3v3_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, legend='Saved', label='Saved', ax=ax_3v3_shots);
                except:
                    pass 
                try:
                    MS_marker = team_3v3_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='black', linewidth=0, alpha=1, legend='Missed', label='Missed', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    BS_marker = team_3v3_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='black', linewidth=0, alpha=1, legend='Blocked', label='Blocked', ax=ax_3v3_shots);
                except:
                    pass

            # for each state, plot the bars for total shots and markers for saved, missed and blocked shots markers
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                try:
                    S_5v5_plot = team_5v5_df.plot.barh(x='PLAYER', y='S', color=team_color, edgecolor=None, width=0.75, legend=None, label='', ax=ax_5v5_shots);
                except:
                    pass 
                try:
                    G_5v5_marker = team_5v5_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    SS_5v5_marker = team_5v5_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    MS_5v5_marker = team_5v5_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    BS_5v5_marker = team_5v5_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                try:
                    S_4v4_plot = team_4v4_df.plot.barh(x='PLAYER', y='S', color=team_color, edgecolor=None, width=0.75, legend=None, label='', ax=ax_4v4_shots);
                except:
                    pass 
                try:
                    G_4v4_marker = team_4v4_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    SS_4v4_marker = team_4v4_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    MS_4v4_marker = team_4v4_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    BS_4v4_marker = team_4v4_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                try:
                    S_3v3_plot = team_3v3_df.plot.barh(x='PLAYER', y='S', color=team_color, edgecolor=None, width=0.75, legend=None, label='', ax=ax_3v3_shots);
                except:
                    pass 
                try:
                    G_3v3_marker = team_3v3_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    SS_3v3_marker = team_3v3_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    MS_3v3_marker = team_3v3_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    BS_3v3_marker = team_3v3_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass

            if team_PP_toi != 0:
                try:
                    S_PP_plot = team_PP_df.plot.barh(x='PLAYER', y='S', color=team_color, edgecolor=None, width=0.75, legend=None, label='', ax=ax_PP_shots);
                except:
                    pass 
                try:
                    G_PP_marker = team_PP_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass   
                try:
                    SS_PP_marker = team_PP_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass 
                try:
                    MS_PP_marker = team_PP_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass
                try:
                    BS_PP_marker = team_PP_df.plot(x='BS', y='RANK', marker='_', markersize=13, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass

            if team_SH_toi != 0:    
                try:
                    S_SH_plot = team_SH_df.plot.barh(x='PLAYER', y='S', color=team_color, edgecolor=None, width=0.75, legend=None, label='', ax=ax_SH_shots);
                except:
                    pass 
                try:
                    G_SH_marker = team_SH_df.plot(x='G', y='RANK', marker='D', markersize=11, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
                except:
                    pass   
                try:
                    SS_SH_marker = team_SH_df.plot(x='SS', y='RANK', marker='o', markersize=7, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
                except:
                    pass 
                try:
                    MS_SH_marker = team_SH_df.plot(x='MS', y='RANK', marker='x', markersize=7, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
                except:
                    pass
                try:
                    BS_SH_marker = team_SH_df.plot(x='BS', y='RANK', marker='_', markersize=11, markeredgewidth=1, color='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
                except:
                    pass
    
            # for each state, plot the bars for time on ice
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                try:
                    toi_5v5_plot = team_5v5_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_5v5_toi);
                except:
                    pass 

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                try:
                    toi_4v4_plot = team_4v4_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_4v4_toi);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                try:
                    toi_3v3_plot = team_3v3_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_3v3_toi);
                except:
                    pass 

            if team_PP_toi != 0:
                try:
                    toi_PP_plot = team_PP_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_PP_toi);
                except:
                    pass

            if team_SH_toi != 0:            
                try:
                    toi_SH_plot = team_SH_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_SH_toi);
                except:
                    pass
    
            # set / remove the y-labels for the subplots
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.set_xlabel('')
                ax_5v5_shots.set_ylabel('', fontsize=10)
                ax_5v5_toi.set_xlabel('')
                ax_5v5_toi.set_ylabel('')

            if period == 4 and int(game_id) < 30000:
                ax_3v3_shots.set_xlabel('')
                ax_3v3_shots.set_ylabel('', fontsize=10)
                ax_3v3_toi.set_xlabel('')
                ax_3v3_toi.set_ylabel('')
        
            ax_PP_shots.set_xlabel('')
            ax_PP_shots.set_ylabel('', fontsize=10)
            ax_PP_toi.set_xlabel('')
            ax_PP_toi.set_ylabel('')
    
            ax_SH_shots.set_xlabel('')
            ax_SH_shots.set_ylabel('', fontsize=10)
            ax_SH_toi.set_xlabel('')
            ax_SH_toi.set_ylabel('')
               
            # change the tick parameters for each axes
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.tick_params(
                    axis='both',       # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,        # ticks along the left edge are off
                    labelbottom=True)  # labels along the bottom edge are on
                ax_5v5_toi.tick_params(
                    axis='both',       # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,        # ticks along the left edge are off
                    labelleft=False,   # labels along the left edge are off
                    labelbottom=True)  # labels along the bottom edge are on

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.tick_params(
                    axis='both',       # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,        # ticks along the left edge are off
                    labelbottom=True)  # labels along the bottom edge are on
                ax_4v4_toi.tick_params(
                    axis='both',       # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,        # ticks along the left edge are off
                    labelleft=False,   # labels along the left edge are off
                    labelbottom=True)  # labels along the bottom edge are on

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.tick_params(
                    axis='both',       # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,        # ticks along the left edge are off
                    labelbottom=True)  # labels along the bottom edge are on
                ax_3v3_toi.tick_params(
                    axis='both',       # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    left=False,        # ticks along the left edge are off
                    labelleft=False,   # labels along the left edge are off
                    labelbottom=True)  # labels along the bottom edge are on

            ax_PP_shots.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=True)  # labels along the bottom edge are on
            ax_PP_toi.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelleft=False,   # labels along the left edge are off            
                labelbottom=True)  # labels along the bottom edge are on
    
            ax_SH_shots.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=True)  # labels along the bottom edge are on
            ax_SH_toi.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelleft=False,   # labels along the left edge are off
                labelbottom=True)  # labels along the bottom edge are on

            # change the y-axis label colors
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.tick_params(
                        axis='y',
                        which='both',
                        labelcolor=team_color)
        
            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.tick_params(
                        axis='y',
                        which='both',
                        labelcolor=team_color)
        
            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.tick_params(
                        axis='y',
                        which='both',
                        labelcolor=team_color)      
   
            ax_PP_shots.tick_params(
                    axis='y',
                    which='both',
                    labelcolor=team_color)
       
            ax_SH_shots.tick_params(
                    axis='y',
                    which='both',
                    labelcolor=team_color)
        
            # create a list of x-axis tick values contingent on the max values for shots
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                S_5v5_max = team_5v5_df['S']
                S_5v5_tickmax = S_5v5_max.max()
    
                S_5v5_ticklabels = []
                if S_5v5_tickmax <= 10:
                    S_5v5_ticklabels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                if S_5v5_tickmax > 10 and S_5v5_tickmax <= 20:
                    S_5v5_ticklabels = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        
                toi_5v5_ticklabels = [0, 20]
        
            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                S_4v4_max = team_4v4_df['S']
                S_4v4_tickmax = S_4v4_max.max()
    
                S_4v4_ticklabels = []
                if S_4v4_tickmax <= 10:
                    S_4v4_ticklabels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                if S_4v4_tickmax > 10 and S_4v4_tickmax <= 20:
                    S_4v4_ticklabels = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        
                toi_4v4_ticklabels = [0, 5]
                
            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                S_3v3_max = team_3v3_df['S']
                S_3v3_tickmax = S_3v3_max.max()
    
                S_3v3_ticklabels = []
                if S_3v3_tickmax <= 10:
                    S_3v3_ticklabels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                if S_3v3_tickmax > 10 and S_3v3_tickmax <= 20:
                    S_3v3_ticklabels = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        
                toi_3v3_ticklabels = [0, 5]
                       
            S_PP_max = team_PP_df['S']
            S_PP_tickmax = S_PP_max.max()
    
            S_PP_ticklabels = []
            if S_PP_tickmax <= 5:
                S_PP_ticklabels = [0, 1, 2, 3, 4, 5]
            if S_PP_tickmax > 5 and S_PP_tickmax <= 10:
                S_PP_ticklabels = [0, 2, 4, 6, 8, 10]
            if S_PP_tickmax > 10 and S_PP_tickmax <= 15:
                S_PP_ticklabels = [0, 3, 6, 9, 12, 15]
    
            S_SH_max = team_SH_df['S']
            S_SH_tickmax = S_SH_max.max()
    
            S_SH_ticklabels = []
            if S_SH_tickmax <= 5:
                S_SH_ticklabels = [0, 1, 2, 3, 4, 5]
            if S_SH_tickmax > 5 and S_SH_tickmax <= 10:
                S_SH_ticklabels = [0, 2, 4, 6, 8, 10]
            if S_SH_tickmax > 10 and S_SH_tickmax <= 15:
                S_SH_ticklabels = [0, 3, 6, 9, 12, 15]
    
            toi_PP_tickmax = max_PP_toi
    
            toi_SH_tickmax = max_SH_toi
    
            toi_specialteams_tickmax = float()
            if toi_PP_tickmax >= toi_SH_tickmax:
                toi_specialteams_tickmax = toi_PP_tickmax
            if toi_PP_tickmax < toi_SH_tickmax:
                toi_specialteams_tickmax = toi_SH_tickmax
    
            toi_specialteams_ticklabels = []
            if toi_specialteams_tickmax <= 2:
                toi_specialteams_ticklabels = [0, 2]
            if toi_specialteams_tickmax > 2 and toi_specialteams_tickmax <= 4:
                toi_specialteams_ticklabels = [0, 4]
            if toi_specialteams_tickmax > 4 and toi_specialteams_tickmax <= 6:
                toi_specialteams_ticklabels = [0, 6]
            if toi_specialteams_tickmax > 6 and toi_specialteams_tickmax <= 8:
                toi_specialteams_ticklabels = [0, 8]
            if toi_specialteams_tickmax > 8 and toi_specialteams_tickmax <= 10:
                toi_specialteams_ticklabels = [0, 10]
            if toi_specialteams_tickmax > 10 and toi_specialteams_tickmax <= 12:
                toi_specialteams_ticklabels = [0, 12]
            if toi_specialteams_tickmax > 12 and toi_specialteams_tickmax <= 14:
                toi_specialteams_ticklabels = [0, 14]
            if toi_specialteams_tickmax > 14 and toi_specialteams_tickmax <= 16:
                toi_specialteams_ticklabels = [0, 16]
            if toi_specialteams_tickmax > 16 and toi_specialteams_tickmax <= 18:
                toi_specialteams_ticklabels = [0, 18]
            if toi_specialteams_tickmax > 18 and toi_specialteams_tickmax <= 20:
                toi_specialteams_ticklabels = [0, 20]

            # set vertical indicator for midpoint of time on ice max
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                             
                ax_5v5_toi.axvspan(toi_5v5_ticklabels[1] / 2, toi_5v5_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
                ax_5v5_toi.axvspan(toi_5v5_ticklabels[1], toi_5v5_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_toi.axvspan(toi_4v4_ticklabels[1] / 2, toi_4v4_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
                ax_4v4_toi.axvspan(toi_4v4_ticklabels[1], toi_4v4_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_toi.axvspan(toi_3v3_ticklabels[1] / 2, toi_3v3_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
                ax_3v3_toi.axvspan(toi_3v3_ticklabels[1], toi_3v3_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
    
            ax_PP_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_PP_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
    
            ax_SH_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_SH_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
              
            # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.set_xticks(S_5v5_ticklabels, minor=False)
                ax_5v5_toi.set_xticks(toi_5v5_ticklabels, minor=False)

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.set_xticks(S_4v4_ticklabels, minor=False)
                ax_4v4_toi.set_xticks(toi_4v4_ticklabels, minor=False)

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.set_xticks(S_3v3_ticklabels, minor=False)
                ax_3v3_toi.set_xticks(toi_3v3_ticklabels, minor=False)

            ax_PP_shots.set_xticks(S_PP_ticklabels, minor=False)
            ax_PP_toi.set_xticks(toi_specialteams_ticklabels, minor=False)

            ax_SH_shots.set_xticks(S_SH_ticklabels, minor=False)
            ax_SH_toi.set_xticks(toi_specialteams_ticklabels, minor=False)

            # remove axes ticks for instances where there is no special teams play    
            if team_PP_toi == 0:            
                ax_PP_shots.set_xticks([], minor=False)
                ax_PP_shots.set_yticks([], minor=False)

                ax_PP_toi.set_xticks([], minor=False)
                ax_PP_toi.set_yticks([], minor=False)

            if team_SH_toi == 0:                           
                ax_SH_shots.set_xticks([], minor=False)
                ax_SH_shots.set_yticks([], minor=False)

                ax_SH_toi.set_xticks([], minor=False)
                ax_SH_toi.set_yticks([], minor=False)
            
            # remove the borders to each subplot
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.spines["top"].set_visible(False)   
                ax_5v5_shots.spines["bottom"].set_visible(False)    
                ax_5v5_shots.spines["right"].set_visible(False)    
                ax_5v5_shots.spines["left"].set_visible(False)  
                ax_5v5_toi.spines["top"].set_visible(False)   
                ax_5v5_toi.spines["bottom"].set_visible(False)    
                ax_5v5_toi.spines["right"].set_visible(False)    
                ax_5v5_toi.spines["left"].set_visible(False) 

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.spines["top"].set_visible(False)   
                ax_4v4_shots.spines["bottom"].set_visible(False)    
                ax_4v4_shots.spines["right"].set_visible(False)    
                ax_4v4_shots.spines["left"].set_visible(False)  
                ax_4v4_toi.spines["top"].set_visible(False)   
                ax_4v4_toi.spines["bottom"].set_visible(False)    
                ax_4v4_toi.spines["right"].set_visible(False)    
                ax_4v4_toi.spines["left"].set_visible(False) 

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.spines["top"].set_visible(False)   
                ax_3v3_shots.spines["bottom"].set_visible(False)    
                ax_3v3_shots.spines["right"].set_visible(False)    
                ax_3v3_shots.spines["left"].set_visible(False)  
                ax_3v3_toi.spines["top"].set_visible(False)   
                ax_3v3_toi.spines["bottom"].set_visible(False)    
                ax_3v3_toi.spines["right"].set_visible(False)    
                ax_3v3_toi.spines["left"].set_visible(False) 
        
            ax_PP_shots.spines["top"].set_visible(False)   
            ax_PP_shots.spines["bottom"].set_visible(False)    
            ax_PP_shots.spines["right"].set_visible(False)    
            ax_PP_shots.spines["left"].set_visible(False) 
            ax_PP_toi.spines["top"].set_visible(False)   
            ax_PP_toi.spines["bottom"].set_visible(False)    
            ax_PP_toi.spines["right"].set_visible(False)    
            ax_PP_toi.spines["left"].set_visible(False) 
    
            ax_SH_shots.spines["top"].set_visible(False)   
            ax_SH_shots.spines["bottom"].set_visible(False)    
            ax_SH_shots.spines["right"].set_visible(False)    
            ax_SH_shots.spines["left"].set_visible(False) 
            ax_SH_toi.spines["top"].set_visible(False)   
            ax_SH_toi.spines["bottom"].set_visible(False)    
            ax_SH_toi.spines["right"].set_visible(False)    
            ax_SH_toi.spines["left"].set_visible(False) 
            
            # add a legend for the shot type markers
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.legend(loc='center', bbox_to_anchor=(.55, -.9), ncol=4).get_frame().set_linewidth(0.0)

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.legend(loc='center', bbox_to_anchor=(.55, -.9), ncol=4).get_frame().set_linewidth(0.0)

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.legend(loc='center', bbox_to_anchor=(.55, -.9), ncol=4).get_frame().set_linewidth(0.0)

            # add text boxes with team names in white and with the team's color in the background  
            fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
            fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
            fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))
    
    
            ###
            ### SAVE TO FILE
            ###
            
            if team == away:
                plt.savefig(charts_players_individual_period + 'skaters_individual_shots_away_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)
            elif team == home:
                plt.savefig(charts_players_individual_period + 'skaters_individual_shots_home_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)    
            
            # exercise a command-line option to show the current figure
            if images == 'show':
                plt.show()
    
    
            ###
            ### CLOSE
            ###
            
            plt.close(fig)
            
            # status update
            print('Plotting ' + team + ' skaters individual shots for the ' + period_name + ' period.')   
        
    # status update
    print('Finished plotting the individual shots for skaters by period.')