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
    charts_players_onice = parameters.charts_players_onice
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
    players_file = files_root + 'stats_players_onice.csv'
    
    # create a dataframe object that reads in info from the .csv files
    players_df = pd.read_csv(players_file)

    players_5v5_df = players_df.copy()
    players_5v5_df = players_5v5_df[(players_5v5_df['STATE'] == '5v5')]
    max_5v5_toi = players_5v5_df['TOI'].max()     

    players_PP_df = players_df.copy()
    players_PP_df = players_PP_df[(players_PP_df['STATE'] == 'PP')]
    max_PP_toi = players_PP_df['TOI'].max()

    players_SH_df = players_df.copy()
    players_SH_df = players_SH_df[(players_SH_df['STATE'] == 'SH')]
    max_SH_toi = players_SH_df['TOI'].max()      
    
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
    
    # loop through each team
    for team in teams:
        
        if team == away:
            team_color = team_colors[0]
            opponent_color = team_colors[1]
    
        if team == home:
            team_color = team_colors[1]
            opponent_color = team_colors[0]


        # create a dataframe; filter for team; sort by team, game state and position; rank by time on ice and then invert the rankings
        team_df = players_df.copy()
        team_df = team_df[(team_df['TEAM'] == team)]

        # remove zeros from the differential column      
        team_df['SD'] = team_df['SD'].replace(0, np.NaN)       

        # make goals against and shots against negative
        team_df['SA'] *= -1
        
        # make distinct dataframes for skaters and goalies
        team_skaters_df = team_df[(team_df['POS'] != 'G')]
        team_goalies_df = team_df[(team_df['POS'] == 'G')]
        
        # create a filtered dataframe for each game state; sort by team, game state and position; rank by time on ice and then invert the rankings
        team_5v5_skaters_df = team_skaters_df.copy()
        team_5v5_skaters_df = team_5v5_skaters_df[(team_5v5_skaters_df['STATE'] == '5v5')]
        team_5v5_skaters_df = team_5v5_skaters_df.sort_values(by=['TOI'], ascending = True)
        team_5v5_skaters_df['RANK'] = team_5v5_skaters_df['TOI'].rank(method='first')
        team_5v5_skaters_df['RANK'] -= 1

        team_5v5_goalies_df = team_goalies_df.copy()
        team_5v5_goalies_df = team_5v5_goalies_df[(team_5v5_goalies_df['STATE'] == '5v5')]
        team_5v5_goalies_df = team_5v5_goalies_df.sort_values(by=['TOI'], ascending = True)
        team_5v5_goalies_df['RANK'] = team_5v5_goalies_df['TOI'].rank(method='first')
        team_5v5_goalies_df['RANK'] -= 1
               
        team_PP_skaters_df = team_skaters_df.copy()
        team_PP_skaters_df = team_PP_skaters_df[(team_PP_skaters_df['STATE'] == 'PP') & (team_PP_skaters_df['TOI'] > 0)]
        team_PP_skaters_df = team_PP_skaters_df.sort_values(by=['TOI'], ascending = True)
        team_PP_skaters_df = team_PP_skaters_df.iloc[-10:]    
        team_PP_skaters_df['RANK'] = team_PP_skaters_df['TOI'].rank(method='first')
        team_PP_skaters_df['RANK'] -= 1

        team_PP_goalies_df = team_goalies_df.copy()
        team_PP_goalies_df = team_PP_goalies_df[(team_PP_goalies_df['STATE'] == 'PP') & (team_PP_goalies_df['TOI'] > 0)]
        team_PP_goalies_df = team_PP_goalies_df.sort_values(by=['TOI'], ascending = True)
        team_PP_goalies_df['RANK'] = team_PP_goalies_df['TOI'].rank(method='first')
        team_PP_goalies_df['RANK'] -= 1

        team_SH_skaters_df = team_skaters_df.copy()
        team_SH_skaters_df = team_SH_skaters_df[(team_SH_skaters_df['STATE'] == 'SH') & (team_SH_skaters_df['TOI'] > 0)]
        team_SH_skaters_df = team_SH_skaters_df.sort_values(by=['TOI'], ascending = True)
        team_SH_skaters_df = team_SH_skaters_df.iloc[-10:]    
        team_SH_skaters_df['RANK'] = team_SH_skaters_df['TOI'].rank(method='first')
        team_SH_skaters_df['RANK'] -= 1

        team_SH_goalies_df = team_goalies_df.copy()
        team_SH_goalies_df = team_SH_goalies_df[(team_SH_goalies_df['STATE'] == 'SH') & (team_SH_goalies_df['TOI'] > 0)]
        team_SH_goalies_df = team_SH_goalies_df.sort_values(by=['TOI'], ascending = True)
        team_SH_goalies_df['RANK'] = team_SH_goalies_df['TOI'].rank(method='first')
        team_SH_goalies_df['RANK'] -= 1
      
        # for each game state, create a dataframe with just the time on ice column; set a max value; scale each player's time on ice relative to the max
        team_toi_5v5_skaters = team_5v5_skaters_df['TOI']        
        max_team_toi_5v5_skaters = team_toi_5v5_skaters.max()

        team_toi_5v5_goalies = team_5v5_goalies_df['TOI']        
        max_team_toi_5v5_goalies = team_toi_5v5_goalies.max()
        
        team_toi_PP_skaters = team_PP_skaters_df['TOI']        
        max_team_toi_PP_skaters = team_toi_PP_skaters.max()
        team_PP_toi_skaters = max_team_toi_PP_skaters

        team_toi_PP_goalies = team_PP_goalies_df['TOI']        
        max_team_toi_PP_goalies = team_toi_PP_goalies.max()
        team_PP_toi_goalies = max_team_toi_PP_goalies

        team_toi_SH_skaters = team_SH_skaters_df['TOI']        
        max_team_toi_SH_skaters = team_toi_SH_skaters.max()
        team_SH_toi_skaters = max_team_toi_SH_skaters

        team_toi_SH_goalies = team_SH_goalies_df['TOI']        
        max_team_toi_SH_goalies = team_toi_SH_goalies.max()
        team_SH_toi_goalies = max_team_toi_SH_goalies
        
        # create a figure with six subplots arrangled complexly using a grid structure
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(11, 8,  hspace=0.25, wspace=0.75)

        ax_5v5_skaters_shots = fig.add_subplot(grid[0:5, :-1])
        ax_5v5_skaters_toi = fig.add_subplot(grid[0:5, 7])        

        ax_5v5_goalies_shots = fig.add_subplot(grid[5:6, :-1])
        ax_5v5_goalies_toi = fig.add_subplot(grid[5:6, 7])        

        ax_gap = fig.add_subplot(grid[6:7, :])

        ax_PP_skaters_shots = fig.add_subplot(grid[7:10, :2])
        ax_PP_skaters_toi = fig.add_subplot(grid[7:10, 2]) 

        ax_PP_goalies_shots = fig.add_subplot(grid[10:, :2])
        ax_PP_goalies_toi = fig.add_subplot(grid[10:, 2])        

        ax_SH_skaters_shots = fig.add_subplot(grid[7:10, 5:-1])
        ax_SH_skaters_toi = fig.add_subplot(grid[7:10, 7]) 

        ax_SH_goalies_shots = fig.add_subplot(grid[10:, 5:-1])
        ax_SH_goalies_toi = fig.add_subplot(grid[10:, 7])        

        # set the plot title
        fig.suptitle(date + ' Players On-Ice Shots\n\n')       

        # set the axes titles
        ax_5v5_skaters_shots.set_title('5v5 S', fontsize=10)
        ax_5v5_skaters_toi.set_title('5v5 TOI', fontsize=10)

        ax_5v5_goalies_shots.set_title('', fontsize=10)
        ax_5v5_goalies_toi.set_title('', fontsize=10)

        ax_PP_skaters_shots.set_title('PP S', fontsize=10)
        ax_PP_skaters_toi.set_title('PP TOI', fontsize=10)

        ax_PP_goalies_shots.set_title('', fontsize=10)
        ax_PP_goalies_toi.set_title('', fontsize=10)

        ax_SH_skaters_shots.set_title('SH S', fontsize=10)
        ax_SH_skaters_toi.set_title('SH TOI', fontsize=10)

        ax_SH_goalies_shots.set_title('', fontsize=10)
        ax_SH_goalies_toi.set_title('', fontsize=10)

        # ensure certain axes backgrounds are transparent
        ax_gap.set_facecolor('None')
       
        # for each state, plot the bars for total shots and markers for saved, missed and blocked shots markers
        try:
            SF_5v5_skaters_plot = team_5v5_skaters_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_skaters_shots);
        except:
            pass 
        try:
            SA_5v5_skaters_plot = team_5v5_skaters_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_skaters_shots);
        except:
            pass
        try:
            SD_5v5_skaters_marker = team_5v5_skaters_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_skaters_shots);
        except:
            pass

        try:
            SF_5v5_goalies_plot = team_5v5_goalies_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_5v5_goalies_shots);
        except:
            pass 
        try:
            SA_5v5_goalies_plot = team_5v5_goalies_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_5v5_goalies_shots);
        except:
            pass
        try:
            SD_5v5_goalies_marker = team_5v5_goalies_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_goalies_shots);
        except:
            pass
        
        try:
            SF_PP_skaters_plot = team_PP_skaters_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_skaters_shots);
        except:
            pass 
        try:
            SA_PP_skaters_plot = team_PP_skaters_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_skaters_shots);
        except:
            pass
        try:
            SD_PP_skaters_marker = team_PP_skaters_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_skaters_shots);
        except:
            pass

        try:
            SF_PP_goalies_plot = team_PP_goalies_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_PP_goalies_shots);
        except:
            pass 
        try:
            SA_PP_goalies_plot = team_PP_goalies_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_PP_goalies_shots);
        except:
            pass
        try:
            SD_PP_goalies_marker = team_PP_goalies_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_goalies_shots);
        except:
            pass

        try:
            SF_SH_skaters_plot = team_SH_skaters_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_SH_skaters_shots);
        except:
            pass 
        try:
            SA_SH_skaters_plot = team_SH_skaters_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_SH_skaters_shots);
        except:
            pass
        try:
            SD_SH_skater_marker = team_SH_skaters_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_skaters_shots);
        except:
            pass

        try:
            SF_SH_goalies_plot = team_SH_goalies_df.plot.barh(x='PLAYER', y='SF', color=team_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_SH_goalies_shots);
        except:
            pass 
        try:
            SA_SH_goalies_plot = team_SH_goalies_df.plot.barh(x='PLAYER', y='SA', color=opponent_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_SH_goalies_shots);
        except:
            pass
        try:
            SD_SH_goalies_marker = team_SH_goalies_df.plot(x='SD', y='RANK', marker='|', markersize=11, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_SH_goalies_shots);
        except:
            pass

        # for each state, plot the bars for time on ice
        try:
            toi_5v5_skaters_plot = team_5v5_skaters_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_5v5_skaters_toi);
        except:
            pass
        
        try:
            toi_5v5_goalies_plot = team_5v5_goalies_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_5v5_goalies_toi);
        except:
            pass      
        
        try:
            toi_PP_skaters_plot = team_PP_skaters_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_PP_skaters_toi);
        except:
            pass

        try:
            toi_PP_goalies_plot = team_PP_goalies_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_PP_goalies_toi);
        except:
            pass
        
        try:
            toi_SH_skaters_plot = team_SH_skaters_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_SH_skaters_toi);
        except:
            pass

        try:
            toi_SH_goalies_plot = team_SH_goalies_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_SH_goalies_toi);
        except:
            pass

        # set / remove the y-labels for the subplots
        ax_5v5_skaters_shots.set_xlabel('')
        ax_5v5_skaters_shots.set_ylabel('', fontsize=10, color=team_color)
        ax_5v5_skaters_toi.set_xlabel('')
        ax_5v5_skaters_toi.set_ylabel('')

        ax_5v5_goalies_shots.set_xlabel('')
        ax_5v5_goalies_shots.set_ylabel('', fontsize=10, color=team_color)
        ax_5v5_goalies_toi.set_xlabel('')
        ax_5v5_goalies_toi.set_ylabel('')

        ax_gap.set_xlabel('')
        ax_gap.set_ylabel('', fontsize=10)
        ax_gap.set_xlabel('')
        ax_gap.set_ylabel('')

        ax_PP_skaters_shots.set_xlabel('')
        ax_PP_skaters_shots.set_ylabel('', fontsize=10, color=team_color)
        ax_PP_skaters_toi.set_xlabel('')
        ax_PP_skaters_toi.set_ylabel('')

        ax_PP_goalies_shots.set_xlabel('')
        ax_PP_goalies_shots.set_ylabel('', fontsize=10, color=team_color)
        ax_PP_goalies_toi.set_xlabel('')
        ax_PP_goalies_toi.set_ylabel('')

        ax_SH_skaters_shots.set_xlabel('')
        ax_SH_skaters_shots.set_ylabel('', fontsize=10, color=team_color)
        ax_SH_skaters_toi.set_xlabel('')
        ax_SH_skaters_toi.set_ylabel('')

        ax_SH_goalies_shots.set_xlabel('')
        ax_SH_goalies_shots.set_ylabel('', fontsize=10, color=team_color)
        ax_SH_goalies_toi.set_xlabel('')
        ax_SH_goalies_toi.set_ylabel('')

        # set vertical indicators for zero shots
        ax_5v5_skaters_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        ax_5v5_goalies_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')

        ax_PP_skaters_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        ax_PP_goalies_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')

        ax_SH_skaters_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        ax_SH_goalies_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        
        # change the tick parameters for each axes
        ax_5v5_skaters_shots.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off
        ax_5v5_skaters_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off

        ax_5v5_goalies_shots.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on
        ax_5v5_goalies_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on

        ax_gap.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off
        ax_gap.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off

        ax_PP_skaters_shots.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off
        ax_PP_skaters_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off            
            labelbottom=False)  # labels along the bottom edge are off

        ax_PP_goalies_shots.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on
        ax_PP_goalies_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off            
            labelbottom=True)  # labels along the bottom edge are on

        ax_SH_skaters_shots.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off
        ax_SH_skaters_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=False)  # labels along the bottom edge are off

        ax_SH_goalies_shots.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on
        ax_SH_goalies_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on

        # change the y-axis label colors
        ax_5v5_skaters_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_5v5_goalies_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_PP_skaters_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_PP_goalies_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_SH_skaters_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_SH_goalies_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        # create a list of x-axis tick values contingent on the max values for shots
        team_5v5_df2 = players_5v5_df.copy()
        team_PP_df2 = players_PP_df.copy()
        team_SH_df2 = players_SH_df.copy()
       
        team_5v5_df2['SA'] *= -1
        team_PP_df2['SA'] *= -1
        team_SH_df2['SA'] *= -1
       
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
          
        toi_5v5_tickmax = max_5v5_toi

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
        if toi_5v5_tickmax > 30 and toi_5v5_tickmax <= 35:
            toi_5v5_ticklabels = [0, 35]
        if toi_5v5_tickmax > 35 and toi_5v5_tickmax <= 40:
            toi_5v5_ticklabels = [0, 40]
        if toi_5v5_tickmax > 40 and toi_5v5_tickmax <= 45:
            toi_5v5_ticklabels = [0, 45]
        if toi_5v5_tickmax > 45 and toi_5v5_tickmax <= 50:
            toi_5v5_ticklabels = [0, 50]
        if toi_5v5_tickmax > 50 and toi_5v5_tickmax <= 55:
            toi_5v5_ticklabels = [0, 55]
        if toi_5v5_tickmax > 55 and toi_5v5_tickmax <= 60:
            toi_5v5_ticklabels = [0, 60]
           
        SF_PP_max = team_PP_df2['SF']
        SF_PP_max = SF_PP_max.max()
       
        SA_PP_max = team_PP_df2['SA']
        SA_PP_max = SA_PP_max.max()

        S_PP_tickmax = int()
        if SF_PP_max >= SA_PP_max:
            S_PP_tickmax = SF_PP_max
        if SF_PP_max < SA_PP_max:
            S_PP_tickmax = SA_PP_max
          
        SF_SH_max = team_SH_df2['SF']
        SF_SH_max = SF_SH_max.max()
       
        SA_SH_max = team_SH_df2['SA']
        SA_SH_max = SA_SH_max.max()

        S_SH_tickmax = int()
        if SF_SH_max >= SA_SH_max:
            S_SH_tickmax = SF_SH_max
        if SF_SH_max < SA_SH_max:
            S_SH_tickmax = SA_SH_max

        S_specialteams_tickmax = int()
        if S_PP_tickmax >= S_SH_tickmax:
            S_specialteams_tickmax = S_PP_tickmax
        if S_PP_tickmax < S_SH_tickmax:
            S_specialteams_tickmax = S_SH_tickmax

        S_specialteams_ticklabels = []
        if S_specialteams_tickmax <= 4:
            S_specialteams_ticklabels = [-4, -2, 0, 2, 4]
        if S_specialteams_tickmax > 4 and S_specialteams_tickmax <= 6:
            S_specialteams_ticklabels = [-6, -3, 0, 3, 6]
        if S_specialteams_tickmax > 6 and S_specialteams_tickmax <= 8:
            S_specialteams_ticklabels = [-8, -4, 0, 4, 8]
        if S_specialteams_tickmax > 8 and S_specialteams_tickmax <= 10:
            S_specialteams_ticklabels = [-10, -5, 0, 5, 10]
        if S_specialteams_tickmax > 10 and S_specialteams_tickmax <= 12:
            S_specialteams_ticklabels = [-12, -6, 0, 6, 12]
        if S_specialteams_tickmax > 12 and S_specialteams_tickmax <= 14:
            S_specialteams_ticklabels = [-14, -7, 0, 7, 14]
        if S_specialteams_tickmax > 14 and S_specialteams_tickmax <= 16:
            S_specialteams_ticklabels = [-16, -8, 0, 8, 16]
        if S_specialteams_tickmax > 16 and S_specialteams_tickmax <= 18:
            S_specialteams_ticklabels = [-18, -9, 0, 9, 18]
        if S_specialteams_tickmax > 18 and S_specialteams_tickmax <= 20:
            S_specialteams_ticklabels = [-20, -10, 0, 10, 20]
            
        toi_PP_tickmax = max_PP_toi

        toi_SH_tickmax = max_SH_toi

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
        ax_5v5_skaters_toi.axvspan(toi_5v5_ticklabels[1] / 2, toi_5v5_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_5v5_skaters_toi.axvspan(toi_5v5_ticklabels[1], toi_5v5_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_5v5_goalies_toi.axvspan(toi_5v5_ticklabels[1] / 2, toi_5v5_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_5v5_goalies_toi.axvspan(toi_5v5_ticklabels[1], toi_5v5_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_PP_skaters_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_PP_skaters_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_PP_goalies_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_PP_goalies_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_SH_skaters_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_SH_skaters_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_SH_goalies_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_SH_goalies_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
          
        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_5v5_skaters_shots.set_xticks(S_5v5_ticklabels, minor=False)
        ax_5v5_skaters_toi.set_xticks(toi_5v5_ticklabels, minor=False)

        ax_5v5_goalies_shots.set_xticks(S_5v5_ticklabels, minor=False)
        ax_5v5_goalies_toi.set_xticks(toi_5v5_ticklabels, minor=False)
        
        ax_PP_skaters_shots.set_xticks(S_specialteams_ticklabels, minor=False)
        ax_PP_skaters_toi.set_xticks(toi_specialteams_ticklabels, minor=False)

        ax_PP_goalies_shots.set_xticks(S_specialteams_ticklabels, minor=False)
        ax_PP_goalies_toi.set_xticks(toi_specialteams_ticklabels, minor=False)
        
        ax_SH_skaters_shots.set_xticks(S_specialteams_ticklabels, minor=False)
        ax_SH_skaters_toi.set_xticks(toi_specialteams_ticklabels, minor=False)

        ax_SH_goalies_shots.set_xticks(S_specialteams_ticklabels, minor=False)
        ax_SH_goalies_toi.set_xticks(toi_specialteams_ticklabels, minor=False)

        # remove axes ticks for instances where there is no special teams play    
        if max_team_toi_PP_skaters == 0:            
            ax_PP_skaters_shots.set_xticks([], minor=False)
            ax_PP_skaters_shots.set_yticks([], minor=False)               
            ax_PP_skaters_toi.set_xticks([], minor=False)
            ax_PP_skaters_toi.set_yticks([], minor=False)

        if max_team_toi_PP_goalies == 0:            
            ax_PP_goalies_shots.set_xticks([], minor=False)
            ax_PP_goalies_shots.set_yticks([], minor=False)               
            ax_PP_goalies_toi.set_xticks([], minor=False)
            ax_PP_goalies_toi.set_yticks([], minor=False)
    
        if max_team_toi_SH_skaters == 0:            
            ax_SH_skaters_shots.set_xticks([], minor=False)
            ax_SH_skaters_shots.set_yticks([], minor=False)
            ax_SH_skaters_toi.set_xticks([], minor=False)
            ax_SH_skaters_toi.set_yticks([], minor=False)
 
        if max_team_toi_SH_goalies == 0:            
            ax_SH_goalies_shots.set_xticks([], minor=False)
            ax_SH_goalies_shots.set_yticks([], minor=False)
            ax_SH_goalies_toi.set_xticks([], minor=False)
            ax_SH_goalies_toi.set_yticks([], minor=False)
       
        # remove the borders to each subplot
        ax_5v5_skaters_shots.spines["top"].set_visible(False)   
        ax_5v5_skaters_shots.spines["bottom"].set_visible(False)    
        ax_5v5_skaters_shots.spines["right"].set_visible(False)    
        ax_5v5_skaters_shots.spines["left"].set_visible(False)  
        ax_5v5_skaters_toi.spines["top"].set_visible(False)   
        ax_5v5_skaters_toi.spines["bottom"].set_visible(False)    
        ax_5v5_skaters_toi.spines["right"].set_visible(False)    
        ax_5v5_skaters_toi.spines["left"].set_visible(False) 

        ax_5v5_goalies_shots.spines["top"].set_visible(False)   
        ax_5v5_goalies_shots.spines["bottom"].set_visible(False)    
        ax_5v5_goalies_shots.spines["right"].set_visible(False)    
        ax_5v5_goalies_shots.spines["left"].set_visible(False)  
        ax_5v5_goalies_toi.spines["top"].set_visible(False)   
        ax_5v5_goalies_toi.spines["bottom"].set_visible(False)    
        ax_5v5_goalies_toi.spines["right"].set_visible(False)    
        ax_5v5_goalies_toi.spines["left"].set_visible(False)

        ax_gap.spines["top"].set_visible(False)   
        ax_gap.spines["bottom"].set_visible(False)    
        ax_gap.spines["right"].set_visible(False)    
        ax_gap.spines["left"].set_visible(False)  
        
        ax_PP_skaters_shots.spines["top"].set_visible(False)   
        ax_PP_skaters_shots.spines["bottom"].set_visible(False)    
        ax_PP_skaters_shots.spines["right"].set_visible(False)    
        ax_PP_skaters_shots.spines["left"].set_visible(False) 
        ax_PP_skaters_toi.spines["top"].set_visible(False)   
        ax_PP_skaters_toi.spines["bottom"].set_visible(False)    
        ax_PP_skaters_toi.spines["right"].set_visible(False)    
        ax_PP_skaters_toi.spines["left"].set_visible(False) 

        ax_PP_goalies_shots.spines["top"].set_visible(False)   
        ax_PP_goalies_shots.spines["bottom"].set_visible(False)    
        ax_PP_goalies_shots.spines["right"].set_visible(False)    
        ax_PP_goalies_shots.spines["left"].set_visible(False)  
        ax_PP_goalies_toi.spines["top"].set_visible(False)   
        ax_PP_goalies_toi.spines["bottom"].set_visible(False)    
        ax_PP_goalies_toi.spines["right"].set_visible(False)    
        ax_PP_goalies_toi.spines["left"].set_visible(False)

        ax_SH_skaters_shots.spines["top"].set_visible(False)   
        ax_SH_skaters_shots.spines["bottom"].set_visible(False)    
        ax_SH_skaters_shots.spines["right"].set_visible(False)    
        ax_SH_skaters_shots.spines["left"].set_visible(False) 
        ax_SH_skaters_toi.spines["top"].set_visible(False)   
        ax_SH_skaters_toi.spines["bottom"].set_visible(False)    
        ax_SH_skaters_toi.spines["right"].set_visible(False)    
        ax_SH_skaters_toi.spines["left"].set_visible(False) 

        ax_SH_goalies_shots.spines["top"].set_visible(False)   
        ax_SH_goalies_shots.spines["bottom"].set_visible(False)    
        ax_SH_goalies_shots.spines["right"].set_visible(False)    
        ax_SH_goalies_shots.spines["left"].set_visible(False)  
        ax_SH_goalies_toi.spines["top"].set_visible(False)   
        ax_SH_goalies_toi.spines["bottom"].set_visible(False)    
        ax_SH_goalies_toi.spines["right"].set_visible(False)    
        ax_SH_goalies_toi.spines["left"].set_visible(False)

        # add a legend for the shot type markers
        from matplotlib.lines import Line2D
        elements = [Line2D([0], [0], marker='|', markersize=11, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
        ax_5v5_skaters_shots.legend(handles=elements, loc='center', bbox_to_anchor=(.55, -1.425), ncol=2).get_frame().set_linewidth(0.0)
        
        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', color='white', fontsize='12', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))


        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_players_onice + 'players_onice_shots_away.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_players_onice + 'players_onice_shots_home.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()


        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' skaters and goalies on-ice shots.')   
        
    # status update
    print('Finished plotting the on-ice shots for skaters and goalies.')