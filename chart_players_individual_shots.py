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
    charts_players_individual = parameters.charts_players_individual
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
    players_file = files_root + 'stats_players_individual.csv'
    
    # create a dataframe object that reads in info from the .csv files
    players_df = pd.read_csv(players_file)

    skaters_5v5_df = players_df.copy()
    skaters_5v5_df = skaters_5v5_df[(skaters_5v5_df['STATE'] == '5v5') & (skaters_5v5_df['POS'] != 'G')]
    max_5v5_toi = skaters_5v5_df['TOI'].max()     

    skaters_PP_df = players_df.copy()
    skaters_PP_df = skaters_PP_df[(skaters_PP_df['STATE'] == 'PP') & (skaters_PP_df['POS'] != 'G')]
    max_PP_toi = skaters_PP_df['TOI'].max()     

    skaters_SH_df = players_df.copy()
    skaters_SH_df = skaters_SH_df[(skaters_SH_df['STATE'] == 'PP') & (skaters_SH_df['POS'] != 'G')]
    max_SH_toi = skaters_SH_df['TOI'].max()     
    
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
    
        if team == home:
            team_color = team_colors[1]
    
        # create a dataframe; filter for team; sort by team, game state and position; rank by time on ice and then invert the rankings
        team_df = players_df.copy()
        team_df = team_df[(team_df['TEAM'] == team) & (team_df['POS'] != 'G')]

        # create columns for saved, missed and blocked shots; remove zeros from all the columns intended for plotting
        team_df['SS'] = team_df['ONS'] - team_df['G']
        team_df['MS'] = team_df['US'] - team_df['ONS']
        team_df['BS'] = team_df['S'] - team_df['US']
        
        team_df['G'] = team_df['G'].replace(0, np.NaN)
        team_df['SS'] = team_df['SS'].replace(0, np.NaN)
        team_df['MS'] = team_df['MS'].replace(0, np.NaN)
        team_df['BS'] = team_df['BS'].replace(0, np.NaN)

        # create a filtered dataframe for each game state; sort by team, game state and position; rank by time on ice and then invert the rankings
        team_5v5_df = team_df.copy()
        team_5v5_df = team_5v5_df[(team_5v5_df['STATE'] == '5v5')]
        team_5v5_df = team_5v5_df.sort_values(by=['TOI'], ascending = True)
        team_5v5_df['RANK'] = team_5v5_df['TOI'].rank(method='first')
        team_5v5_df['RANK'] -= 1
        
        team_PP_df = team_df.copy()
        team_PP_df = team_PP_df[(team_PP_df['STATE'] == 'PP') & (team_PP_df['TOI'] > 0)]
        team_PP_df = team_PP_df.sort_values(by=['TOI'], ascending = True)
        team_PP_df = team_PP_df.iloc[-10:]  
        team_PP_df['RANK'] = team_PP_df['TOI'].rank(method='first')
        team_PP_df['RANK'] -= 1

        team_SH_df = team_df.copy()
        team_SH_df = team_SH_df[(team_SH_df['STATE'] == 'SH') & (team_SH_df['TOI'] > 0)]
        team_SH_df = team_SH_df.sort_values(by=['TOI'], ascending = True)
        team_SH_df = team_SH_df.iloc[-10:]
        team_SH_df['RANK'] = team_SH_df['TOI'].rank(method='first')
        team_SH_df['RANK'] -= 1

        # for each game state, create a dataframe with just the time on ice column; set a max value; scale each player's time on ice relative to the max
        toi_5v5 = team_5v5_df['TOI']        
        max_toi_5v5 = toi_5v5.max()
        
        toi_PP = team_PP_df['TOI']
        max_toi_PP = toi_PP.max()
        team_PP_toi = max_toi_PP

        toi_SH = team_SH_df['TOI']    
        max_toi_SH = toi_SH.max()
        team_SH_toi = max_toi_SH
        
        # create a figure with six subplots arrangled complexly using a grid structure
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(5, 8,  hspace=0.75, wspace=0.75)

        ax_5v5_shots = fig.add_subplot(grid[0:-2, :-1])
        ax_5v5_toi = fig.add_subplot(grid[0:-2, 7])        

        ax_PP_shots = fig.add_subplot(grid[3:, :2])
        ax_PP_toi = fig.add_subplot(grid[3:, 2]) 

        ax_SH_shots = fig.add_subplot(grid[3:, 5:-1])
        ax_SH_toi = fig.add_subplot(grid[3:, 7]) 
        
        # set the plot title
        fig.suptitle(date + ' Skaters Individual Shots\n\n')       

        # set the axes titles
        ax_5v5_shots.set_title('5v5 S', fontsize=10)
        ax_5v5_toi.set_title('5v5 TOI', fontsize=10)

        ax_PP_shots.set_title('PP S', fontsize=10)
        ax_PP_toi.set_title('PP TOI', fontsize=10)

        ax_SH_shots.set_title('SH S', fontsize=10)
        ax_SH_toi.set_title('SH TOI', fontsize=10)
        
        # create markers for the plot legend
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


        # for each state, plot the bars for total shots and markers for saved, missed and blocked shots markers
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
        try:
            toi_5v5_plot = team_5v5_df.plot.barh(x='PLAYER', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_5v5_toi);
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
        ax_5v5_shots.set_xlabel('')
        ax_5v5_shots.set_ylabel('', fontsize=10)
        ax_5v5_toi.set_xlabel('')
        ax_5v5_toi.set_ylabel('')

        ax_PP_shots.set_xlabel('')
        ax_PP_shots.set_ylabel('', fontsize=10)
        ax_PP_toi.set_xlabel('')
        ax_PP_toi.set_ylabel('')

        ax_SH_shots.set_xlabel('')
        ax_SH_shots.set_ylabel('', fontsize=10)
        ax_SH_toi.set_xlabel('')
        ax_SH_toi.set_ylabel('')
           
        # change the tick parameters for each axes
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
        ax_5v5_shots.tick_params(
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
        S_5v5_max = team_5v5_df['S']
        S_5v5_tickmax = S_5v5_max.max()

        S_5v5_ticklabels = []
        if S_5v5_tickmax <= 10:
            S_5v5_ticklabels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if S_5v5_tickmax > 10 and S_5v5_tickmax <= 20:
            S_5v5_ticklabels = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

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
        ax_5v5_toi.axvspan(toi_5v5_ticklabels[1] / 2, toi_5v5_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_5v5_toi.axvspan(toi_5v5_ticklabels[1], toi_5v5_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_PP_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_PP_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_SH_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_SH_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
          
        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_5v5_shots.set_xticks(S_5v5_ticklabels, minor=False)
        ax_5v5_toi.set_xticks(toi_5v5_ticklabels, minor=False)
        
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
        ax_5v5_shots.spines["top"].set_visible(False)   
        ax_5v5_shots.spines["bottom"].set_visible(False)    
        ax_5v5_shots.spines["right"].set_visible(False)    
        ax_5v5_shots.spines["left"].set_visible(False)  
        ax_5v5_toi.spines["top"].set_visible(False)   
        ax_5v5_toi.spines["bottom"].set_visible(False)    
        ax_5v5_toi.spines["right"].set_visible(False)    
        ax_5v5_toi.spines["left"].set_visible(False) 
        
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
        ax_5v5_shots.legend(loc='center', bbox_to_anchor=(.55, -.9), ncol=4).get_frame().set_linewidth(0.0)

        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))


        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_players_individual + 'skaters_individual_shots_away.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_players_individual + 'skaters_individual_shots_home.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()


        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' skaters individual shots.')   
        
    # status update
    print('Finished plotting the individual shots for skaters.')