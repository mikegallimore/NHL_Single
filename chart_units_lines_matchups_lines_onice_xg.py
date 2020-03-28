# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parameters
import matplotlib.colors as clr
import dict_team_colors
import mod_switch_colors

def parse_ids(season_id, game_id, images):

    # pull common variables from the parameters file
    charts_units_lines_matchups = parameters.charts_units_lines_matchups
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    # create variables that point to the .csv processed stats file for lines
    lines_file = files_root + 'stats_units_lines_onice.csv'
    lines_matchups_lines_file = files_root + 'stats_units_lines_onice_matchups_lines.csv'
    
    # create dataframe objects that read in info from the .csv files
    lines_df = pd.read_csv(lines_file)

    lines_matchups_lines_df = pd.read_csv(lines_matchups_lines_file)

    max_toi = lines_matchups_lines_df['TOI'].max()  
 
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
    
    away_cmap = clr.LinearSegmentedColormap.from_list('custom away', [(0, '#ffffff'), (1, away_color)], N=256)  
    home_cmap = clr.LinearSegmentedColormap.from_list('custom home', [(0, '#ffffff'), (1, home_color)], N=256)
   
    
    ###
    ### 5v5
    ###
    
    ### loop through each team
    for team in teams:
      
        if team == away:
            team_color = team_colors[0]
            opponent_color = team_colors[1]
            team_color_map = plt.cm.get_cmap(away_cmap)
            opponent_color_map = plt.cm.get_cmap(home_cmap)  
    
        if team == home:
            team_color = team_colors[1]
            opponent_color = team_colors[0]
            team_color_map = plt.cm.get_cmap(home_cmap)
            opponent_color_map = plt.cm.get_cmap(away_cmap)    

        # create a lines dataframe; filter for team; sort by time on ice; keep the lines with the 4 highest totals; rank and then invert the rankings
        team_lines_df = lines_df.copy()
        team_lines_df = team_lines_df[(team_lines_df['TEAM'] == team)]  
        team_lines_df = team_lines_df.sort_values(by=['TOI'], ascending = True)
        team_lines_df = team_lines_df.iloc[-4:]      
        team_lines_df['RANK'] = team_lines_df['TOI'].rank(method='first')
        team_lines_df = team_lines_df.sort_values(by=['RANK'], ascending = True)
        team_lines_df['RANK'] -= 1
        
        team_lines_list = team_lines_df.LINE.unique()

        # create a lines dataframe; filter for team
        team_lines_matchups_lines_df = lines_matchups_lines_df.copy()
        team_lines_matchups_lines_df = team_lines_matchups_lines_df[(team_lines_matchups_lines_df['TEAM'] == team)]

        max_lines_toi = team_lines_matchups_lines_df['TOI'].max()

        # remove zeros from the differential column       
        team_lines_matchups_lines_df['xGD'] = team_lines_matchups_lines_df['xGD'].replace(0, np.NaN)       
        
        # make expected goals against negative values 
        team_lines_matchups_lines_df['xGA'] *= -1

        # create dataframes for specific lines; sort by time on ice; rank and then invert the rankings  
        team_line1_matchups_lines_df = team_lines_matchups_lines_df.copy()
        team_line1_matchups_lines_df = team_line1_matchups_lines_df[(team_line1_matchups_lines_df['LINE'] == team_lines_list[3])]
        team_line1_matchups_lines_df.sort_values(by=['TOI'], inplace=True)
        team_line1_matchups_lines_df['RANK'] = team_line1_matchups_lines_df['TOI'].rank(method='first')
        team_line1_matchups_lines_df['RANK'] -= 1
        
        team_line2_matchups_lines_df = team_lines_matchups_lines_df.copy()
        team_line2_matchups_lines_df = team_line2_matchups_lines_df[(team_line2_matchups_lines_df['LINE'] == team_lines_list[2])]
        team_line2_matchups_lines_df.sort_values(by=['TOI'], inplace=True)
        team_line2_matchups_lines_df['RANK'] = team_line2_matchups_lines_df['TOI'].rank(method='first')
        team_line2_matchups_lines_df['RANK'] -= 1

        team_line3_matchups_lines_df = team_lines_matchups_lines_df.copy()
        team_line3_matchups_lines_df = team_line3_matchups_lines_df[(team_line3_matchups_lines_df['LINE'] == team_lines_list[1])]
        team_line3_matchups_lines_df.sort_values(by=['TOI'], inplace=True)
        team_line3_matchups_lines_df['RANK'] = team_line3_matchups_lines_df['TOI'].rank(method='first')
        team_line3_matchups_lines_df['RANK'] -= 1

        try:
            team_line4_matchups_lines_df = team_lines_matchups_lines_df.copy()
            team_line4_matchups_lines_df = team_line4_matchups_lines_df[(team_line4_matchups_lines_df['LINE'] == team_lines_list[0])]
            team_line4_matchups_lines_df.sort_values(by=['TOI'], inplace=True)
            team_line4_matchups_lines_df['RANK'] = team_line4_matchups_lines_df['TOI'].rank(method='first')
            team_line4_matchups_lines_df['RANK'] -= 1

            team_line4_list = team_line4_matchups_lines_df.MATCHUP.unique()
        except:
            pass
        
        # create lists for use in determining the differential marker size
        team_line1_matchups_lines_list = team_line1_matchups_lines_df.MATCHUP.unique()
        team_line2_matchups_lines_list = team_line2_matchups_lines_df.MATCHUP.unique()
        team_line3_matchups_lines_list = team_line3_matchups_lines_df.MATCHUP.unique()
        team_line4_matchups_lines_list = team_line4_matchups_lines_df.MATCHUP.unique()

        if len(team_line1_matchups_lines_list) >= 7:
            line1_width = .8
        elif len(team_line1_matchups_lines_list) == 6:
            line1_width = .7
        elif len(team_line1_matchups_lines_list) == 5:
            line1_width = .6
        elif len(team_line1_matchups_lines_list) == 4:
            line1_width = .5
        elif len(team_line1_matchups_lines_list) == 3:
            line1_width = .4
        elif len(team_line1_matchups_lines_list) == 2:
            line1_width = .3
        elif len(team_line1_matchups_lines_list) == 1:
            line1_width = .2      

        if len(team_line2_matchups_lines_list) >= 7:
            line2_width = .8
        elif len(team_line2_matchups_lines_list) == 6:
            line2_width = .7
        elif len(team_line2_matchups_lines_list) == 5:
            line2_width = .6
        elif len(team_line2_matchups_lines_list) == 4:
            line2_width = .5
        elif len(team_line2_matchups_lines_list) == 3:
            line2_width = .4
        elif len(team_line2_matchups_lines_list) == 2:
            line2_width = .3
        elif len(team_line2_matchups_lines_list) == 1:
            line2_width = .2

        if len(team_line3_matchups_lines_list) >= 7:
            line3_width = .8
        elif len(team_line3_matchups_lines_list) == 6:
            line3_width = .7
        elif len(team_line3_matchups_lines_list) == 5:
            line3_width = .6
        elif len(team_line3_matchups_lines_list) == 4:
            line3_width = .5
        elif len(team_line3_matchups_lines_list) == 3:
            line3_width = .4
        elif len(team_line3_matchups_lines_list) == 2:
            line3_width = .3
        elif len(team_line3_matchups_lines_list) == 1:
            line3_width = .2   

        if len(team_line4_matchups_lines_list) >= 7:
            line4_width = .8
        elif len(team_line4_matchups_lines_list) == 6:
            line4_width = .7
        elif len(team_line4_matchups_lines_list) == 5:
            line4_width = .6
        elif len(team_line4_matchups_lines_list) == 4:
            line4_width = .5
        elif len(team_line4_matchups_lines_list) == 3:
            line4_width = .4
        elif len(team_line4_matchups_lines_list) == 2:
            line4_width = .3
        elif len(team_line4_matchups_lines_list) == 1:
            line4_width = .2
        
        # create more lines dataframes with just the time on ice column; set a max value; scale each line's time on ice relative to the max  
        line1_matchups_lines_toi = team_line1_matchups_lines_df['TOI']
        max_line1_matchups_lines_toi = line1_matchups_lines_toi.max()   
        line1_matchups_lines_toi_color = line1_matchups_lines_toi / float(max_line1_matchups_lines_toi)

        line2_matchups_lines_toi = team_line2_matchups_lines_df['TOI']
        max_line2_matchups_lines_toi = line2_matchups_lines_toi.max()    
        line2_matchups_lines_toi_color = line2_matchups_lines_toi / float(max_line2_matchups_lines_toi)

        line3_matchups_lines_toi = team_line3_matchups_lines_df['TOI']
        max_line3_matchups_lines_toi = line3_matchups_lines_toi.max()    
        line3_matchups_lines_toi_color = line3_matchups_lines_toi / float(max_line3_matchups_lines_toi)

        try:
            line4_matchups_lines_toi = team_line4_matchups_lines_df['TOI']
            max_line4_matchups_lines_toi = line4_matchups_lines_toi.max()    
            line4_matchups_lines_toi_color = line4_matchups_lines_toi / float(max_line4_matchups_lines_toi)
        except:
            pass
        
        # connect team and opponent color map colors to each line's scaled time on ice 
        line1_matchups_lines_toi_color_map_for = team_color_map(line1_matchups_lines_toi_color)
        line1_matchups_lines_toi_color_map_against = opponent_color_map(line1_matchups_lines_toi_color)

        line2_matchups_lines_toi_color_map_for = team_color_map(line2_matchups_lines_toi_color)
        line2_matchups_lines_toi_color_map_against = opponent_color_map(line2_matchups_lines_toi_color)

        line3_matchups_lines_toi_color_map_for = team_color_map(line3_matchups_lines_toi_color)
        line3_matchups_lines_toi_color_map_against = opponent_color_map(line3_matchups_lines_toi_color)

        try:
            line4_matchups_lines_toi_color_map_for = team_color_map(line4_matchups_lines_toi_color)
            line4_matchups_lines_toi_color_map_against = opponent_color_map(line4_matchups_lines_toi_color)
        except:
            pass
 
        # create a figure with two subplots sharing the y-axis
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(4, 8, hspace=.40, wspace=0.50)

        ax_line1_xG = fig.add_subplot(grid[0, 0:-2])
        ax_line1_toi = fig.add_subplot(grid[0, -1])

        ax_line2_xG = fig.add_subplot(grid[1, 0:-2])
        ax_line2_toi = fig.add_subplot(grid[1, -1])

        ax_line3_xG = fig.add_subplot(grid[2, 0:-2])
        ax_line3_toi = fig.add_subplot(grid[2, -1])

        ax_line4_xG = fig.add_subplot(grid[3, 0:-2])
        ax_line4_toi = fig.add_subplot(grid[3, -1])
       
        # set the plot title
        fig.suptitle(date + ' Lines vs. Lines Expected Goals\n\n')

        fig.text(.396, 0.910, '5v5 S', color='black', fontsize='10', bbox=dict(facecolor='None', edgecolor='None'))
        
        # set the axes titles
        ax_line1_xG.set_title(team_lines_list[3], fontsize=10, color=team_color)
        ax_line1_toi.set_title('5v5 TOI\n', fontsize=10)

        ax_line2_xG.set_title(team_lines_list[2], fontsize=10, color=team_color)
        ax_line2_toi.set_title('', fontsize=10)

        ax_line3_xG.set_title(team_lines_list[1], fontsize=10, color=team_color)
        ax_line3_toi.set_title('', fontsize=10)

        if len(team_line4_list) != 0:
            ax_line4_xG.set_title(team_lines_list[0], fontsize=10, color=team_color)
            ax_line4_toi.set_title('', fontsize=10)
        
        # create bars for expected goals for and against as well as line markers (to note the expected goals differential) for each line
        try:
            line1_xGF_plot = team_line1_matchups_lines_df.plot.barh(x='MATCHUP', y='xGF', stacked=True, color=line1_matchups_lines_toi_color_map_for, width=line1_width, legend=None, label='', ax=ax_line1_xG);
        except:
            pass
        try:
            line1_xGA_plot = team_line1_matchups_lines_df.plot.barh(x='MATCHUP', y='xGA', stacked=True, color=line1_matchups_lines_toi_color_map_against, width=line1_width, legend=None, label='', ax=ax_line1_xG);
        except:
            pass
        try:
            line1_xGD_plot = team_line1_matchups_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_line1_xG);
        except:
            pass

        try:
            line2_xGF_plot = team_line2_matchups_lines_df.plot.barh(x='MATCHUP', y='xGF', stacked=True, color=line2_matchups_lines_toi_color_map_for, width=line2_width, legend=None, label='', ax=ax_line2_xG);
        except:
            pass
        try:
            line2_xGA_plot = team_line2_matchups_lines_df.plot.barh(x='MATCHUP', y='xGA', stacked=True, color=line2_matchups_lines_toi_color_map_against, width=line2_width, legend=None, label='', ax=ax_line2_xG);
        except:
            pass
        try:
            line2_xGD_plot = team_line2_matchups_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_line2_xG);
        except:
            pass

        try:
            line3_xGF_plot = team_line3_matchups_lines_df.plot.barh(x='MATCHUP', y='xGF', stacked=True, color=line3_matchups_lines_toi_color_map_for, width=line3_width, legend=None, label='', ax=ax_line3_xG);
        except:
            pass
        try:
            line3_xGA_plot = team_line3_matchups_lines_df.plot.barh(x='MATCHUP', y='xGA', stacked=True, color=line3_matchups_lines_toi_color_map_against, width=line3_width, legend=None, label='', ax=ax_line3_xG);
        except:
            pass
        try:
            line3_xGD_plot = team_line3_matchups_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_line3_xG);
        except:
            pass

        if len(team_line4_list) != 0:
            try:
                line4_xGF_plot = team_line4_matchups_lines_df.plot.barh(x='MATCHUP', y='xGF', stacked=True, color=line4_matchups_lines_toi_color_map_for, width=line4_width, legend=None, label='', ax=ax_line4_xG);
            except:
                pass
            try:
                line4_xGA_plot = team_line4_matchups_lines_df.plot.barh(x='MATCHUP', y='xGA', stacked=True, color=line4_matchups_lines_toi_color_map_against, width=line4_width, legend=None, label='', ax=ax_line4_xG);
            except:
                pass
            try:
                line4_xGD_plot = team_line4_matchups_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_line4_xG);
            except:
                pass

        # plot the bars for time on ice
        try:
            toi_line1 = team_line1_matchups_lines_df.plot.barh(x='MATCHUP', y='TOI', color='white', edgecolor=team_color, width=line1_width, legend=None, label='', ax=ax_line1_toi);
        except:
            pass

        try:
            toi_line2 = team_line2_matchups_lines_df.plot.barh(x='MATCHUP', y='TOI', color='white', edgecolor=team_color, width=line2_width, legend=None, label='', ax=ax_line2_toi);
        except:
            pass

        try:
            toi_line3 = team_line3_matchups_lines_df.plot.barh(x='MATCHUP', y='TOI', color='white', edgecolor=team_color, width=line3_width, legend=None, label='', ax=ax_line3_toi);
        except:
            pass

        if len(team_line4_list) != 0:
            try:
                toi_line4 = team_line4_matchups_lines_df.plot.barh(x='MATCHUP', y='TOI', color='white', edgecolor=team_color, width=line4_width, legend=None, label='', ax=ax_line4_toi);
            except:
                pass

        # remove the labels for each subplot
        ax_line1_xG.set_xlabel('')
        ax_line1_xG.set_ylabel('')

        ax_line1_toi.set_xlabel('')
        ax_line1_toi.set_ylabel('')

        ax_line2_xG.set_xlabel('')
        ax_line2_xG.set_ylabel('')

        ax_line2_toi.set_xlabel('')
        ax_line2_toi.set_ylabel('')

        ax_line3_xG.set_xlabel('')
        ax_line3_xG.set_ylabel('')

        ax_line3_toi.set_xlabel('')
        ax_line3_toi.set_ylabel('')

        ax_line4_xG.set_xlabel('')
        ax_line4_xG.set_ylabel('')

        ax_line4_toi.set_xlabel('')
        ax_line4_toi.set_ylabel('')
    
        # set vertical indicators for break-even expected goals differential
        ax_line1_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        ax_line2_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        ax_line3_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
        ax_line4_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
    
        # change the tick parameters
        ax_line1_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=False)

        ax_line1_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=False)

        ax_line2_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=False)

        ax_line2_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=False)

        ax_line3_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=False)

        ax_line3_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=False)

        ax_line4_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=True)

        ax_line4_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=True)

        # change the y-axis label colors
        ax_line1_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=opponent_color)

        ax_line2_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=opponent_color)

        ax_line3_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=opponent_color)

        ax_line4_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=opponent_color)
        
        # create a list of x-axis tick values contingent on the max values for expected goals for and against 
        xGF_max = lines_matchups_lines_df['xGF']
        xGF_max = xGF_max.max()
        
        xGA_max = lines_matchups_lines_df['xGA']
        xGA_max = xGA_max.max()

        xG_tickmax = int()
        if xGF_max >= xGA_max:
            xG_tickmax = xGF_max
        elif xGF_max < xGA_max:
            xG_tickmax = xGA_max

        xG_ticklabels = []
        if xG_tickmax > 0 and xG_tickmax <= 0.5:
            xG_ticklabels = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        if xG_tickmax > 0.5 and xG_tickmax <= 1:
            xG_ticklabels = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        if xG_tickmax > 1 and xG_tickmax <= 1.5:
            xG_ticklabels = [-1.5, -1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2, 1.5]
        if xG_tickmax > 1.5 and xG_tickmax <= 2:
            xG_ticklabels = [-2.0, -1.6, -1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2, 1.6, 2.0]
        if xG_tickmax > 2 and xG_tickmax <= 2.5:
            xG_ticklabels = [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        if xG_tickmax > 2.5 and xG_tickmax <= 3:
            xG_ticklabels = [-3.0, -2.4, -1.8, -1.2, -0.6, 0.0, 0.6, 1.2, 1.8, 2.4, 3.0]
        if xG_tickmax > 3 and xG_tickmax <= 3.5:
            xG_ticklabels = [-3.5, -2.8, -2.1, -1.4, -0.7, 0.0, 0.7, 1.4, 2.1, 2.8, 3.5]
        if xG_tickmax > 3.5 and xG_tickmax <= 4:
            xG_ticklabels = [-4.0, -3.2, -2.4, -1.6, -0.8, 0.0, 0.8, 1.6, 2.4, 3.2, 4.0]

        toi_tickmax = max_toi

        toi_ticklabels = []
        if toi_tickmax <= 2:
            toi_ticklabels = [0, 2]
        if toi_tickmax > 2 and toi_tickmax <= 4:
            toi_ticklabels = [0, 4]
        if toi_tickmax > 4 and toi_tickmax <= 6:
            toi_ticklabels = [0, 6]
        if toi_tickmax > 6 and toi_tickmax <= 8:
            toi_ticklabels = [0, 8]
        if toi_tickmax > 8 and toi_tickmax <= 10:
            toi_ticklabels = [0, 10]
        if toi_tickmax > 10 and toi_tickmax <= 12:
            toi_ticklabels = [0, 12]
        if toi_tickmax > 12 and toi_tickmax <= 14:
            toi_ticklabels = [0, 14]
        if toi_tickmax > 14 and toi_tickmax <= 16:
            toi_ticklabels = [0, 16]
        if toi_tickmax > 16 and toi_tickmax <= 18:
            toi_ticklabels = [0, 18]
        if toi_tickmax > 18 and toi_tickmax <= 20:
            toi_ticklabels = [0, 20]

        # set vertical indicator for midpoint of time on ice max
        ax_line1_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_line1_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
 
        ax_line2_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_line2_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_line3_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_line3_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_line4_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_line4_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
      
        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_line1_xG.set_xticks(xG_ticklabels, minor=False)
        ax_line1_toi.set_xticks(toi_ticklabels, minor=False)

        ax_line2_xG.set_xticks(xG_ticklabels, minor=False)
        ax_line2_toi.set_xticks(toi_ticklabels, minor=False)

        ax_line3_xG.set_xticks(xG_ticklabels, minor=False)
        ax_line3_toi.set_xticks(toi_ticklabels, minor=False)

        ax_line4_xG.set_xticks(xG_ticklabels, minor=False)
        ax_line4_toi.set_xticks(toi_ticklabels, minor=False)

        # remove axes ticks for instances where a line had no opposing lines meet the time on ice threshold
        if len(team_line4_list) == 0:
            ax_line4_xG.set_yticks([], minor=False)

            ax_line4_toi.set_yticks([], minor=False)
    
        # remove the borders to each subplot
        ax_line1_xG.spines["top"].set_visible(False)   
        ax_line1_xG.spines["bottom"].set_visible(False)    
        ax_line1_xG.spines["right"].set_visible(False)    
        ax_line1_xG.spines["left"].set_visible(False)

        ax_line1_toi.spines["top"].set_visible(False)   
        ax_line1_toi.spines["bottom"].set_visible(False)    
        ax_line1_toi.spines["right"].set_visible(False)    
        ax_line1_toi.spines["left"].set_visible(False)
    
        ax_line2_xG.spines["top"].set_visible(False)   
        ax_line2_xG.spines["bottom"].set_visible(False)    
        ax_line2_xG.spines["right"].set_visible(False)    
        ax_line2_xG.spines["left"].set_visible(False)

        ax_line2_toi.spines["top"].set_visible(False)   
        ax_line2_toi.spines["bottom"].set_visible(False)    
        ax_line2_toi.spines["right"].set_visible(False)    
        ax_line2_toi.spines["left"].set_visible(False)

        ax_line3_xG.spines["top"].set_visible(False)   
        ax_line3_xG.spines["bottom"].set_visible(False)    
        ax_line3_xG.spines["right"].set_visible(False)    
        ax_line3_xG.spines["left"].set_visible(False)

        ax_line3_toi.spines["top"].set_visible(False)   
        ax_line3_toi.spines["bottom"].set_visible(False)    
        ax_line3_toi.spines["right"].set_visible(False)    
        ax_line3_toi.spines["left"].set_visible(False)

        ax_line4_xG.spines["top"].set_visible(False)   
        ax_line4_xG.spines["bottom"].set_visible(False)    
        ax_line4_xG.spines["right"].set_visible(False)    
        ax_line4_xG.spines["left"].set_visible(False)

        ax_line4_toi.spines["top"].set_visible(False)   
        ax_line4_toi.spines["bottom"].set_visible(False)    
        ax_line4_toi.spines["right"].set_visible(False)    
        ax_line4_toi.spines["left"].set_visible(False)
    
        # add a legend for the shot type markers
        from matplotlib.lines import Line2D
        elements = [Line2D([0], [0], marker='|', markersize=13, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
        ax_line4_xG.legend(handles=elements, loc='center', bbox_to_anchor=(.5, -.40), ncol=2).get_frame().set_linewidth(0.0)
        
        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))


        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_units_lines_matchups + 'onice_xg_away_lines_matchups_lines.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units_lines_matchups + 'onice_xg_home_lines_matchups_lines.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()
        
        
        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' lines vs. lines 5v5 on-ice xG.')   
        
    # status update
    print('Finished plotting the 5v5 on-ice xG for lines vs. lines.')