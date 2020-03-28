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
    charts_units_pairings = parameters.charts_units_pairings
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    # create variables that point to the .csv processed stats file for pairings
    pairings_file = files_root + 'stats_units_pairings_onice.csv'
    
    # create dataframe objects that read in info from the .csv files
    pairings_df = pd.read_csv(pairings_file)

    max_toi = pairings_df['TOI'].max()  
   
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

    away_cmap = clr.LinearSegmentedColormap.from_list('custom away', [(0,    '#ffffff'), (1, away_color)], N=256)  
    home_cmap = clr.LinearSegmentedColormap.from_list('custom home', [(0,    '#ffffff'), (1, home_color)], N=256)
    
                                                                       
    ###
    ### 5v5
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
            
        # create a pairings dataframe; filter for team; sort by time on ice; keep the pairs with the 3 highest totals; rank and then invert the rankings   
        team_pairings_df = pairings_df.copy()
        team_pairings_df = team_pairings_df[(team_pairings_df['TEAM'] == team)]
        team_pairings_df = team_pairings_df.sort_values(by=['TOI'], ascending = True)
        team_pairings_df = team_pairings_df.iloc[-6:]    
        team_pairings_df['RANK'] = team_pairings_df['TOI'].rank(method='first')
        team_pairings_df['RANK'] -= 1

        # remove zeros from the goals for and against columns       
        team_pairings_df['GF'] = team_pairings_df['GF'].replace(0, np.NaN)       
        team_pairings_df['GA'] = team_pairings_df['GA'].replace(0, np.NaN)

        # remove zeros from the differential column       
        team_pairings_df['SD'] = team_pairings_df['SD'].replace(0, np.NaN)       
        
        # make shots against negative values    
        team_pairings_df['SA'] *= -1
    
        # create another pairings dataframe with just the time on ice column; set a max value; scale each pair's time on ice relative to the max  
        pairings_toi = team_pairings_df['TOI']
    
        max_pairings_toi = max(pairings_toi)
    
        pairings_toi_color = pairings_toi / float(max_pairings_toi)
    
        # connect team and opponent color map colors to each line's scaled time on ice 
        pairings_toi_color_map_for = team_color_map(pairings_toi_color)
        pairings_toi_color_map_against = opponent_color_map(pairings_toi_color)
                     
        # create a figure with two subplots sharing the y-axis
        fig = plt.figure(figsize=(8,8))
        grid = plt.GridSpec(1, 8, hspace=0.75, wspace=0.50)

        ax_pairings_shots = fig.add_subplot(grid[0, 0:-2])
        ax_pairings_toi = fig.add_subplot(grid[0, -1])

        # set the plot title
        fig.suptitle(date + ' Pairings On-Ice Shots\n\n')

        ax_pairings_shots.set_title('5v5 S', fontsize=10)
        ax_pairings_toi.set_title('5v5 TOI', fontsize=10)
        
        # create bars for shots for and against as well as line markers (to note the shot differential) for each pair
        try:
            pairings_SF_plot = team_pairings_df.plot.barh(x='PAIRING', y='SF', stacked=True, color=pairings_toi_color_map_for, width=0.25, legend=None, label='', ax=ax_pairings_shots);
        except:
            pass
        try:
            pairings_SA_plot = team_pairings_df.plot.barh(x='PAIRING', y='SA', stacked=True, color=pairings_toi_color_map_against, width=0.25, legend=None, label='', ax=ax_pairings_shots);
        except:
            pass
        try:
            pairing1_GF_marker = team_pairings_df.plot(x='GF', y='RANK', marker='D', markersize=5,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pairings_shots);
        except:
            pass
        try:
            pairing1_GA_marker = team_pairings_df.plot(x='GA', y='RANK', marker='D', markersize=5,  markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pairings_shots);
        except:
            pass
        try:
            pairings_SD_plot = team_pairings_df.plot(x='SD', y='RANK', marker='|', markersize=19, markerfacecolor='None', markeredgecolor='white', linewidth=0, alpha=1, legend=None, label='', ax=ax_pairings_shots);
        except:
            pass

        # plot the bars for time on ice
        try:
            toi_pairings = team_pairings_df.plot.barh(x='PAIRING', y='TOI', color='white', edgecolor=team_color, width=0.25, legend=None, label='', ax=ax_pairings_toi);
        except:
            pass 
    
        # remove the labels for each subplot
        ax_pairings_shots.set_xlabel('')
        ax_pairings_shots.set_ylabel('')

        ax_pairings_toi.set_xlabel('')
        ax_pairings_toi.set_ylabel('')
        
        # set vertical indicators for break-even shot differential
        ax_pairings_shots.axvspan(0, 0, ymin=0, ymax=1, alpha=.25, linestyle=':', color='black')
    
        # change the tick parameters
        ax_pairings_shots.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=True,   # labels along the left edge are on
                labelbottom=True)

        ax_pairings_toi.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelleft=False,   # labels along the left edge are off
                labelbottom=True)

        # change the y-axis label colors
        ax_pairings_shots.tick_params(
                axis='y',
                which='both',
                labelcolor=opponent_color)

        # create a list of x-axis tick values contingent on the max values for shots for and against 
        SF_max = pairings_df['SF']
        SF_max = SF_max.max()

        SA_max = pairings_df['SA']
        SA_max = SA_max.max()

        S_tickmax = int()
        if SF_max >= SA_max:
            S_tickmax = SF_max
        if SF_max < SA_max:
            S_tickmax = SA_max

        S_ticklabels = []
        if S_tickmax <= 5:
            S_ticklabels = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        if S_tickmax > 5 and S_tickmax <= 10:
            S_ticklabels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
        if S_tickmax > 10 and S_tickmax <= 15:
            S_ticklabels = [-15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15]        
        if S_tickmax > 15 and S_tickmax <= 20:
            S_ticklabels = [-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20]       
        if S_tickmax > 20 and S_tickmax <= 25:
            S_ticklabels = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]

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
        ax_pairings_toi.axvspan(toi_ticklabels[1] / 2, toi_ticklabels[1] / 2, ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
        ax_pairings_toi.axvspan(toi_ticklabels[1], toi_ticklabels[1], ymin=0, ymax=1, zorder=0, alpha=0.25, linestyle=':', color='black')
       
        # use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax_pairings_shots.set_xticks(S_ticklabels, minor=False)
        ax_pairings_toi.set_xticks(toi_ticklabels, minor=False)

        # remove the borders to each subplot
        ax_pairings_shots.spines["top"].set_visible(False)   
        ax_pairings_shots.spines["bottom"].set_visible(False)    
        ax_pairings_shots.spines["right"].set_visible(False)    
        ax_pairings_shots.spines["left"].set_visible(False)

        ax_pairings_toi.spines["top"].set_visible(False)   
        ax_pairings_toi.spines["bottom"].set_visible(False)    
        ax_pairings_toi.spines["right"].set_visible(False)    
        ax_pairings_toi.spines["left"].set_visible(False)
        
        # add a legend for the shot type markers
        from matplotlib.lines import Line2D
        elements = [Line2D([0], [0], marker='D', markersize=5, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Scored'), Line2D([0], [0], marker='|', markersize=13, markerfacecolor='None', markeredgecolor='black', linewidth=0, alpha=1, label='Differential')]
        ax_pairings_shots.legend(handles=elements, loc='center', bbox_to_anchor=(.5, -.1), ncol=2).get_frame().set_linewidth(0.0)
        
        # add text boxes with team names in white and with the team's color in the background  
        fig.text(.425, 0.936, ' ' + away + ' ', color='white', fontsize='12', bbox=dict(facecolor=away_color, edgecolor='None'))
        fig.text(.525, 0.936, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
        fig.text(.490, 0.936, '@', color='black', fontsize='12', bbox=dict(facecolor='white', edgecolor='None'))
    
    
        ###
        ### SAVE TO FILE
        ###
        
        if team == away:
            plt.savefig(charts_units_pairings + 'onice_shots_away_pairings.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units_pairings + 'onice_shots_home_pairings.png', bbox_inches='tight', pad_inches=0.2)    
        
        # exercise a command-line option to show the current figure
        if images == 'show':
            plt.show()

  
        ###
        ### CLOSE
        ###
        
        plt.close(fig)
        
        # status update
        print('Plotting ' + team + ' pairings 5v5 on-ice shots.')   
        
    # status update  
    print('Finished plotting 5v5 on-ice shots for pairings.')