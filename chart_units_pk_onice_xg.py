# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
#import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parameters
import matplotlib.colors as clr
import dict_team_colors
import mod_switch_colors

def parse_ids(season_id, game_id, images):

    # pull common variables from the parameters file
    charts_units_pk = parameters.charts_units_pk
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    # create variables that point to the .csv processed stats files for lines
    pk_file = files_root + 'stats_units_pk_onice.csv'
    
    # create dataframe objects that read in info from the .csv files
    pk_df = pd.read_csv(pk_file)

    max_toi = pk_df['TOI'].max()  
    
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
    ### PP
    ###
    
    # loop through each team
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
            
        # create a lines dataframe; filter for team; sort by time on ice; keep the lines with the 8 highest totals; rank and then invert the rankings
        team_pk_df = pk_df.copy()
        team_pk_df = team_pk_df[(team_pk_df['TEAM'] == team)]  
        team_pk_df = team_pk_df.sort_values(by=['TOI'], ascending = True)
        team_pk_df = team_pk_df.iloc[-8:]      
        team_pk_df['RANK'] = team_pk_df['TOI'].rank(method='first')
        team_pk_df = team_pk_df.sort_values(by=['RANK'], ascending = True)
        team_pk_df['RANK'] -= 1
 
        team_pk_df['UNIT'] = team_pk_df['UNIT'] + ' (' + team_pk_df['STRENGTH'] + ')'
    
        # remove zeros from the differential column       
        team_pk_df['xGD'] = team_pk_df['xGD'].replace(0, np.NaN)       
       
        # make expected goals against negative values    
        team_pk_df['xGA'] *= -1
   
        # create another lines dataframe with just the time on ice column; set a max value; scale each line's time on ice relative to the max value
        pk_toi = team_pk_df['TOI']     
        team_max_pk_toi = pk_toi.max()
    
        pk_toi_color = pk_toi / float(team_max_pk_toi)
    
        # connect team and opponent color map colors to each line's scaled time on ice   
        pk_toi_color_map_for = team_color_map(pk_toi_color)
        pk_toi_color_map_against = opponent_color_map(pk_toi_color)    
                     
        # create a figure with two subplots sharing the y-axis
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(1, 8, hspace=0.75, wspace=0.50)

        ax_pk_xg = fig.add_subplot(grid[0, 0:-2])
        ax_pk_toi = fig.add_subplot(grid[0, -1])

        # set the plot title
        fig.suptitle(date + ' Penalty Kill Units On-Ice Expected Goals\n\n')

        ax_pk_xg.set_title('5v5 xG', fontsize=10)
        ax_pk_toi.set_title('5v5 TOI', fontsize=10)
           
        # create bars for expected goals for and against as well as line markers (to note the expected goals differential) for each line
        try:
            pk_xGF_plot = team_pk_df.plot.barh(x='UNIT', y='xGF', stacked=True, color=pk_toi_color_map_for, width=0.25, legend=None, label='', ax=ax_pk_xg);
        except:
            pass
        try:
            pk_xGA_plot = team_pk_df.plot.barh(x='UNIT', y='xGA', stacked=True, color=pk_toi_color_map_against, width=0.25, legend=None, label='', ax=ax_pk_xg);
        except:
            pass    
        try:
            pk_xGD_plot = team_pk_df.plot(x='xGD', y='RANK', marker='|', markersize=15, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pk_xg);
        except:
            pass

        # plot the bars for time on ice
        try:
            toi_pk = team_pk_df.plot.barh(x='UNIT', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_pk_toi);
        except:
            pass
    
        # remove the labels for each subplot
        ax_pk_xg.set_xlabel('')
        ax_pk_xg.set_ylabel('')

        ax_pk_toi.set_xlabel('')
        ax_pk_toi.set_ylabel('')
    
        # set vertical indicators for break-even expected goals differential
        ax_pk_xg.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
    
        # change the tick parameters
        ax_pk_xg.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=True)

        ax_pk_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=True)

        # change the y-axis label colors
        ax_pk_xg.tick_params(
                axis='y',
                which='both',
                labelcolor=team_color)

        # create a list of x-axis tick values contingent on the max values for expected goals for and against 
        xGF_max = pk_df['xGF']
        xGF_max = xGF_max.max()

        xGA_max = pk_df['xGA']
        xGA_max = xGA_max.max()

        xG_tickmax = int()
        if xGF_max > xGA_max:
            xG_tickmax = xGF_max
        if xGF_max < xGA_max:
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
        ax_pk_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_pk_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        
        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_pk_xg.set_xticks(xG_ticklabels, minor=False)
        ax_pk_toi.set_xticks(toi_ticklabels, minor=False)

        # remove the borders to each subplot
        ax_pk_xg.spines["top"].set_visible(False)   
        ax_pk_xg.spines["bottom"].set_visible(False)    
        ax_pk_xg.spines["right"].set_visible(False)    
        ax_pk_xg.spines["left"].set_visible(False)

        ax_pk_toi.spines["top"].set_visible(False)   
        ax_pk_toi.spines["bottom"].set_visible(False)    
        ax_pk_toi.spines["right"].set_visible(False)    
        ax_pk_toi.spines["left"].set_visible(False)
    
        # add a legend for the shot type markers
        from matplotlib.lines import Line2D
        elements = [Line2D([0], [0], marker='|', markersize=13, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
        ax_pk_xg.legend(handles=elements, loc='center', bbox_to_anchor=(.5, -.1), ncol=2).get_frame().set_linewidth(0.0)
 
        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))

    
        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_units_pk + 'onice_xg_away_pk.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units_pk + 'onice_xg_home_pk.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()
        
        
        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' power play units on-ice xG.')   
        
    # status update    
    print('Finished plotting on-ice xG for power play units.')