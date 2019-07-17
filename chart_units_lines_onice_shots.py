# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
#import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import parameters

def parse_ids(season_id, game_id, images):

    ### pull common variables from the parameters file
    charts_units = parameters.charts_units
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

    ### create variables that point to the .csv processed stats files for lines
    lines_file = files_root + 'stats_units_lines_onice.csv'
    
    ### create dataframe objects that read in info from the .csv files
    lines_df = pd.read_csv(lines_file)
    
    ### choose colors for each team; set them in a list
    away_color = '#e60000'
    home_color = '#206a92'
    
    team_colors = [away_color, home_color]
    
    ###
    ### 5v5
    ###
    
    ### loop through each team
    for team in teams:
      
        if team == away:
            team_text = 'AWAY'
            team_state = team_text + '_STATE'
            team_strength = team_text + '_STRENGTH'
            team_color = team_colors[0]
            opponent_color = team_colors[1]
            team_color_map = plt.cm.get_cmap('Reds')
            opponent_color_map = plt.cm.get_cmap('Blues')        
    
        if team == home:
            team_text = 'HOME'
            team_state = team_text + '_STATE'
            team_strength = team_text + '_STRENGTH'
            team_color = team_colors[1]
            opponent_color = team_colors[0]
            team_color_map = plt.cm.get_cmap('Blues')
            opponent_color_map = plt.cm.get_cmap('Reds')        
            
        ### create a lines dataframe; filter for team; sort by time on ice; keep the lines with the 8 highest totals; rank and then invert the rankings
        team_lines_df = lines_df.copy()
        team_lines_df = team_lines_df[(team_lines_df['TEAM'] == team)]  
        team_lines_df = team_lines_df.sort_values(by=['TOI'], ascending = True)
        team_lines_df = team_lines_df.iloc[-8:]      
        team_lines_df['RANK'] = team_lines_df['TOI'].rank(method='first')
        team_lines_df = team_lines_df.sort_values(by=['RANK'], ascending = True)
        team_lines_df['RANK'] -= 1
        
        ### make shots against negative values    
        team_lines_df['SA'] *= -1
    
        ### create another lines dataframe with just the time on ice column; set a max value; scale each line's time on ice relative to the max value
        lines_toi = team_lines_df['TOI']
        
        max_lines_toi = max(lines_toi)
    
        lines_toi_color = lines_toi / float(max(lines_toi))
    
        ### connect team and opponent color map colors to each line's scaled time on ice   
        lines_toi_color_map_for = team_color_map(lines_toi_color)
        lines_toi_color_map_against = opponent_color_map(lines_toi_color)    
                     
        ### create a figure with two subplots sharing the y-axis
        fig, ax = plt.subplots(figsize=(8,6))
        
        ### create bars for shots for and against as well as line markers (to note the shot differential) for each line
        try:
            lines_SF_plot = team_lines_df.plot.barh(x='LINE', y='SF', stacked=True, color=lines_toi_color_map_for, width=0.75, legend=None, label='', ax=ax);
        except:
            pass
        try:
            lines_SA_plot = team_lines_df.plot.barh(x='LINE', y='SA', stacked=True, color=lines_toi_color_map_against, width=0.75, legend=None, label='', ax=ax);
        except:
            pass    
        try:
            lines_SD_plot = team_lines_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=8, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=ax);
        except:
            pass
    
        ### remove the labels for each subplot
        ax.set_xlabel('')
        ax.set_ylabel('')
    
        ### set vertical indicators for break-even shot differential
        ax.axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
    
        ### change the tick parameters
        ax.tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelbottom=True)

        ### create a list of x-axis tick values contingent on the max values for shots for and against 
        SF_max = team_lines_df['SF']
        SF_max = SF_max.max()
        SA_max = team_lines_df['SA']
        SA_max *= -1
        SA_max = SA_max.max()

        if SF_max >= SA_max:
            x_tickmax = SF_max
        elif SF_max < SA_max:
            x_tickmax = SA_max

        x_ticklabels = []
        if x_tickmax <= 5:
            x_ticklabels = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        if x_tickmax > 5 and x_tickmax <= 10:
            x_ticklabels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
        if x_tickmax > 10 and x_tickmax <= 15:
            x_ticklabels = [-15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15]        
        if x_tickmax > 15 and x_tickmax <= 20:
            x_ticklabels = [-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20]       
        if x_tickmax > 20 and x_tickmax <= 25:
            x_ticklabels = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
        
        ### use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax.set_xticks(x_ticklabels, minor=False)

        ### remove the borders to each subplot
        ax.spines["top"].set_visible(False)   
        ax.spines["bottom"].set_visible(False)    
        ax.spines["right"].set_visible(False)    
        ax.spines["left"].set_visible(False)
    
        ### insert time on ice colorbars for each axis
        lines_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        lines_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=lines_norm)
        lines_sm.set_array([])
        lines_color_bar = plt.colorbar(lines_sm, ax=ax)
        from matplotlib import ticker
        tick_locator = ticker.MaxNLocator(nbins=4)
        lines_color_bar.locator = tick_locator
        lines_color_bar.update_ticks()
        lines_color_bar.ax.set_yticklabels(['0', '', '', '', max_lines_toi])
        lines_color_bar.set_label('Time On Ice', rotation=270)
    
        ### set the plot title
        plt.title(date + ' Forward Lines 5v5 On-Ice Shots\n ' + away + ' @ ' + home + '\n')
    
    
        ### save the image to file
        if team == away:
            plt.savefig(charts_units + 'onice_shots_away_lines.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units + 'onice_shots_home_lines.png', bbox_inches='tight', pad_inches=0.2)    
        
        ### show the current figure
        if images == 'show':
            plt.show()
        
        ### close the current figure   
        plt.close(fig)
        
        
        print('Plotting ' + team + ' lines 5v5 on-ice shots.')   
        
        
    print('Finished plotting 5v5 on-ice shots for lines.')