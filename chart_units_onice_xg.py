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
    charts_units = parameters.charts_units
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
    lines_file = files_root + 'stats_units_lines_onice.csv'
    pairings_file = files_root + 'stats_units_pairings_onice.csv'
    pk_file = files_root + 'stats_units_pk_onice.csv'
    pp_file = files_root + 'stats_units_pp_onice.csv'
    
    # create a dataframe object that reads in info from the .csv files
    lines_df = pd.read_csv(lines_file)
    pairings_df = pd.read_csv(pairings_file)
    PP_df = pd.read_csv(pp_file)
    PK_df = pd.read_csv(pk_file)    

    max_lines_toi = lines_df['TOI'].max()      
    max_pairings_toi = pairings_df['TOI'].max()      
    max_PP_toi = PP_df['TOI'].max()      
    max_PK_toi = PK_df['TOI'].max()

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
    ### 5v5, PP, PK
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
        team_lines_df = lines_df.copy()
        team_lines_df = team_lines_df[(team_lines_df['TEAM'] == team)]  
        team_lines_df = team_lines_df.sort_values(by=['TOI'], ascending = True)
        team_lines_df = team_lines_df.iloc[-4:]      
        team_lines_df['RANK'] = team_lines_df['TOI'].rank(method='first')
        team_lines_df = team_lines_df.sort_values(by=['RANK'], ascending = True)
        team_lines_df['RANK'] -= 1

        # remove zeros from the differential column       
        team_lines_df['xGD'] = team_lines_df['xGD'].replace(0, np.NaN)       
        
        # make shots against negative values    
        team_lines_df['GA'] *= -1
        team_lines_df['xGA'] *= -1
        
        # find the max toi value       
        team_max_lines_toi = team_lines_df['TOI'].max()
                      
        # create a pairings dataframe; filter for team; sort by time on ice; keep the pairs with the 3 highest totals; rank and then invert the rankings   
        team_pairings_df = pairings_df.copy()
        team_pairings_df = team_pairings_df[(team_pairings_df['TEAM'] == team)]
        team_pairings_df = team_pairings_df.sort_values(by=['TOI'], ascending = True)
        team_pairings_df = team_pairings_df.iloc[-3:]    
        team_pairings_df['RANK'] = team_pairings_df['TOI'].rank(method='first')
        team_pairings_df['RANK'] -= 1

        # remove zeros from the differential column       
        team_pairings_df['xGD'] = team_pairings_df['xGD'].replace(0, np.NaN)       
        
        # make expected goals against negative values    
        team_pairings_df['GA'] *= -1
        team_pairings_df['xGA'] *= -1

        # find the max toi value       
        team_max_pairings_toi = team_pairings_df['TOI'].max()

        # create a power play units dataframe; filter for team; sort by time on ice; keep the units with the 4 highest totals; rank and then invert the rankings   
        team_PP_df = PP_df.copy()
        team_PP_df = team_PP_df[(team_PP_df['TEAM'] == team)]
        team_PP_df = team_PP_df.sort_values(by=['TOI'], ascending = True)
        team_PP_df = team_PP_df.iloc[-4:]    
        team_PP_df['RANK'] = team_PP_df['TOI'].rank(method='first')
        team_PP_df['RANK'] -= 1

        # remove zeros from the differential column       
        team_PP_df['xGD'] = team_PP_df['xGD'].replace(0, np.NaN)       

        # make expected goals against negative values    
        team_PP_df['GA'] *= -1
        team_PP_df['xGA'] *= -1

        # find the max toi value       
        team_max_PP_toi = team_PP_df['TOI'].max()

        # create a penalty kill units dataframe; filter for team; sort by time on ice; keep the units with the 4 highest totals; rank and then invert the rankings   
        team_PK_df = PK_df.copy()

        team_PK_df = team_PK_df[(team_PK_df['TEAM'] == team)]
        team_PK_df = team_PK_df.sort_values(by=['TOI'], ascending = True)
        team_PK_df = team_PK_df.iloc[-4:]    
        team_PK_df['RANK'] = team_PK_df['TOI'].rank(method='first')
        team_PK_df['RANK'] -= 1
 
        # remove zeros from the differential column       
        team_PK_df['xGD'] = team_PK_df['xGD'].replace(0, np.NaN)       
      
        # make expected goals against negative values    
        team_PK_df['GA'] *= -1
        team_PK_df['xGA'] *= -1

        # find the max toi value       
        team_max_PK_toi = team_PK_df['TOI'].max()

        # create a figure with six subplots arrangled complexly using a grid structure
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(4, 8, hspace=0.75, wspace=0.50)

        ax_5v5_lines_xG = fig.add_subplot(grid[0, 0:-2])
        ax_5v5_lines_toi = fig.add_subplot(grid[0, -1])

        ax_5v5_pairings_xG = fig.add_subplot(grid[1, 0:-2])
        ax_5v5_pairings_toi = fig.add_subplot(grid[1, -1])
        
        ax_PP_xG = fig.add_subplot(grid[2, 0:-2])
        ax_PP_toi = fig.add_subplot(grid[2, -1]) 

        ax_PK_xG = fig.add_subplot(grid[3, 0:-2])
        ax_PK_toi = fig.add_subplot(grid[3, -1]) 
        
        # set the plot title
        fig.suptitle(date + ' Unit On-Ice Expected Goals\n\n')       

        # set the axes titles
        ax_5v5_lines_xG.set_title('5v5 xG', fontsize=10)
        ax_5v5_lines_toi.set_title('5v5 TOI', fontsize=10)

        ax_PP_xG.set_title('PP xG', fontsize=10)
        ax_PP_toi.set_title('PP TOI', fontsize=10)

        ax_PK_xG.set_title('SH xG', fontsize=10)
        ax_PK_toi.set_title('SH TOI', fontsize=10)
        
        # for each state, plot the bars for total shots and markers for saved, missed and blocked shots markers
        try:
            xGF_5v5_lines_plot = team_lines_df.plot.barh(x='LINE', y='xGF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_lines_xG);
        except:
            pass 
        try:
            xGA_5v5_lines_plot = team_lines_df.plot.barh(x='LINE', y='xGA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_5v5_lines_xG);
        except:
            pass
        try:
            xGD_5v5_lines_plot = team_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=13, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_lines_xG);
        except:
            pass

        try:
            xGF_5v5_pairings_plot = team_pairings_df.plot.barh(x='PAIRING', y='xGF', color=team_color, edgecolor='None', width=0.5, legend=None, label='', ax=ax_5v5_pairings_xG);
        except:
            pass 
        try:
            xGA_5v5_pairings_plot = team_pairings_df.plot.barh(x='PAIRING', y='xGA', color=opponent_color, edgecolor='None', width=0.5, legend=None, label='', ax=ax_5v5_pairings_xG);
        except:
            pass
        try:
            xGD_5v5_pairings_plot = team_pairings_df.plot(x='xGD', y='RANK', marker='|', markersize=13, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_5v5_pairings_xG);
        except:
            pass

        try:
            xGF_PP_plot = team_PP_df.plot.barh(x='UNIT', y='xGF', color=team_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_xG);
        except:
            pass 
        try:
            xGA_PP_plot = team_PP_df.plot.barh(x='UNIT', y='xGA', color=opponent_color, edgecolor='None', width=0.75, legend=None, label='', ax=ax_PP_xG);
        except:
            pass 
        try:
            xGD_PP_marker = team_PP_df.plot(x='xGD', y='RANK', marker='|', markersize=13, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PP_xG);
        except:
            pass

        try:
            xGF_PK_plot = team_PK_df.plot.barh(x='UNIT', y='xGF', color=team_color, edgecolor='None', width=0.5, legend=None, label='', ax=ax_PK_xG);
        except:
            pass 
        try:
            xGA_PK_plot = team_PK_df.plot.barh(x='UNIT', y='xGA', color=opponent_color, edgecolor='None', width=0.5, legend=None, label='', ax=ax_PK_xG);
        except:
            pass
        try:
            xGD_PK_marker = team_PK_df.plot(x='xGD', y='RANK', marker='|', markersize=13, markeredgewidth=1, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend='', label='', ax=ax_PK_xG);
        except:
            pass

        # for each state, plot the bars for time on ice
        try:
            toi_5v5_lines_plot = team_lines_df.plot.barh(x='LINE', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_5v5_lines_toi);
        except:
            pass 
        try:
            toi_5v5_pairings_plot = team_pairings_df.plot.barh(x='PAIRING', y='TOI', color='white', edgecolor=team_color, width=0.5, legend=None, label='', ax=ax_5v5_pairings_toi);
        except:
            pass
        try:
            toi_PP_plot = team_PP_df.plot.barh(x='UNIT', y='TOI', color='white', edgecolor=team_color, width=0.75, legend=None, label='', ax=ax_PP_toi);
        except:
            pass
        try:
            toi_PK_plot = team_PK_df.plot.barh(x='UNIT', y='TOI', color='white', edgecolor=team_color, width=0.5, legend=None, label='', ax=ax_PK_toi);
        except:
            pass

        # set / remove the y-labels for the subplots
        ax_5v5_lines_xG.set_xlabel('')
        ax_5v5_lines_xG.set_ylabel('')
        ax_5v5_lines_toi.set_xlabel('')
        ax_5v5_lines_toi.set_ylabel('')

        ax_5v5_pairings_xG.set_xlabel('')
        ax_5v5_pairings_xG.set_ylabel('')
        ax_5v5_pairings_toi.set_xlabel('')
        ax_5v5_pairings_toi.set_ylabel('')

        ax_PP_xG.set_xlabel('')
        ax_PP_xG.set_ylabel('')
        ax_PP_toi.set_xlabel('')
        ax_PP_toi.set_ylabel('')

        ax_PK_xG.set_xlabel('')
        ax_PK_xG.set_ylabel('')
        ax_PK_toi.set_xlabel('')
        ax_PK_toi.set_ylabel('')
        
        # set vertical indicators for zero shots
        ax_5v5_lines_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=0.25, linestyle=':', color='black')
        ax_5v5_pairings_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=0.25, linestyle=':', color='black')
        ax_PP_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=0.25, linestyle=':', color='black')
        ax_PK_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=0.25, linestyle=':', color='black')
        
        # change the tick parameters for each axes
        ax_5v5_lines_xG.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on
        ax_5v5_lines_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on

        ax_5v5_pairings_xG.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on
        ax_5v5_pairings_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on

        ax_PP_xG.tick_params(
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

        ax_PK_xG.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on
        ax_PK_toi.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelleft=False,   # labels along the left edge are off
            labelbottom=True)  # labels along the bottom edge are on

        # change the y-axis label colors
        ax_5v5_lines_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_5v5_pairings_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_PP_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_PP_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_PK_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_PK_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        # create a list of x-axis tick values contingent on the max values for shots
        team_5v5_lines_df2 = team_lines_df.copy()
        team_5v5_pairings_df2 = team_pairings_df.copy()
        team_PP_df2 = team_PP_df.copy()
        team_PK_df2 = team_PK_df.copy()
        
        team_5v5_lines_df2['xGA'] *= -1
        team_5v5_pairings_df2['xGA'] *= -1
        team_PP_df2['xGA'] *= -1
        team_PK_df2['xGA'] *= -1
        
        xGF_5v5_lines_max = team_5v5_lines_df2['xGF']
        xGF_5v5_lines_max = xGF_5v5_lines_max.max()

        xGA_5v5_lines_max = team_5v5_lines_df2['xGA']
        xGA_5v5_lines_max = xGA_5v5_lines_max.max()

        xG_5v5_lines_max = int()
        if xGF_5v5_lines_max >= xGA_5v5_lines_max:
            xG_5v5_lines_max = xGF_5v5_lines_max
        if xGF_5v5_lines_max < xGA_5v5_lines_max:
            xG_5v5_lines_max = xGA_5v5_lines_max

        xGF_5v5_pairings_max = team_5v5_pairings_df2['xGF']
        xGF_5v5_pairings_max = xGF_5v5_pairings_max.max()

        xGA_5v5_pairings_max = team_5v5_pairings_df2['xGA']
        xGA_5v5_pairings_max = xGA_5v5_pairings_max.max()

        xG_5v5_pairings_max = int()
        if xGF_5v5_pairings_max >= xGA_5v5_pairings_max:
            xG_5v5_pairings_max = xGF_5v5_pairings_max
        if xGF_5v5_pairings_max < xGA_5v5_pairings_max:
            xG_5v5_pairings_max = xGA_5v5_pairings_max
           
        xG_5v5_tickmax = int()
        if xG_5v5_lines_max >= xG_5v5_pairings_max:
            xG_5v5_tickmax = xG_5v5_lines_max
        if xG_5v5_lines_max < xG_5v5_pairings_max:
            xG_5v5_tickmax = xG_5v5_pairings_max   

        xG_5v5_ticklabels = []
        if xG_5v5_tickmax <= 0.5:
            xG_5v5_ticklabels = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        if xG_5v5_tickmax > 0.5 and xG_5v5_tickmax <= 1:
            xG_5v5_ticklabels = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        if xG_5v5_tickmax > 1 and xG_5v5_tickmax <= 1.5:
            xG_5v5_ticklabels = [-1.5, -1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2, 1.5]
        if xG_5v5_tickmax > 1.5 and xG_5v5_tickmax <= 2:
            xG_5v5_ticklabels = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6, 2.0]
        if xG_5v5_tickmax > 2 and xG_5v5_tickmax <= 2.5:
            xG_5v5_ticklabels = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        if xG_5v5_tickmax > 2.5 and xG_5v5_tickmax <= 3:
            xG_5v5_ticklabels = [-3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
        if xG_5v5_tickmax > 3 and xG_5v5_tickmax <= 3.5:
            xG_5v5_ticklabels = [-3.5, -2.8, -2.1, -1.4, -0.7, 0.0, 0.7, 1.4, 2.1, 2.8, 3.5]
        if xG_5v5_tickmax > 3.5 and xG_5v5_tickmax <= 4:
            xG_5v5_ticklabels = [-4.0, -3.2, -2.4, -1.6, -0.8, 0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
            
        toi_5v5_lines_tickmax = max_lines_toi

        toi_5v5_pairings_tickmax = max_pairings_toi

        toi_5v5_tickmax = int()
        if toi_5v5_lines_tickmax >= toi_5v5_pairings_tickmax:
            toi_5v5_tickmax = toi_5v5_lines_tickmax
        if toi_5v5_lines_tickmax < toi_5v5_pairings_tickmax:
            toi_5v5_tickmax = toi_5v5_pairings_tickmax

        toi_5v5_ticklabels = []
        if toi_5v5_tickmax <= 2:
            toi_5v5_ticklabels = [0, 2]
        if toi_5v5_tickmax > 2 and toi_5v5_tickmax <= 4:
            toi_5v5_ticklabels = [0, 4]
        if toi_5v5_tickmax > 4 and toi_5v5_tickmax <= 6:
            toi_5v5_ticklabels = [0, 6]
        if toi_5v5_tickmax > 6 and toi_5v5_tickmax <= 8:
            toi_5v5_ticklabels = [0, 8]
        if toi_5v5_tickmax > 8 and toi_5v5_tickmax <= 10:
            toi_5v5_ticklabels = [0, 10]
        if toi_5v5_tickmax > 10 and toi_5v5_tickmax <= 12:
            toi_5v5_ticklabels = [0, 12]
        if toi_5v5_tickmax > 12 and toi_5v5_tickmax <= 14:
            toi_5v5_ticklabels = [0, 14]
        if toi_5v5_tickmax > 14 and toi_5v5_tickmax <= 16:
            toi_5v5_ticklabels = [0, 16]
        if toi_5v5_tickmax > 16 and toi_5v5_tickmax <= 18:
            toi_5v5_ticklabels = [0, 18]
        if toi_5v5_tickmax > 18 and toi_5v5_tickmax <= 20:
            toi_5v5_ticklabels = [0, 20]     
            
        xGF_PP_max = team_PP_df2['xGF']
        xGF_PP_max = xGF_PP_max.max()
        
        xGA_PP_max = team_PP_df2['xGA']
        xGA_PP_max = xGA_PP_max.max()

        xG_PP_tickmax = int()
        if xGF_PP_max >= xGA_PP_max:
            xG_PP_tickmax = xGF_PP_max
        if xGF_PP_max < xGA_PP_max:
            xG_PP_tickmax = xGA_PP_max

        xGF_PK_max = team_PK_df2['xGF']
        xGF_PK_max = xGF_PK_max.max()
        
        xGA_PK_max = team_PK_df2['xGA']
        xGA_PK_max = xGA_PK_max.max()

        xG_PK_tickmax = int()
        if xGF_PK_max >= xGA_PK_max:
            xG_PK_tickmax = xGF_PK_max
        if xGF_PK_max < xGA_PK_max:
            xG_PK_tickmax = xGA_PK_max

        if xG_PP_tickmax >= xG_PK_tickmax:
            xG_specialteams_tickmax = xG_PP_tickmax
        if xG_PP_tickmax < xG_PK_tickmax:
            xG_specialteams_tickmax = xG_PK_tickmax
        
        xG_specialteams_ticklabels = []
        if xG_specialteams_tickmax <= 4:
            xG_specialteams_ticklabels = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        if xG_specialteams_tickmax > 0.5 and xG_specialteams_tickmax <= 1:
            xG_specialteams_ticklabels = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        if xG_specialteams_tickmax > 1 and xG_specialteams_tickmax <= 1.5:
            xG_specialteams_ticklabels = [-1.5, -1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2, 1.5]
        if xG_specialteams_tickmax > 1.5 and xG_specialteams_tickmax <= 2:
            xG_specialteams_ticklabels = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6, 2.0]
        if xG_specialteams_tickmax > 2 and xG_specialteams_tickmax <= 2.5:
            xG_specialteams_ticklabels = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        if xG_specialteams_tickmax > 2.5 and xG_specialteams_tickmax <= 3:
            xG_specialteams_ticklabels = [-3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
        if xG_specialteams_tickmax > 3 and xG_specialteams_tickmax <= 3.5:
            xG_specialteams_ticklabels = [-3.5, -2.8, -2.1, -1.4, -0.7, 0.0, 0.7, 1.4, 2.1, 2.8, 3.5]
        if xG_specialteams_tickmax > 3.5 and xG_specialteams_tickmax <= 4:
            xG_specialteams_ticklabels = [-4.0, -3.2, -2.4, -1.6, -0.8, 0.0, 0.8, 1.6, 2.4, 3.2, 4.0]
                        
        toi_PP_tickmax = max_PP_toi

        toi_SH_tickmax = max_PK_toi

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
        ax_5v5_lines_toi.axvspan(toi_5v5_ticklabels[1] / 2, toi_5v5_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_5v5_lines_toi.axvspan(toi_5v5_ticklabels[1], toi_5v5_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_5v5_pairings_toi.axvspan(toi_5v5_ticklabels[1] / 2, toi_5v5_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_5v5_pairings_toi.axvspan(toi_5v5_ticklabels[1], toi_5v5_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_PP_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_PP_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_PK_toi.axvspan(toi_specialteams_ticklabels[1] / 2, toi_specialteams_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_PK_toi.axvspan(toi_specialteams_ticklabels[1], toi_specialteams_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
          
        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_5v5_lines_xG.set_xticks(xG_5v5_ticklabels, minor=False)
        ax_5v5_lines_toi.set_xticks(toi_5v5_ticklabels, minor=False)

        ax_5v5_pairings_xG.set_xticks(xG_5v5_ticklabels, minor=False)
        ax_5v5_pairings_toi.set_xticks(toi_5v5_ticklabels, minor=False)
        
        ax_PP_xG.set_xticks(xG_specialteams_ticklabels, minor=False)
        ax_PP_toi.set_xticks(toi_specialteams_ticklabels, minor=False)
        
        ax_PK_xG.set_xticks(xG_specialteams_ticklabels, minor=False)
        ax_PK_toi.set_xticks(toi_specialteams_ticklabels, minor=False)
        
        # remove the borders to each subplot
        ax_5v5_lines_xG.spines["top"].set_visible(False)   
        ax_5v5_lines_xG.spines["bottom"].set_visible(False)    
        ax_5v5_lines_xG.spines["right"].set_visible(False)    
        ax_5v5_lines_xG.spines["left"].set_visible(False)  
        ax_5v5_lines_toi.spines["top"].set_visible(False)   
        ax_5v5_lines_toi.spines["bottom"].set_visible(False)    
        ax_5v5_lines_toi.spines["right"].set_visible(False)    
        ax_5v5_lines_toi.spines["left"].set_visible(False) 

        ax_5v5_pairings_xG.spines["top"].set_visible(False)   
        ax_5v5_pairings_xG.spines["bottom"].set_visible(False)    
        ax_5v5_pairings_xG.spines["right"].set_visible(False)    
        ax_5v5_pairings_xG.spines["left"].set_visible(False)  
        ax_5v5_pairings_toi.spines["top"].set_visible(False)   
        ax_5v5_pairings_toi.spines["bottom"].set_visible(False)    
        ax_5v5_pairings_toi.spines["right"].set_visible(False)    
        ax_5v5_pairings_toi.spines["left"].set_visible(False)
        
        ax_PP_xG.spines["top"].set_visible(False)   
        ax_PP_xG.spines["bottom"].set_visible(False)    
        ax_PP_xG.spines["right"].set_visible(False)    
        ax_PP_xG.spines["left"].set_visible(False) 
        ax_PP_toi.spines["top"].set_visible(False)   
        ax_PP_toi.spines["bottom"].set_visible(False)    
        ax_PP_toi.spines["right"].set_visible(False)    
        ax_PP_toi.spines["left"].set_visible(False) 

        ax_PK_xG.spines["top"].set_visible(False)   
        ax_PK_xG.spines["bottom"].set_visible(False)    
        ax_PK_xG.spines["right"].set_visible(False)    
        ax_PK_xG.spines["left"].set_visible(False) 
        ax_PK_toi.spines["top"].set_visible(False)   
        ax_PK_toi.spines["bottom"].set_visible(False)    
        ax_PK_toi.spines["right"].set_visible(False)    
        ax_PK_toi.spines["left"].set_visible(False) 

        # add a legend for the shot type markers
        from matplotlib.lines import Line2D
        elements = [Line2D([0], [0], marker='|', markersize=13, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
        ax_PK_xG.legend(handles=elements, loc='center', bbox_to_anchor=(.5, -.6), ncol=1).get_frame().set_linewidth(0.0)

        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))

        # add a text box in the event a team does not have a power play
        if team_max_PP_toi == 0:
            fig.text(0.35, 0.375, 'No PP situations', color='black', fontsize='10', bbox=dict(facecolor='None', edgecolor='None'))
         
        # add a text box in the event a team's opponent does not have a power play
        if team_max_PK_toi == 0:
            fig.text(0.35, 0.175, 'No PK situations', color='black', fontsize='10', bbox=dict(facecolor='None', edgecolor='None'))

        # for games where one (or both!) teams spend no time on a powerplay or shorthanded, turn all indicators for the respective axes off 
        if team_max_PP_toi == 0:
            ax_PP_xG.axis('off')
            ax_PP_toi.axis('off')
        if team_max_PK_toi == 0:
            ax_PK_xG.axis('off')
            ax_PK_toi.axis('off')


        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_units + 'onice_xg_away.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units + 'onice_xg_home.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()


        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' lines, pairings and special teams units on-ice xG.')   
        
    # status update
    print('Finished plotting the on-ice xG for lines, pairings and special teams units.')