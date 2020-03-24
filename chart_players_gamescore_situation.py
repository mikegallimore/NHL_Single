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
    charts_players_composite_situation = parameters.charts_players_composite_situation
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
    team_file = files_root + 'stats_teams_situation.csv'
    players_individual_file = files_root + 'stats_players_individual_situation.csv'
    players_onice_file = files_root + 'stats_players_onice_situation.csv'
    
    # create dataframe objects that read in info from the .csv files
    team_stats_df = pd.read_csv(team_file)
    players_individual_df = pd.read_csv(players_individual_file)
    players_individual_df = players_individual_df.rename(columns={'GS': 'iGS'})
    players_individual_df = players_individual_df[['TEAM', 'PLAYER', 'POS', 'STATE', 'SITUATION', 'TOI', 'iGS']]
    
    players_onice_df = pd.read_csv(players_onice_file)
    players_onice_df = players_onice_df.rename(columns={'GS': 'onGS'})
    players_onice_df = players_onice_df[['TEAM', 'PLAYER', 'POS', 'STATE', 'SITUATION', 'TOI', 'onGS']]

    players_df = pd.merge(players_individual_df, players_onice_df, on=['TEAM', 'PLAYER', 'POS', 'STATE', 'SITUATION', 'TOI'], how='inner')
    players_df['GS'] = players_df['iGS'] + players_df['onGS']

    # create dataframes filtered for game state, then player type
    teams_all_df = players_df.copy()
    teams_all_df = teams_all_df[(teams_all_df['STATE'] == 'ALL')]  
    teams_all_skaters_df = teams_all_df.copy()
    teams_all_skaters_df = teams_all_skaters_df[(teams_all_skaters_df['POS'] != 'G')]
    teams_all_goalies_df = teams_all_df.copy()
    teams_all_goalies_df = teams_all_goalies_df[(teams_all_goalies_df['POS'] == 'G')]

    teams_5v5_df = players_df.copy()
    teams_5v5_df = teams_5v5_df[(teams_5v5_df['STATE'] == '5v5')]  
    teams_5v5_skaters_df = teams_5v5_df.copy()
    teams_5v5_skaters_df = teams_5v5_skaters_df[(teams_5v5_skaters_df['POS'] != 'G')]
    teams_5v5_goalies_df = teams_5v5_df.copy()
    teams_5v5_goalies_df = teams_5v5_goalies_df[(teams_5v5_goalies_df['POS'] == 'G')]

    teams_3v3_df = players_df.copy()
    teams_3v3_df = teams_3v3_df[(teams_3v3_df['STATE'] == '3v3')]  
    teams_3v3_skaters_df = teams_3v3_df.copy()
    teams_3v3_skaters_df = teams_3v3_skaters_df[(teams_3v3_skaters_df['POS'] != 'G')]
    teams_3v3_goalies_df = teams_3v3_df.copy()
    teams_3v3_goalies_df = teams_3v3_goalies_df[(teams_3v3_goalies_df['POS'] == 'G')]

    teams_PP_df = players_df.copy()
    teams_PP_df = teams_PP_df[(teams_PP_df['STATE'] == 'PP')]  
    teams_PP_skaters_df = teams_PP_df.copy()
    teams_PP_skaters_df = teams_PP_skaters_df[(teams_PP_skaters_df['POS'] != 'G')]
    teams_PP_goalies_df = teams_PP_df.copy()
    teams_PP_goalies_df = teams_PP_goalies_df[(teams_PP_goalies_df['POS'] == 'G')]

    teams_SH_df = players_df.copy()
    teams_SH_df = teams_SH_df[(teams_SH_df['STATE'] == 'SH')]  
    teams_SH_skaters_df = teams_SH_df.copy()
    teams_SH_skaters_df = teams_SH_skaters_df[(teams_SH_skaters_df['POS'] != 'G')]
    teams_SH_goalies_df = teams_SH_df.copy()
    teams_SH_goalies_df = teams_SH_goalies_df[(teams_SH_goalies_df['POS'] == 'G')]
    
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

    situations = ['Leading', 'Tied', 'Trailing']

    # loop through each situation
    for situation in situations:
        
        if situation == 'Leading':
            home_situation = 'Leading'
            away_situation = 'Trailing'
        if situation == 'Tied':
            home_situation = 'Tied'
            away_situation = 'Tied'
        if situation == 'Trailing':
            home_situation = 'Trailing'
            away_situation = 'Leading'
    
        # add a loop for each team
        for team in teams:
            
            if team == away:
                team_color = team_colors[0]
                situation = away_situation
        
            if team == home:
                team_color = team_colors[1]
                situation = home_situation
            
            # create a dataframe from the team stats file for generating toi values for the different game states
            team_toi_df = team_stats_df.copy()

            team_all_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == 'ALL') & (team_toi_df['SITUATION'] == situation)]
            team_all_toi = team_all_toi['TOI'].item()

            team_5v5_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == '5v5') & (team_toi_df['SITUATION'] == situation)]
            team_5v5_toi = team_5v5_toi['TOI'].item()

            team_PP_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == 'PP') & (team_toi_df['SITUATION'] == situation)]
            team_PP_toi = team_PP_toi['TOI'].item()

            team_SH_toi = team_toi_df[(team_toi_df['TEAM'] == team) & (team_toi_df['STATE'] == 'SH') & (team_toi_df['SITUATION'] == situation)]
            team_SH_toi = team_SH_toi['TOI'].item()

            # create a dataframe; filter for team; sort by team, game state and position; rank by time on ice and then invert the rankings
            team_df = players_df.copy()
            team_df = team_df[(team_df['TEAM'] == team) & (team_df['SITUATION'] == situation)]
    
            # remove zeros from the individual gamescore, onice gamescore and overall gamescore columns      
            team_df['iGS'] = team_df['iGS'].replace(0, np.NaN)       
            team_df['onGS'] = team_df['onGS'].replace(0, np.NaN)
            team_df['GS'] = team_df['GS'].replace(0, np.NaN)
            
            # create a filtered dataframe for each game state; sort by team, game state and position; rank by time on ice and then invert the rankings
            team_5v5_skaters_df = teams_5v5_skaters_df.copy()
            team_5v5_skaters_df = team_5v5_skaters_df[(team_5v5_skaters_df['TEAM'] == team) & (team_5v5_skaters_df['SITUATION'] == situation)]
            team_5v5_skaters_df = team_5v5_skaters_df.sort_values(by=['TOI'], ascending = True)
            team_5v5_skaters_df['RANK'] = team_5v5_skaters_df['TOI'].rank(method='first')
            team_5v5_skaters_df['RANK'] -= 1

            team_5v5_goalies_df = teams_5v5_goalies_df.copy()
            team_5v5_goalies_df = team_5v5_goalies_df[(team_5v5_goalies_df['TEAM'] == team) & (team_5v5_goalies_df['SITUATION'] == situation)]
            team_5v5_goalies_df = team_5v5_goalies_df.sort_values(by=['TOI'], ascending = True)
            team_5v5_goalies_df['RANK'] = team_5v5_goalies_df['TOI'].rank(method='first')
            team_5v5_goalies_df['RANK'] -= 1
                               
            team_PP_skaters_df = teams_PP_skaters_df.copy()
            team_PP_skaters_df = team_PP_skaters_df[(team_PP_skaters_df['TEAM'] == team) & (team_PP_skaters_df['SITUATION'] == situation)]
            team_PP_skaters_df = team_PP_skaters_df[(team_PP_skaters_df['TOI'] > 0)]
            team_PP_skaters_df = team_PP_skaters_df.sort_values(by=['TOI'], ascending = True)
            team_PP_skaters_df['RANK'] = team_PP_skaters_df['TOI'].rank(method='first')
            team_PP_skaters_df['RANK'] -= 1
    
            team_PP_goalies_df = teams_PP_goalies_df.copy()
            team_PP_goalies_df = team_PP_goalies_df[(team_PP_goalies_df['TEAM'] == team) & (team_PP_goalies_df['SITUATION'] == situation)]
            team_PP_goalies_df = team_PP_goalies_df[(team_PP_goalies_df['TOI'] > 0)]
            team_PP_goalies_df = team_PP_goalies_df.sort_values(by=['TOI'], ascending = True)
            team_PP_goalies_df['RANK'] = team_PP_goalies_df['TOI'].rank(method='first')
            team_PP_goalies_df['RANK'] -= 1
    
            team_SH_skaters_df = teams_SH_skaters_df.copy()
            team_SH_skaters_df = team_SH_skaters_df[(team_SH_skaters_df['TEAM'] == team) & (team_SH_skaters_df['SITUATION'] == situation)]
            team_SH_skaters_df = team_SH_skaters_df[(team_SH_skaters_df['TOI'] > 0)]
            team_SH_skaters_df = team_SH_skaters_df.sort_values(by=['TOI'], ascending = True)
            team_SH_skaters_df['RANK'] = team_SH_skaters_df['TOI'].rank(method='first')
            team_SH_skaters_df['RANK'] -= 1
    
            team_SH_goalies_df = teams_SH_goalies_df.copy()
            team_SH_goalies_df = team_SH_goalies_df[(team_SH_goalies_df['TEAM'] == team) & (team_SH_goalies_df['SITUATION'] == situation)]
            team_SH_goalies_df = team_SH_goalies_df[(team_SH_goalies_df['TOI'] > 0)]
            team_SH_goalies_df = team_SH_goalies_df.sort_values(by=['TOI'], ascending = True)
            team_SH_goalies_df['RANK'] = team_SH_goalies_df['TOI'].rank(method='first')
            team_SH_goalies_df['RANK'] -= 1
          
            # for each game state, create a dataframe with just the time on ice column; set a max value; scale each player's time on ice relative to the max
            toi_5v5_skaters = team_5v5_skaters_df['TOI']        
            max_toi_5v5_skaters = toi_5v5_skaters.max()
        
            toi_5v5_goalies = team_5v5_goalies_df['TOI']        
            max_toi_5v5_goalies = toi_5v5_goalies.max()
           
            toi_PP_skaters = team_PP_skaters_df['TOI']
            max_toi_PP_skaters = toi_PP_skaters.max()
    
            toi_PP_goalies = team_PP_goalies_df['TOI']
            max_toi_PP_goalies = toi_PP_goalies.max()
    
            toi_SH_skaters = team_SH_skaters_df['TOI']    
            max_toi_SH_skaters = toi_SH_skaters.max()
    
            toi_SH_goalies = team_SH_goalies_df['TOI']    
            max_toi_SH_goalies = toi_SH_goalies.max()
            
            # create a figure with six subplots arrangled complexly using a grid structure
            fig = plt.figure(figsize=(9,9))
            grid = plt.GridSpec(11, 8,  hspace=0.0, wspace=0.75)

            ax_5v5_skaters_gamescore = fig.add_subplot(grid[0:5, :-1])
            ax_5v5_skaters_toi = fig.add_subplot(grid[0:5, 7])        
        
            ax_5v5_goalies_gamescore = fig.add_subplot(grid[5:6, :-1])
            ax_5v5_goalies_toi = fig.add_subplot(grid[5:6, 7]) 
   
            ax_gap = fig.add_subplot(grid[6:7, :])
    
            ax_PP_skaters_gamescore = fig.add_subplot(grid[7:10, :2])
            ax_PP_skaters_toi = fig.add_subplot(grid[7:10, 2]) 
    
            ax_PP_goalies_gamescore = fig.add_subplot(grid[10:, :2])
            ax_PP_goalies_toi = fig.add_subplot(grid[10:, 2]) 
    
            ax_SH_skaters_gamescore = fig.add_subplot(grid[7:10, 5:-1])
            ax_SH_skaters_toi = fig.add_subplot(grid[7:10, 7]) 
    
            ax_SH_goalies_gamescore = fig.add_subplot(grid[10:, 5:-1])
            ax_SH_goalies_toi = fig.add_subplot(grid[10:, 7])             
            
            # set the plot title
            if team == away:
                fig.suptitle(date + ' GameScores (Away ' + situation + ')\n\n')       
            if team == home:
                fig.suptitle(date + ' GameScores (Home ' + situation + ')\n\n')       
    
            # set the axes titles
            ax_5v5_skaters_gamescore.set_title('5v5 GS', fontsize=10)
            ax_5v5_skaters_toi.set_title('5v5 TOI', fontsize=10)
        
            ax_5v5_goalies_gamescore.set_title('', fontsize=10)
            ax_5v5_goalies_toi.set_title('', fontsize=10)
  
            ax_PP_skaters_gamescore.set_title('PP GS', fontsize=10)
            ax_PP_skaters_toi.set_title('PP TOI', fontsize=10)
    
            ax_PP_goalies_gamescore.set_title('', fontsize=10)
            ax_PP_goalies_toi.set_title('', fontsize=10)
    
            ax_SH_skaters_gamescore.set_title('SH GS', fontsize=10)
            ax_SH_skaters_toi.set_title('SH TOI', fontsize=10)
    
            ax_SH_goalies_gamescore.set_title('', fontsize=10)
            ax_SH_goalies_toi.set_title('', fontsize=10)

            # ensure the gap axis is transparent
            ax_gap.set_facecolor('None')
           
            # for each state, plot the bars for total gamescore
            try:
                GS_5v5_skaters_plot = team_5v5_skaters_df.plot.barh(x='PLAYER', y='GS', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_skaters_gamescore);
            except:
                pass 
            try:
                GS_5v5_goalies_plot = team_5v5_goalies_df.plot.barh(x='PLAYER', y='GS', color=team_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_5v5_goalies_gamescore);
            except:
                pass 

            if team_PP_toi != 0:
                try:
                    GS_PP_skaters_plot = team_PP_skaters_df.plot.barh(x='PLAYER', y='GS', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_skaters_gamescore);
                except:
                    pass 
                try:
                    GS_PP_goalies_plot = team_PP_goalies_df.plot.barh(x='PLAYER', y='GS', color=team_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_PP_goalies_gamescore);
                except:
                    pass 
            if team_SH_toi != 0:
                try:
                    GS_SH_skaters_plot = team_SH_skaters_df.plot.barh(x='PLAYER', y='GS', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_SH_skaters_gamescore);
                except:
                    pass
                try:
                    GS_SH_goalies_plot = team_SH_goalies_df.plot.barh(x='PLAYER', y='GS', color=team_color, edgecolor='None', width=0.25, legend=None, label='', ax=ax_SH_goalies_gamescore);
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
           
            if team_PP_toi != 0:
                try:
                    toi_PP_skaters_plot = team_PP_skaters_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_PP_skaters_toi);
                except:
                    pass
                try:
                    toi_PP_goalies_plot = team_PP_goalies_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_PP_goalies_toi);
                except:
                    pass

            if team_SH_toi != 0:
                try:
                    toi_SH_skaters_plot = team_SH_skaters_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_SH_skaters_toi);
                except:
                    pass
                try:
                    toi_SH_goalies_plot = team_SH_goalies_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_SH_goalies_toi);
                except:
                    pass
            
            # set / remove the y-labels for the subplots
            ax_5v5_skaters_gamescore.set_xlabel('')
            ax_5v5_skaters_gamescore.set_ylabel('', fontsize=10)
            ax_5v5_skaters_toi.set_xlabel('')
            ax_5v5_skaters_toi.set_ylabel('')
    
            ax_5v5_goalies_gamescore.set_xlabel('')
            ax_5v5_goalies_gamescore.set_ylabel('', fontsize=10)
            ax_5v5_goalies_toi.set_xlabel('')
            ax_5v5_goalies_toi.set_ylabel('')

            ax_gap.set_xlabel('')
            ax_gap.set_ylabel('', fontsize=10)

            ax_PP_skaters_gamescore.set_xlabel('')
            ax_PP_skaters_gamescore.set_ylabel('', fontsize=10)
            ax_PP_skaters_toi.set_xlabel('')
            ax_PP_skaters_toi.set_ylabel('')
    
            ax_PP_goalies_gamescore.set_xlabel('')
            ax_PP_goalies_gamescore.set_ylabel('', fontsize=10)
            ax_PP_goalies_toi.set_xlabel('')
            ax_PP_goalies_toi.set_ylabel('')
    
            ax_SH_skaters_gamescore.set_xlabel('')
            ax_SH_skaters_gamescore.set_ylabel('', fontsize=10)
            ax_SH_skaters_toi.set_xlabel('')
            ax_SH_skaters_toi.set_ylabel('')
    
            ax_SH_goalies_gamescore.set_xlabel('')
            ax_SH_goalies_gamescore.set_ylabel('', fontsize=10)
            ax_SH_goalies_toi.set_xlabel('')
            ax_SH_goalies_toi.set_ylabel('')
            
            # set vertical indicators for break-even gamescore
            ax_5v5_skaters_gamescore.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            ax_5v5_goalies_gamescore.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            
            ax_PP_skaters_gamescore.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            ax_PP_goalies_gamescore.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            
            ax_SH_skaters_gamescore.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            ax_SH_goalies_gamescore.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
            
            # change the tick parameters for each axes
            ax_5v5_skaters_gamescore.tick_params(
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

            ax_5v5_goalies_gamescore.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=True) # labels along the bottom edge are off
            ax_5v5_goalies_toi.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelleft=False,   # labels along the left edge are off
                labelbottom=True) # labels along the bottom edge are off

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
   
            ax_PP_skaters_gamescore.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=False)  # labels along the bottom edge are on
            ax_PP_skaters_toi.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelleft=False,   # labels along the left edge are off            
                labelbottom=False)  # labels along the bottom edge are off
    
            ax_PP_goalies_gamescore.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=True) # labels along the bottom edge are on
            ax_PP_goalies_toi.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelleft=False,   # labels along the left edge are off            
                labelbottom=True) # labels along the bottom edge are on
    
            ax_SH_skaters_gamescore.tick_params(
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
    
            ax_SH_goalies_gamescore.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=True) # labels along the bottom edge are on
            ax_SH_goalies_toi.tick_params(
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelleft=False,   # labels along the left edge are off
                labelbottom=True) # labels along the bottom edge are on
    
            # create a list of x-axis tick values contingent on the max values for gamescore       
            GS_5v5_maxmin = teams_5v5_df['GS']
            GS_5v5_max = round(GS_5v5_maxmin.max(), 1)
            GS_5v5_min = abs(round(GS_5v5_maxmin.min(), 1))
    
            GS_5v5_tickmax = int()
            GS_5v5_tickmin = int()
            if GS_5v5_max >= GS_5v5_min:
                GS_5v5_tickmax = GS_5v5_max
                GS_5v5_tickmin = GS_5v5_max * -1
            if GS_5v5_max < GS_5v5_min:
                GS_5v5_tickmax = GS_5v5_min
                GS_5v5_tickmin = GS_5v5_min * -1
            
            GS_5v5_ticklabels = [GS_5v5_tickmin, round((GS_5v5_tickmin / 2), 1), 0, round((GS_5v5_tickmax / 2), 1), GS_5v5_tickmax]
                
            toi_5v5_skaters_tickmax = max_toi_5v5_skaters
    
            toi_5v5_skaters_ticklabels = []
            if toi_5v5_skaters_tickmax <= 10:
                toi_5v5_skaters_ticklabels = [0, 10]
            if toi_5v5_skaters_tickmax > 10 and toi_5v5_skaters_tickmax <= 15:
                toi_5v5_skaters_ticklabels = [0, 15]
            if toi_5v5_skaters_tickmax > 15 and toi_5v5_skaters_tickmax <= 20:
                toi_5v5_skaters_ticklabels = [0, 20]
            if toi_5v5_skaters_tickmax > 20 and toi_5v5_skaters_tickmax <= 25:
                toi_5v5_skaters_ticklabels = [0, 25]
            if toi_5v5_skaters_tickmax > 25 and toi_5v5_skaters_tickmax <= 30:
                toi_5v5_skaters_ticklabels = [0, 30]
    
            toi_5v5_goalies_tickmax = max_toi_5v5_goalies
    
            toi_5v5_goalies_ticklabels = []
            if toi_5v5_goalies_tickmax <= 10:
                toi_5v5_goalies_ticklabels = [0, 10]
            if toi_5v5_goalies_tickmax > 10 and toi_5v5_goalies_tickmax <= 15:
                toi_5v5_goalies_ticklabels = [0, 15]
            if toi_5v5_goalies_tickmax > 15 and toi_5v5_goalies_tickmax <= 20:
                toi_5v5_goalies_ticklabels = [0, 20]
            if toi_5v5_goalies_tickmax > 20 and toi_5v5_goalies_tickmax <= 25:
                toi_5v5_goalies_ticklabels = [0, 25]
            if toi_5v5_goalies_tickmax > 25 and toi_5v5_goalies_tickmax <= 30:
                toi_5v5_goalies_ticklabels = [0, 30]
            if toi_5v5_goalies_tickmax > 30 and toi_5v5_goalies_tickmax <= 35:
                toi_5v5_goalies_ticklabels = [0, 35]
            if toi_5v5_goalies_tickmax > 35 and toi_5v5_goalies_tickmax <= 40:
                toi_5v5_goalies_ticklabels = [0, 40]
            if toi_5v5_goalies_tickmax > 40 and toi_5v5_goalies_tickmax <= 45:
                toi_5v5_goalies_ticklabels = [0, 45]
            if toi_5v5_goalies_tickmax > 45 and toi_5v5_goalies_tickmax <= 50:
                toi_5v5_goalies_ticklabels = [0, 50]
            if toi_5v5_goalies_tickmax > 50 and toi_5v5_goalies_tickmax <= 55:
                toi_5v5_goalies_ticklabels = [0, 55]
            if toi_5v5_goalies_tickmax > 55 and toi_5v5_goalies_tickmax <= 60:
                toi_5v5_goalies_ticklabels = [0, 60]
                
            GS_PP_maxmin = teams_PP_df['GS']
            GS_PP_max = round(GS_PP_maxmin.max(), 1)
            GS_PP_min = abs(round(GS_PP_maxmin.min(), 1))
            
            GS_PP_tickmax = int()
            GS_PP_tickmin = int()
            if GS_PP_max >= GS_PP_min:
                GS_PP_tickmax = GS_PP_max
                GS_PP_tickmin = GS_PP_max * -1
            if GS_PP_max < GS_PP_min:
                GS_PP_tickmax = GS_PP_min
                GS_PP_tickmin = GS_PP_min * -1
    
            GS_PP_ticklabels = [GS_PP_tickmin, round((GS_PP_tickmin / 2), 1), 0, round((GS_PP_tickmax / 2), 1), GS_PP_tickmax]
    
            GS_SH_maxmin = teams_SH_df['GS']
            GS_SH_max = round(GS_SH_maxmin.max(), 1)
            GS_SH_min = abs(round(GS_SH_maxmin.min(), 1))
    
            GS_SH_tickmax = int()
            GS_SH_tickmin = int()
            if GS_SH_max >= GS_SH_min:
                GS_SH_tickmax = GS_SH_max
                GS_SH_tickmin = GS_SH_max * -1
            if GS_SH_max < GS_SH_min:
                GS_SH_tickmax = GS_SH_min
                GS_SH_tickmin = GS_SH_min * -1
    
            GS_SH_ticklabels = [GS_SH_tickmin, round((GS_SH_tickmin / 2), 1), 0, round((GS_SH_tickmax / 2), 1), GS_SH_tickmax]            
               
            toi_PP_skaters_tickmax = max_toi_PP_skaters
    
            toi_SH_skaters_tickmax = max_toi_SH_skaters
    
            toi_specialteams_skaters_tickmax = int()
            if toi_PP_skaters_tickmax >= toi_SH_skaters_tickmax:
                toi_specialteams_skaters_tickmax = toi_PP_skaters_tickmax
            if toi_PP_skaters_tickmax < toi_SH_skaters_tickmax:
                toi_specialteams_skaters_tickmax = toi_SH_skaters_tickmax
    
            toi_specialteams_skaters_ticklabels = []
            if toi_specialteams_skaters_tickmax <= 2:
                toi_specialteams_skaters_ticklabels = [0, 2]
            if toi_specialteams_skaters_tickmax > 2 and toi_specialteams_skaters_tickmax <= 4:
                toi_specialteams_skaters_ticklabels = [0, 4]
            if toi_specialteams_skaters_tickmax > 4 and toi_specialteams_skaters_tickmax <= 6:
                toi_specialteams_skaters_ticklabels = [0, 6]
            if toi_specialteams_skaters_tickmax > 6 and toi_specialteams_skaters_tickmax <= 8:
                toi_specialteams_skaters_ticklabels = [0, 8]
            if toi_specialteams_skaters_tickmax > 8 and toi_specialteams_skaters_tickmax <= 10:
                toi_specialteams_skaters_ticklabels = [0, 10]
            if toi_specialteams_skaters_tickmax > 10 and toi_specialteams_skaters_tickmax <= 12:
                toi_specialteams_skaters_ticklabels = [0, 12]
    
            toi_PP_goalies_tickmax = max_toi_PP_goalies
    
            toi_SH_goalies_tickmax = max_toi_SH_goalies
    
            toi_specialteams_goalies_tickmax = int()
            if toi_PP_goalies_tickmax >= toi_SH_goalies_tickmax:
                toi_specialteams_goalies_tickmax = toi_PP_goalies_tickmax
            if toi_PP_goalies_tickmax < toi_SH_goalies_tickmax:
                toi_specialteams_goalies_tickmax = toi_SH_goalies_tickmax
    
            toi_specialteams_goalies_ticklabels = []
            if toi_specialteams_goalies_tickmax <= 2:
                toi_specialteams_goalies_ticklabels = [0, 2]
            if toi_specialteams_goalies_tickmax > 2 and toi_specialteams_goalies_tickmax <= 4:
                toi_specialteams_goalies_ticklabels = [0, 4]
            if toi_specialteams_goalies_tickmax > 4 and toi_specialteams_goalies_tickmax <= 6:
                toi_specialteams_goalies_ticklabels = [0, 6]
            if toi_specialteams_goalies_tickmax > 6 and toi_specialteams_goalies_tickmax <= 8:
                toi_specialteams_goalies_ticklabels = [0, 8]
            if toi_specialteams_goalies_tickmax > 8 and toi_specialteams_goalies_tickmax <= 10:
                toi_specialteams_goalies_ticklabels = [0, 10]
            if toi_specialteams_goalies_tickmax > 10 and toi_specialteams_goalies_tickmax <= 12:
                toi_specialteams_goalies_ticklabels = [0, 12]

            # set vertical indicator for midpoint of time on ice max
            ax_5v5_skaters_toi.axvspan(toi_5v5_skaters_ticklabels[1] / 2, toi_5v5_skaters_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_5v5_skaters_toi.axvspan(toi_5v5_skaters_ticklabels[1], toi_5v5_skaters_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
    
            ax_5v5_goalies_toi.axvspan(toi_5v5_goalies_ticklabels[1] / 2, toi_5v5_goalies_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_5v5_goalies_toi.axvspan(toi_5v5_goalies_ticklabels[1], toi_5v5_goalies_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

            ax_PP_skaters_toi.axvspan(toi_specialteams_skaters_ticklabels[1] / 2, toi_specialteams_skaters_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_PP_skaters_toi.axvspan(toi_specialteams_skaters_ticklabels[1], toi_specialteams_skaters_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
  
            ax_PP_goalies_toi.axvspan(toi_specialteams_goalies_ticklabels[1] / 2, toi_specialteams_goalies_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_PP_goalies_toi.axvspan(toi_specialteams_goalies_ticklabels[1], toi_specialteams_goalies_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

            ax_SH_skaters_toi.axvspan(toi_specialteams_skaters_ticklabels[1] / 2, toi_specialteams_skaters_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_SH_skaters_toi.axvspan(toi_specialteams_skaters_ticklabels[1], toi_specialteams_skaters_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
    
            ax_SH_goalies_toi.axvspan(toi_specialteams_goalies_ticklabels[1] / 2, toi_specialteams_goalies_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
            ax_SH_goalies_toi.axvspan(toi_specialteams_goalies_ticklabels[1], toi_specialteams_goalies_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
              
            # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
            ax_5v5_skaters_gamescore.set_xticks(GS_5v5_ticklabels, minor=False)
            ax_5v5_skaters_toi.set_xticks(toi_5v5_skaters_ticklabels, minor=False)
    
            ax_5v5_goalies_gamescore.set_xticks(GS_5v5_ticklabels, minor=False)
            ax_5v5_goalies_toi.set_xticks(toi_5v5_goalies_ticklabels, minor=False)

            ax_PP_skaters_gamescore.set_xticks(GS_PP_ticklabels, minor=False)
            ax_PP_skaters_toi.set_xticks(toi_specialteams_skaters_ticklabels, minor=False)
        
            ax_PP_goalies_gamescore.set_xticks(GS_PP_ticklabels, minor=False)
            ax_PP_goalies_toi.set_xticks(toi_specialteams_goalies_ticklabels, minor=False)

            ax_SH_skaters_gamescore.set_xticks(GS_SH_ticklabels, minor=False)
            ax_SH_skaters_toi.set_xticks(toi_specialteams_skaters_ticklabels, minor=False)
        
            ax_SH_goalies_gamescore.set_xticks(GS_SH_ticklabels, minor=False)
            ax_SH_goalies_toi.set_xticks(toi_specialteams_goalies_ticklabels, minor=False)
 
            # remove axes ticks for instances where there is no special teams play    
            if team_PP_toi == 0:            
                ax_PP_skaters_gamescore.set_xticks([], minor=False)
                ax_PP_skaters_gamescore.set_yticks([], minor=False)               
                ax_PP_skaters_toi.set_xticks([], minor=False)
                ax_PP_skaters_toi.set_yticks([], minor=False)
        
                ax_PP_goalies_gamescore.set_xticks([], minor=False)
                ax_PP_goalies_gamescore.set_yticks([], minor=False)
                ax_PP_goalies_toi.set_xticks([], minor=False)
                ax_PP_goalies_toi.set_yticks([], minor=False)

            if team_SH_toi == 0:            
                ax_SH_skaters_gamescore.set_xticks([], minor=False)
                ax_SH_skaters_gamescore.set_yticks([], minor=False)
                ax_SH_skaters_toi.set_xticks([], minor=False)
                ax_SH_skaters_toi.set_yticks([], minor=False)
        
                ax_SH_goalies_gamescore.set_xticks([], minor=False)
                ax_SH_goalies_gamescore.set_yticks([], minor=False)
                ax_SH_goalies_toi.set_xticks([], minor=False)
                ax_SH_goalies_toi.set_yticks([], minor=False)

            # remove the borders to each subplot
            ax_5v5_skaters_gamescore.spines["top"].set_visible(False)   
            ax_5v5_skaters_gamescore.spines["bottom"].set_visible(False)    
            ax_5v5_skaters_gamescore.spines["right"].set_visible(False)    
            ax_5v5_skaters_gamescore.spines["left"].set_visible(False)  
            ax_5v5_skaters_toi.spines["top"].set_visible(False)   
            ax_5v5_skaters_toi.spines["bottom"].set_visible(False)    
            ax_5v5_skaters_toi.spines["right"].set_visible(False)    
            ax_5v5_skaters_toi.spines["left"].set_visible(False) 

            ax_5v5_goalies_gamescore.spines["top"].set_visible(False)   
            ax_5v5_goalies_gamescore.spines["bottom"].set_visible(False)    
            ax_5v5_goalies_gamescore.spines["right"].set_visible(False)    
            ax_5v5_goalies_gamescore.spines["left"].set_visible(False)  
            ax_5v5_goalies_toi.spines["top"].set_visible(False)   
            ax_5v5_goalies_toi.spines["bottom"].set_visible(False)    
            ax_5v5_goalies_toi.spines["right"].set_visible(False)    
            ax_5v5_goalies_toi.spines["left"].set_visible(False)

            ax_gap.spines["top"].set_visible(False)   
            ax_gap.spines["bottom"].set_visible(False)    
            ax_gap.spines["right"].set_visible(False)    
            ax_gap.spines["left"].set_visible(False)  

            ax_PP_skaters_gamescore.spines["top"].set_visible(False)   
            ax_PP_skaters_gamescore.spines["bottom"].set_visible(False)    
            ax_PP_skaters_gamescore.spines["right"].set_visible(False)    
            ax_PP_skaters_gamescore.spines["left"].set_visible(False) 
            ax_PP_skaters_toi.spines["top"].set_visible(False)   
            ax_PP_skaters_toi.spines["bottom"].set_visible(False)    
            ax_PP_skaters_toi.spines["right"].set_visible(False)    
            ax_PP_skaters_toi.spines["left"].set_visible(False) 
    
            ax_PP_goalies_gamescore.spines["top"].set_visible(False)   
            ax_PP_goalies_gamescore.spines["bottom"].set_visible(False)    
            ax_PP_goalies_gamescore.spines["right"].set_visible(False)    
            ax_PP_goalies_gamescore.spines["left"].set_visible(False) 
            ax_PP_goalies_toi.spines["top"].set_visible(False)   
            ax_PP_goalies_toi.spines["bottom"].set_visible(False)    
            ax_PP_goalies_toi.spines["right"].set_visible(False)    
            ax_PP_goalies_toi.spines["left"].set_visible(False) 
    
            ax_SH_skaters_gamescore.spines["top"].set_visible(False)   
            ax_SH_skaters_gamescore.spines["bottom"].set_visible(False)    
            ax_SH_skaters_gamescore.spines["right"].set_visible(False)    
            ax_SH_skaters_gamescore.spines["left"].set_visible(False) 
            ax_SH_skaters_toi.spines["top"].set_visible(False)   
            ax_SH_skaters_toi.spines["bottom"].set_visible(False)    
            ax_SH_skaters_toi.spines["right"].set_visible(False)    
            ax_SH_skaters_toi.spines["left"].set_visible(False) 
    
            ax_SH_goalies_gamescore.spines["top"].set_visible(False)   
            ax_SH_goalies_gamescore.spines["bottom"].set_visible(False)    
            ax_SH_goalies_gamescore.spines["right"].set_visible(False)    
            ax_SH_goalies_gamescore.spines["left"].set_visible(False) 
            ax_SH_goalies_toi.spines["top"].set_visible(False)   
            ax_SH_goalies_toi.spines["bottom"].set_visible(False)    
            ax_SH_goalies_toi.spines["right"].set_visible(False)    
            ax_SH_goalies_toi.spines["left"].set_visible(False) 
           
            # add text boxes with team names in white and with the team's color in the background
            fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
            fig.text(.525, 0.936, ' ' + home + ' ', color='white', fontsize='12', bbox=dict(facecolor=home_color, edgecolor='None'))
            fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))
    
    
            ###
            ### SAVE TO FILE
            ###
            
            if team == away:
                plt.savefig(charts_players_composite_situation + 'gamescores_away_' + situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
            elif team == home:
                plt.savefig(charts_players_composite_situation + 'gamescores_home_' + situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)    
            
            # exercise a command-line option to show the current figure
            if images == 'show':
                plt.show()
    
    
            ###
            ### CLOSE
            ###
            
            plt.close(fig)
            
            # status update
            print('Plotting ' + team + ' ' + situation.lower() + ' gamescores for players.')   
        
    # status update
    print('Finished plotting player gamescores by situation for ' + season_id + ' ' + game_id)