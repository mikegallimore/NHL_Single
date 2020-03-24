# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

import pandas as pd
import matplotlib.pyplot as plt
import parameters
import matplotlib.colors as clr
import dict_team_colors
import mod_switch_colors

def parse_ids(season_id, game_id, images):

    # pull common variables from the parameters file
    charts_units_pairings_teammates = parameters.charts_units_pairings_teammates
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
    pairings_file = files_root + 'stats_units_pairings_onice.csv'
    pairings_teammates_lines_file = files_root + 'stats_units_pairings_onice_teammates_lines.csv'
    
    # create dataframe objects that read in info from the .csv files
    pairings_df = pd.read_csv(pairings_file)

    pairings_teammates_lines_df = pd.read_csv(pairings_teammates_lines_file)
 
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
    
    # loop through each team
    for team in teams:
      
        if team == away:
            team_color = team_colors[0]
            team_color_map = plt.cm.get_cmap(away_cmap)
            opponent_color_map = plt.cm.get_cmap(home_cmap)        
    
        if team == home:
            team_color = team_colors[1]
            team_color_map = plt.cm.get_cmap(home_cmap)
            opponent_color_map = plt.cm.get_cmap(away_cmap)        

        # create a lines dataframe; filter for team; sort by time on ice; keep the lines with the 4 highest totals; rank and then invert the rankings
        team_pairings_df = pairings_df.copy()
        team_pairings_df = team_pairings_df[(team_pairings_df['TEAM'] == team)]  
        team_pairings_df = team_pairings_df.sort_values(by=['TOI'], ascending = True)
        team_pairings_df = team_pairings_df.iloc[-3:]      
        team_pairings_df['RANK'] = team_pairings_df['TOI'].rank(method='first')
        team_pairings_df = team_pairings_df.sort_values(by=['RANK'], ascending = True)
        team_pairings_df['RANK'] -= 1
        
        team_pairings_list = team_pairings_df.PAIRING.unique()

        # create a lines dataframe; filter for team
        team_pairings_teammates_lines_df = pairings_teammates_lines_df.copy()
        team_pairings_teammates_lines_df = team_pairings_teammates_lines_df[(team_pairings_teammates_lines_df['TEAM'] == team)]

        max_pairings_toi = team_pairings_teammates_lines_df['TOI'].max()
       
        # make expected goals against negative values 
        team_pairings_teammates_lines_df['xGA'] *= -1

        # create dataframes for specific lines; sort by time on ice; rank and then invert the rankings  
        team_pairing1_teammates_lines_df = team_pairings_teammates_lines_df.copy()
        team_pairing1_teammates_lines_df = team_pairing1_teammates_lines_df[(team_pairing1_teammates_lines_df['PAIRING'] == team_pairings_list[2])]
        team_pairing1_teammates_lines_df.sort_values(by=['TOI'], inplace=True)
        team_pairing1_teammates_lines_df['RANK'] = team_pairing1_teammates_lines_df['TOI'].rank(method='first')
        team_pairing1_teammates_lines_df['RANK'] -= 1
        
        team_pairing2_teammates_lines_df = team_pairings_teammates_lines_df.copy()
        team_pairing2_teammates_lines_df = team_pairing2_teammates_lines_df[(team_pairing2_teammates_lines_df['PAIRING'] == team_pairings_list[1])]
        team_pairing2_teammates_lines_df.sort_values(by=['TOI'], inplace=True)
        team_pairing2_teammates_lines_df['RANK'] = team_pairing2_teammates_lines_df['TOI'].rank(method='first')
        team_pairing2_teammates_lines_df['RANK'] -= 1

        team_pairing3_teammates_lines_df = team_pairings_teammates_lines_df.copy()
        team_pairing3_teammates_lines_df = team_pairing3_teammates_lines_df[(team_pairing3_teammates_lines_df['PAIRING'] == team_pairings_list[0])]
        team_pairing3_teammates_lines_df.sort_values(by=['TOI'], inplace=True)
        team_pairing3_teammates_lines_df['RANK'] = team_pairing3_teammates_lines_df['TOI'].rank(method='first')
        team_pairing3_teammates_lines_df['RANK'] -= 1

        # create lists for use in determining the differential marker size
        team_pairing1_teammates_lines_list = team_pairing1_teammates_lines_df.LINE.unique()
        team_pairing2_teammates_lines_list = team_pairing2_teammates_lines_df.LINE.unique()
        team_pairing3_teammates_lines_list = team_pairing3_teammates_lines_df.LINE.unique()

        if len(team_pairing1_teammates_lines_list) >= 7:
            pairing1_width = .8
        elif len(team_pairing1_teammates_lines_list) == 6:
            pairing1_width = .7
        elif len(team_pairing1_teammates_lines_list) == 5:
            pairing1_width = .6
        elif len(team_pairing1_teammates_lines_list) == 4:
            pairing1_width = .5
        elif len(team_pairing1_teammates_lines_list) == 3:
            pairing1_width = .4
        elif len(team_pairing1_teammates_lines_list) == 2:
            pairing1_width = .3
        elif len(team_pairing1_teammates_lines_list) == 1:
            pairing1_width = .2
            
        if len(team_pairing2_teammates_lines_list) >= 7:
            pairing2_width = .8
        elif len(team_pairing2_teammates_lines_list) == 6:
            pairing2_width = .7
        elif len(team_pairing2_teammates_lines_list) == 5:
            pairing2_width = .6
        elif len(team_pairing2_teammates_lines_list) == 4:
            pairing2_width = .5
        elif len(team_pairing2_teammates_lines_list) == 3:
            pairing2_width = .4
        elif len(team_pairing2_teammates_lines_list) == 2:
            pairing2_width = .3
        elif len(team_pairing2_teammates_lines_list) == 1:
            pairing2_width = .2

        if len(team_pairing3_teammates_lines_list) >= 7:
            pairing3_width = .8
        elif len(team_pairing3_teammates_lines_list) == 6:
            pairing3_width = .7
        elif len(team_pairing3_teammates_lines_list) == 5:
            pairing3_width = .6
        elif len(team_pairing3_teammates_lines_list) == 4:
            pairing3_width = .5
        elif len(team_pairing3_teammates_lines_list) == 3:
            pairing3_width = .4
        elif len(team_pairing3_teammates_lines_list) == 2:
            pairing3_width = .3
        elif len(team_pairing3_teammates_lines_list) == 1:
            pairing3_width = .2

        # create more pairings dataframes with just the time on ice column; set a max value; scale each line's time on ice relative to the max  
        try:
            pairing1_teammates_lines_toi = team_pairing1_teammates_lines_df['TOI']
            max_pairing1_teammates_lines_toi = max(pairing1_teammates_lines_toi)    
            pairing1_teammates_lines_toi_color = pairing1_teammates_lines_toi / float(max(pairing1_teammates_lines_toi))
        except:
            pass
        
        try:
            pairing2_teammates_lines_toi = team_pairing2_teammates_lines_df['TOI']
            max_pairing2_teammates_lines_toi = max(pairing2_teammates_lines_toi)    
            pairing2_teammates_lines_toi_color = pairing2_teammates_lines_toi / float(max(pairing2_teammates_lines_toi))
        except:
            pass

        try:
            pairing3_teammates_lines_toi = team_pairing3_teammates_lines_df['TOI']
            max_pairing3_teammates_lines_toi = max(pairing3_teammates_lines_toi)    
            pairing3_teammates_lines_toi_color = pairing3_teammates_lines_toi / float(max(pairing3_teammates_lines_toi))
        except:
            pass
    
        # connect team and opponent color map colors to each line's scaled time on ice 
        try:
            pairing1_teammates_lines_toi_color_map_for = team_color_map(pairing1_teammates_lines_toi_color)
            pairing1_teammates_lines_toi_color_map_against = opponent_color_map(pairing1_teammates_lines_toi_color)
        except:
            pass

        try:
            pairing2_teammates_lines_toi_color_map_for = team_color_map(pairing2_teammates_lines_toi_color)
            pairing2_teammates_lines_toi_color_map_against = opponent_color_map(pairing2_teammates_lines_toi_color)
        except:
            pass
        
        try:
            pairing3_teammates_lines_toi_color_map_for = team_color_map(pairing3_teammates_lines_toi_color)
            pairing3_teammates_lines_toi_color_map_against = opponent_color_map(pairing3_teammates_lines_toi_color)
        except:
            pass

        # create a figure with two subplots sharing the y-axis
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(4, 8, hspace=.40, wspace=0.50)

        ax_pairing1_xG = fig.add_subplot(grid[0, 0:-2])
        ax_pairing1_toi = fig.add_subplot(grid[0, -1])

        ax_pairing2_xG = fig.add_subplot(grid[1, 0:-2])
        ax_pairing2_toi = fig.add_subplot(grid[1, -1])

        ax_pairing3_xG = fig.add_subplot(grid[2, 0:-2])
        ax_pairing3_toi = fig.add_subplot(grid[2, -1])

        # set the plot title
        fig.suptitle(date + ' Pairings + Lines On-Ice Expected Goals\n\n')

        fig.text(.396, 0.910, '5v5 S', color='black', fontsize='10', bbox=dict(facecolor='None', edgecolor='None'))
       
        # set the axes titles
        ax_pairing1_xG.set_title(team_pairings_list[2], fontsize=10, color=team_color)
        ax_pairing1_toi.set_title('5v5 TOI\n', fontsize=10)

        ax_pairing2_xG.set_title(team_pairings_list[1], fontsize=10, color=team_color)
        ax_pairing2_toi.set_title('', fontsize=10)

        ax_pairing3_xG.set_title(team_pairings_list[0], fontsize=10, color=team_color)
        ax_pairing3_toi.set_title('', fontsize=10)
        
        # create bars for expected goals for and against as well as line markers (to note the expected goals differential) for each line
        try:
            pairing1_xGF_plot = team_pairing1_teammates_lines_df.plot.barh(x='LINE', y='xGF', stacked=True, color=pairing1_teammates_lines_toi_color_map_for, width=pairing1_width, legend=None, label='', ax=ax_pairing1_xG);
        except:
            pass
        try:
            pairing1_xGA_plot = team_pairing1_teammates_lines_df.plot.barh(x='LINE', y='xGA', stacked=True, color=pairing1_teammates_lines_toi_color_map_against, width=pairing1_width, legend=None, label='', ax=ax_pairing1_xG);
        except:
            pass
        try:
            pairing1_xGD_plot = team_pairing1_teammates_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pairing1_xG);
        except:
            pass

        try:
            pairing2_xGF_plot = team_pairing2_teammates_lines_df.plot.barh(x='LINE', y='xGF', stacked=True, color=pairing2_teammates_lines_toi_color_map_for, width=pairing2_width, legend=None, label='', ax=ax_pairing2_xG);
        except:
            pass
        try:
            pairing2_xGA_plot = team_pairing2_teammates_lines_df.plot.barh(x='LINE', y='xGA', stacked=True, color=pairing2_teammates_lines_toi_color_map_against, width=pairing2_width, legend=None, label='', ax=ax_pairing2_xG);
        except:
            pass
        try:
            pairing2_xGD_plot = team_pairing2_teammates_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pairing2_xG);
        except:
            pass

        try:
            pairing3_xGF_plot = team_pairing3_teammates_lines_df.plot.barh(x='LINE', y='xGF', stacked=True, color=pairing3_teammates_lines_toi_color_map_for, width=pairing3_width, legend=None, label='', ax=ax_pairing3_xG);
        except:
            pass
        try:
            pairing3_xGA_plot = team_pairing3_teammates_lines_df.plot.barh(x='LINE', y='xGA', stacked=True, color=pairing3_teammates_lines_toi_color_map_against, width=pairing3_width, legend=None, label='', ax=ax_pairing3_xG);
        except:
            pass
        try:
            pairing3_xGD_plot = team_pairing3_teammates_lines_df.plot(x='xGD', y='RANK', marker='|', markersize=15,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pairing3_xG);
        except:
            pass

        # plot the bars for time on ice
        try:
            toi_pairing1 = team_pairing1_teammates_lines_df.plot.barh(x='LINE', y='TOI', color='white', edgecolor=team_color, width=pairing1_width, legend=None, label='', ax=ax_pairing1_toi);
        except:
            pass

        try:
            toi_pairing2 = team_pairing2_teammates_lines_df.plot.barh(x='LINE', y='TOI', color='white', edgecolor=team_color, width=pairing2_width, legend=None, label='', ax=ax_pairing2_toi);
        except:
            pass

        try:
            toi_pairing3 = team_pairing3_teammates_lines_df.plot.barh(x='LINE', y='TOI', color='white', edgecolor=team_color, width=pairing3_width, legend=None, label='', ax=ax_pairing3_toi);
        except:
            pass

        # remove the labels for each subplot
        ax_pairing1_xG.set_xlabel('')
        ax_pairing1_xG.set_ylabel('')

        ax_pairing1_toi.set_xlabel('')
        ax_pairing1_toi.set_ylabel('')

        ax_pairing2_xG.set_xlabel('')
        ax_pairing2_xG.set_ylabel('')

        ax_pairing2_toi.set_xlabel('')
        ax_pairing2_toi.set_ylabel('')

        ax_pairing3_xG.set_xlabel('')
        ax_pairing3_xG.set_ylabel('')

        ax_pairing3_toi.set_xlabel('')
        ax_pairing3_toi.set_ylabel('')
    
        # set vertical indicators for break-even expected goals differential
        ax_pairing1_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
        ax_pairing2_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
        ax_pairing3_xG.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, zorder=0, linestyle=':', color='black')
   
        ### change the tick parameters
        ax_pairing1_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=False)

        ax_pairing1_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=False)

        ax_pairing2_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=False)

        ax_pairing2_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=False)

        ax_pairing3_xG.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=True)

        ax_pairing3_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=True)

        # change the y-axis label colors
        ax_pairing1_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_pairing2_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        ax_pairing3_xG.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)
        
        # create a list of x-axis tick values contingent on the max values for expected goals for and against 
        xGF_max = pairings_teammates_lines_df['xGF']
        xGF_max = xGF_max.max()
        
        xGA_max = pairings_teammates_lines_df['xGA']
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

        toi_tickmax = max_pairings_toi

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
        ax_pairing1_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_pairing1_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
 
        ax_pairing2_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_pairing2_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        ax_pairing3_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_pairing3_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')

        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_pairing1_xG.set_xticks(xG_ticklabels, minor=False)
        ax_pairing1_toi.set_xticks(toi_ticklabels, minor=False)

        ax_pairing2_xG.set_xticks(xG_ticklabels, minor=False)
        ax_pairing2_toi.set_xticks(toi_ticklabels, minor=False)

        ax_pairing3_xG.set_xticks(xG_ticklabels, minor=False)
        ax_pairing3_toi.set_xticks(toi_ticklabels, minor=False)       
        
        # remove the borders to each subplot
        ax_pairing1_xG.spines["top"].set_visible(False)   
        ax_pairing1_xG.spines["bottom"].set_visible(False)    
        ax_pairing1_xG.spines["right"].set_visible(False)    
        ax_pairing1_xG.spines["left"].set_visible(False)

        ax_pairing1_toi.spines["top"].set_visible(False)   
        ax_pairing1_toi.spines["bottom"].set_visible(False)    
        ax_pairing1_toi.spines["right"].set_visible(False)    
        ax_pairing1_toi.spines["left"].set_visible(False)
    
        ax_pairing2_xG.spines["top"].set_visible(False)   
        ax_pairing2_xG.spines["bottom"].set_visible(False)    
        ax_pairing2_xG.spines["right"].set_visible(False)    
        ax_pairing2_xG.spines["left"].set_visible(False)

        ax_pairing2_toi.spines["top"].set_visible(False)   
        ax_pairing2_toi.spines["bottom"].set_visible(False)    
        ax_pairing2_toi.spines["right"].set_visible(False)    
        ax_pairing2_toi.spines["left"].set_visible(False)

        ax_pairing3_xG.spines["top"].set_visible(False)   
        ax_pairing3_xG.spines["bottom"].set_visible(False)    
        ax_pairing3_xG.spines["right"].set_visible(False)    
        ax_pairing3_xG.spines["left"].set_visible(False)

        ax_pairing3_toi.spines["top"].set_visible(False)   
        ax_pairing3_toi.spines["bottom"].set_visible(False)    
        ax_pairing3_toi.spines["right"].set_visible(False)    
        ax_pairing3_toi.spines["left"].set_visible(False)

        # add a legend for the shot type markers
        from matplotlib.lines import Line2D
        elements = [Line2D([0], [0], marker='|', markersize=13, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
        ax_pairing3_xG.legend(handles=elements, loc='center', bbox_to_anchor=(.5, -.50), ncol=2).get_frame().set_linewidth(0.0)
        
        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))
  

        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_units_pairings_teammates + 'onice_xg_away_pairings_teammates_lines.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units_pairings_teammates + 'onice_xg_home_pairings_teammates_lines.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()
        
        
        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' pairings with lines 5v5 on-ice shots.')   
        
    # status update
    print('Finished plotting the 5v5 on-ice shots for pairings with lines.')