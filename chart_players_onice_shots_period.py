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
    charts_players_onice_period = parameters.charts_players_onice_period
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
    players_file = files_root + 'stats_players_onice_period.csv'
    
    # create a dataframe object that reads in info from the .csv files
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
    ### 5v5, PP, SH
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
    
        # loop through each team
        for team in teams:
            
            if team == away:
                team_color = team_colors[0]
                opponent_color = team_colors[1]
        
            if team == home:
                team_color = team_colors[1]
                opponent_color = team_colors[0]

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
    
            # remove zeros from the goals for and against columns       
            team_df['GF'] = team_df['GF'].replace(0, np.NaN)       
            team_df['GA'] = team_df['GA'].replace(0, np.NaN)
    
            # make goals against and shots against negative
            team_df['GA'] *= -1
            team_df['SA'] *= -1
            
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
            team_PP_df = team_PP_df[(team_PP_df['STATE'] == 'PP') & (team_PP_df['TOI'] > 0)]
            team_PP_df = team_PP_df.sort_values(by=['TOI'], ascending = True)
            team_PP_df['RANK'] = team_PP_df['TOI'].rank(method='first')
            team_PP_df['RANK'] -= 1
    
            team_SH_df = team_df.copy()
            team_SH_df = team_SH_df[(team_SH_df['STATE'] == 'SH') & (team_SH_df['TOI'] > 0)]
            team_SH_df = team_SH_df.sort_values(by=['TOI'], ascending = True)
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
            fig.suptitle(date + ' Skaters On-Ice Shots (' + period_name + ' Period)\n\n')       
    
            # set the axes titles
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                      
                ax_5v5_shots.set_title('5v5 S', fontsize=10)
                ax_5v5_toi.set_title('5v5 TOI', fontsize=10)

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.set_title('4v4 S', fontsize=10)
                ax_4v4_toi.set_title('4v4 TOI', fontsize=10)

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.set_title('3v3 S', fontsize=10)
                ax_3v3_toi.set_title('3v3 TOI', fontsize=10)
    
            ax_PP_shots.set_title('PP S', fontsize=10)
            ax_PP_toi.set_title('PP TOI', fontsize=10)
    
            ax_SH_shots.set_title('SH S', fontsize=10)
            ax_SH_toi.set_title('SH TOI', fontsize=10)
           
            # for each state, plot the bars for total shots and markers for saved, missed and blocked shots markers
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                      
                try:
                    SF_5v5_plot = team_5v5_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_shots);
                except:
                    pass 
                try:
                    SA_5v5_plot = team_5v5_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    GF_5v5_marker = team_5v5_df.plot(x='GF', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    GA_5v5_marker = team_5v5_df.plot(x='GA', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass
                try:
                    SD_5v5_marker = team_5v5_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_shots);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                try:
                    SF_4v4_plot = team_4v4_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_4v4_shots);
                except:
                    pass 
                try:
                    SA_4v4_plot = team_4v4_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    GF_4v4_marker = team_4v4_df.plot(x='GF', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    GA_4v4_marker = team_4v4_df.plot(x='GA', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass
                try:
                    SD_4v4_marker = team_4v4_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_4v4_shots);
                except:
                    pass

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                try:
                    SF_3v3_plot = team_3v3_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_3v3_shots);
                except:
                    pass 
                try:
                    SA_3v3_plot = team_3v3_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    GF_3v3_marker = team_3v3_df.plot(x='GF', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    GA_3v3_marker = team_3v3_df.plot(x='GA', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass
                try:
                    SD_3v3_marker = team_3v3_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_3v3_shots);
                except:
                    pass

            if team_PP_toi != 0:
                try:
                    SF_PP_plot = team_PP_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_shots);
                except:
                    pass 
                try:
                    SA_PP_plot = team_PP_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_shots);
                except:
                    pass
                try:
                    GF_PP_marker = team_PP_df.plot(x='GF', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass
                try:
                    GA_PP_marker = team_PP_df.plot(x='GA', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass
                try:
                    SD_PP_marker = team_PP_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_shots);
                except:
                    pass

            if team_SH_toi != 0:   
                try:
                    SF_SH_plot = team_SH_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_SH_shots);
                except:
                    pass 
                try:
                    SA_SH_plot = team_SH_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_SH_shots);
                except:
                    pass
                try:
                    GF_SH_marker = team_SH_df.plot(x='GF', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
                except:
                    pass
                try:
                    GA_SH_marker = team_SH_df.plot(x='GA', y='RANK', marker='D', markersize=5, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
                except:
                    pass
                try:
                    SD_SH_marker = team_SH_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_shots);
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

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.set_xlabel('')
                ax_4v4_shots.set_ylabel('', fontsize=10)
                ax_4v4_toi.set_xlabel('')
                ax_4v4_toi.set_ylabel('')

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
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
            
            # set vertical indicators for zero shots
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')

            ax_PP_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')

            ax_SH_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            
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
    
            # create a list of x-axis tick values contingent on the max values for shots
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:
                team_5v5_df2 = team_5v5_df.copy()
                
                team_5v5_df2['SA'] *= -1
                
                SF_5v5_max = team_5v5_df2['SF']
                SF_5v5_max = SF_5v5_max.max()
        
                SA_5v5_max = team_5v5_df2['SA']
                SA_5v5_max = SA_5v5_max.max()
        
                S_5v5_tickmax = int()
                if SF_5v5_max >= SA_5v5_max:
                    S_5v5_tickmax = SF_5v5_max
                if SF_5v5_max < SA_5v5_max:
                    S_5v5_tickmax = SA_5v5_max
        
                S_5v5_ticklabels = []
                if S_5v5_tickmax <= 10:
                    S_5v5_ticklabels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
                if S_5v5_tickmax > 10 and S_5v5_tickmax <= 20:
                    S_5v5_ticklabels = [-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20]
                if S_5v5_tickmax > 20 and S_5v5_tickmax <= 30:
                    S_5v5_ticklabels = [-30, -24, -18, -12, -6, 0, 6, 12, 18, 24, 30]
                if S_5v5_tickmax > 30 and S_5v5_tickmax <= 40:
                    S_5v5_ticklabels = [-40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40]
                    
                toi_5v5_tickmax = max_toi_5v5
        
                toi_5v5_ticklabels = []
                if toi_5v5_tickmax <= 10:
                    toi_5v5_ticklabels = [0, 10]
                if toi_5v5_tickmax > 10 and toi_5v5_tickmax <= 15:
                    toi_5v5_ticklabels = [0, 15]
                if toi_5v5_tickmax > 15 and toi_5v5_tickmax <= 20:
                    toi_5v5_ticklabels = [0, 20]
                if toi_5v5_tickmax > 20 and toi_5v5_tickmax <= 25:
                    toi_5v5_ticklabels = [0, 25]
                if toi_5v5_tickmax > 25 and toi_5v5_tickmax <= 30:
                    toi_5v5_ticklabels = [0, 30]

            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                team_4v4_df2 = team_4v4_df.copy()
                
                team_4v4_df2['SA'] *= -1
                
                SF_4v4_max = team_4v4_df2['SF']
                SF_4v4_max = SF_4v4_max.max()
        
                SA_4v4_max = team_4v4_df2['SA']
                SA_4v4_max = SA_4v4_max.max()
        
                S_4v4_tickmax = int()
                if SF_4v4_max >= SA_4v4_max:
                    S_4v4_tickmax = SF_4v4_max
                if SF_4v4_max < SA_4v4_max:
                    S_4v4_tickmax = SA_4v4_max
        
                S_4v4_ticklabels = []
                if S_4v4_tickmax <= 10:
                    S_4v4_ticklabels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
                if S_4v4_tickmax > 10 and S_4v4_tickmax <= 20:
                    S_4v4_ticklabels = [-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20]
                if S_4v4_tickmax > 20 and S_4v4_tickmax <= 30:
                    S_4v4_ticklabels = [-30, -24, -18, -12, -6, 0, 6, 12, 18, 24, 30]
                if S_4v4_tickmax > 30 and S_4v4_tickmax <= 40:
                    S_4v4_ticklabels = [-40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40]
                    
                toi_4v4_tickmax = max_toi_4v4
        
                toi_4v4_ticklabels = []
                if toi_4v4_tickmax <= 10:
                    toi_4v4_ticklabels = [0, 10]
                if toi_4v4_tickmax > 10 and toi_4v4_tickmax <= 15:
                    toi_4v4_ticklabels = [0, 15]
                if toi_4v4_tickmax > 15 and toi_4v4_tickmax <= 20:
                    toi_4v4_ticklabels = [0, 20]
                if toi_4v4_tickmax > 20 and toi_4v4_tickmax <= 25:
                    toi_4v4_ticklabels = [0, 25]
                if toi_4v4_tickmax > 25 and toi_4v4_tickmax <= 30:
                    toi_4v4_ticklabels = [0, 30]

            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                team_3v3_df2 = team_3v3_df.copy()
                
                team_3v3_df2['SA'] *= -1
                
                SF_3v3_max = team_3v3_df2['SF']
                SF_3v3_max = SF_3v3_max.max()
        
                SA_3v3_max = team_3v3_df2['SA']
                SA_3v3_max = SA_3v3_max.max()
        
                S_3v3_tickmax = int()
                if SF_3v3_max >= SA_3v3_max:
                    S_3v3_tickmax = SF_3v3_max
                if SF_3v3_max < SA_3v3_max:
                    S_3v3_tickmax = SA_3v3_max
        
                S_3v3_ticklabels = []
                if S_3v3_tickmax <= 10:
                    S_3v3_ticklabels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
                if S_3v3_tickmax > 10 and S_3v3_tickmax <= 20:
                    S_3v3_ticklabels = [-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20]
                if S_3v3_tickmax > 20 and S_3v3_tickmax <= 30:
                    S_3v3_ticklabels = [-30, -24, -18, -12, -6, 0, 6, 12, 18, 24, 30]
                if S_3v3_tickmax > 30 and S_3v3_tickmax <= 40:
                    S_3v3_ticklabels = [-40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40]
                    
                toi_3v3_tickmax = max_toi_3v3
        
                toi_3v3_ticklabels = []
                if toi_3v3_tickmax <= 10:
                    toi_3v3_ticklabels = [0, 10]
                if toi_3v3_tickmax > 10 and toi_3v3_tickmax <= 15:
                    toi_3v3_ticklabels = [0, 15]
                if toi_3v3_tickmax > 15 and toi_3v3_tickmax <= 20:
                    toi_3v3_ticklabels = [0, 20]
                if toi_3v3_tickmax > 20 and toi_3v3_tickmax <= 25:
                    toi_3v3_ticklabels = [0, 25]
                if toi_3v3_tickmax > 25 and toi_3v3_tickmax <= 30:
                    toi_3v3_ticklabels = [0, 30]

            team_PP_df2 = team_PP_df.copy()
            team_PP_df2['SA'] *= -1
                
            SF_PP_max = team_PP_df2['SF']
            SF_PP_max = SF_PP_max.max()
            
            SA_PP_max = team_PP_df2['SA']
            SA_PP_max = SA_PP_max.max()
    
            S_PP_tickmax = int()
            if SF_PP_max >= SA_PP_max:
                S_PP_tickmax = SF_PP_max
            if SF_PP_max < SA_PP_max:
                S_PP_tickmax = SA_PP_max
    
            S_PP_ticklabels = []
            if S_PP_tickmax <= 4:
                S_PP_ticklabels = [-4, -2, 0, 2, 4]
            if S_PP_tickmax > 4 and S_PP_tickmax <= 6:
                S_PP_ticklabels = [-6, -3, 0, 3, 6]
            if S_PP_tickmax > 6 and S_PP_tickmax <= 8:
                S_PP_ticklabels = [-8, -4, 0, 4, 8]
            if S_PP_tickmax > 8 and S_PP_tickmax <= 10:
                S_PP_ticklabels = [-10, -5, 0, 5, 10]
            if S_PP_tickmax > 10 and S_PP_tickmax <= 12:
                S_PP_ticklabels = [-12, -6, 0, 6, 12]
            if S_PP_tickmax > 12 and S_PP_tickmax <= 14:
                S_PP_ticklabels = [-14, -7, 0, 7, 14]
            if S_PP_tickmax > 14 and S_PP_tickmax <= 16:
                S_PP_ticklabels = [-16, -8, 0, 8, 16]
            if S_PP_tickmax > 16 and S_PP_tickmax <= 18:
                S_PP_ticklabels = [-18, -9, 0, 9, 18]
            if S_PP_tickmax > 18 and S_PP_tickmax <= 20:
                S_PP_ticklabels = [-20, -10, 0, 10, 20]

            team_SH_df2 = team_SH_df.copy()
            team_SH_df2['SA'] *= -1
                
            SF_SH_max = team_SH_df2['SF']
            SF_SH_max = SF_SH_max.max()
            
            SA_SH_max = team_SH_df2['SA']
            SA_SH_max = SA_SH_max.max()
    
            S_SH_tickmax = int()
            if SF_SH_max >= SA_SH_max:
                S_SH_tickmax = SF_SH_max
            if SF_SH_max < SA_SH_max:
                S_SH_tickmax = SA_SH_max
    
            S_SH_ticklabels = []
            if S_SH_tickmax <= 4:
                S_SH_ticklabels = [-4, -2, 0, 2, 4]
            if S_SH_tickmax > 4 and S_SH_tickmax <= 6:
                S_SH_ticklabels = [-6, -3, 0, 3, 6]
            if S_SH_tickmax > 6 and S_SH_tickmax <= 8:
                S_SH_ticklabels = [-8, -4, 0, 4, 8]
            if S_SH_tickmax > 8 and S_SH_tickmax <= 10:
                S_SH_ticklabels = [-10, -5, 0, 5, 10]
            if S_SH_tickmax > 10 and S_SH_tickmax <= 12:
                S_SH_ticklabels = [-12, -6, 0, 6, 12]
            if S_SH_tickmax > 12 and S_SH_tickmax <= 14:
                S_SH_ticklabels = [-14, -7, 0, 7, 14]
            if S_SH_tickmax > 14 and S_SH_tickmax <= 16:
                S_SH_ticklabels = [-16, -8, 0, 8, 16]
            if S_SH_tickmax > 16 and S_SH_tickmax <= 18:
                S_SH_ticklabels = [-18, -9, 0, 9, 18]
            if S_SH_tickmax > 18 and S_SH_tickmax <= 20:
                S_SH_ticklabels = [-20, -10, 0, 10, 20]
                
            toi_PP_tickmax = max_toi_PP
    
            toi_SH_tickmax = max_toi_SH
    
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
            from matplotlib.lines import Line2D
            elements = [Line2D([0], [0], marker='D', markersize=5, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Scored'), Line2D([0], [0], marker='|', markersize=11, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
            if period < 4 and int(game_id) < 30000 or period == 4 and int(game_id) >= 30000:                          
                ax_5v5_shots.legend(handles=elements, loc='center', bbox_to_anchor=(.55, -.925), ncol=2).get_frame().set_linewidth(0.0)
            if period == 4 and int(game_id) < 30000 and int(season_id) <= 20142015:
                ax_4v4_shots.legend(handles=elements, loc='center', bbox_to_anchor=(.55, -.925), ncol=2).get_frame().set_linewidth(0.0)
            if period == 4 and int(game_id) < 30000 and int(season_id) >= 20152016:
                ax_3v3_shots.legend(handles=elements, loc='center', bbox_to_anchor=(.55, -.925), ncol=2).get_frame().set_linewidth(0.0)
            
            # add text boxes with team names in white and with the team's color in the background  
            fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
            fig.text(.525, 0.936, ' ' + home + ' ', color='white', fontsize='12', bbox=dict(facecolor=home_color, edgecolor='None'))
            fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))
    
    
            ###
            ### SAVE TO FILE
            ###
            
            if team == away:
                plt.savefig(charts_players_onice_period + 'skaters_onice_shots_away_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)
            elif team == home:
                plt.savefig(charts_players_onice_period + 'skaters_onice_shots_home_' + period_name + '.png', bbox_inches='tight', pad_inches=0.2)    
            
            # exercise a command-line option to show the current figure
            if images == 'show':
                plt.show()
    
    
            ###
            ### CLOSE
            ###
            
            plt.close(fig)
            
            # status update
            print('Plotting ' + team + ' skaters on-ice shots for the ' + period_name + ' period.')   
        
    # status update
    print('Finished plotting the on-ice shots for skaters by period.')