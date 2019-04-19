# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

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

    ### create variables that point to the .csv processed stats files for lines and pairings
    lines_file = files_root + 'stats_units_lines_onice.csv'
    pairings_file = files_root + 'stats_units_pairings_onice.csv'
    
    ### create dataframe objects that read in info from the .csv files
    lines_df = pd.read_csv(lines_file)
    pairings_df = pd.read_csv(pairings_file)
    
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
            
        ### create a lines dataframe; filter for team; sort by time on ice; keep the lines with the 4 highest totals; rank and then invert the rankings
        team_lines_df = lines_df.copy()
        team_lines_df = team_lines_df[(team_lines_df['TEAM'] == team)]  
        team_lines_df = team_lines_df.sort_values(by=['TOI'], ascending = True)
        team_lines_df = team_lines_df.iloc[-4:]      
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
               
        ### create a pairings dataframe; filter for team; sort by time on ice; keep the pairs with the 3 highest totals; rank and then invert the rankings   
        team_pairings_df = pairings_df.copy()
        team_pairings_df = team_pairings_df[(team_pairings_df['TEAM'] == team)]
        team_pairings_df = team_pairings_df.sort_values(by=['TOI'], ascending = True)
        team_pairings_df = team_pairings_df.iloc[-3:]    
        team_pairings_df['RANK'] = team_pairings_df['TOI'].rank(method='first')
        team_pairings_df['RANK'] -= 1
        
        ### make shots against negative values    
        team_pairings_df['SA'] *= -1
    
        ### create another pairings dataframe with just the time on ice column; set a max value; scale each pair's time on ice relative to the max  
        pairings_toi = team_pairings_df['TOI']
    
        max_pairings_toi = max(pairings_toi)
    
        pairings_toi_color = pairings_toi / float(max(pairings_toi))
    
        ### connect team and opponent color map colors to each line's scaled time on ice 
        pairings_toi_color_map_for = team_color_map(pairings_toi_color)
        pairings_toi_color_map_against = opponent_color_map(pairings_toi_color)
           
        ### create a figure with two subplots sharing the y-axis
        fig, axarr = plt.subplots(2, sharex=True)
        
        ### set the plot title
        axarr[0].set_title(date + ' Unit 5v5 On-Ice Shots\n ' + away + ' @ ' + home + '\n' )
    
        ### create bars for shots for and against as well as line markers (to note the shot differential) for each line
        try:
            lines_SF_plot = team_lines_df.plot.barh(x='LINE', y='SF', stacked=True, color=lines_toi_color_map_for, width=0.75, legend=None, label='', ax=axarr[0]);
        except:
            pass
        try:
            lines_SA_plot = team_lines_df.plot.barh(x='LINE', y='SA', stacked=True, color=lines_toi_color_map_against, width=0.75, legend=None, label='', ax=axarr[0]);
        except:
            pass    
        try:
            lines_SD_plot = team_lines_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=8, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=axarr[0]);
        except:
            pass
    
        ### create bars for shots for and against as well as line markers (to note the shot differential) for each pair
        try:
            pairings_SF_plot = team_pairings_df.plot.barh(x='PAIRING', y='SF', stacked=True, color=pairings_toi_color_map_for, width=0.5, legend=None, label='', ax=axarr[1]);
        except:
            pass
        try:
            pairings_SA_plot = team_pairings_df.plot.barh(x='PAIRING', y='SA', stacked=True, color=pairings_toi_color_map_against, width=0.5, legend=None, label='', ax=axarr[1]);
        except:
            pass
        try:
            pairings_SD_plot = team_pairings_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=8, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=axarr[1]);
        except:
            pass
        
        ### remove the labels for each subplot
        axarr[0].set_xlabel('')
        axarr[0].set_ylabel('')
    
        axarr[1].set_xlabel('')    
        axarr[1].set_ylabel('')  
    
        ### set vertical indicators for break-even shot differential
        axarr[0].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
        axarr[1].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
    
        ### change the tick parameters for each axes
        axarr[0].tick_params(
                axis='both',
                which='both',
                bottom=False,
                top=False,
                left=False,
                labelbottom=False)
        
        axarr[1].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=True)
    
        ### remove the borders to each subplot
        axarr[0].spines["top"].set_visible(False)   
        axarr[0].spines["bottom"].set_visible(False)    
        axarr[0].spines["right"].set_visible(False)    
        axarr[0].spines["left"].set_visible(False)  
    
        axarr[1].spines["top"].set_visible(False)   
        axarr[1].spines["bottom"].set_visible(False)    
        axarr[1].spines["right"].set_visible(False)    
        axarr[1].spines["left"].set_visible(False)  
    
        ### insert time on ice colorbars for each axis
        lines_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        lines_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=lines_norm)
        lines_sm.set_array([])
        lines_color_bar = plt.colorbar(lines_sm, ax=axarr[0])
        lines_color_bar.ax.set_yticklabels(['0', '', '', '' , '', max_lines_toi])
        lines_color_bar.set_label('Time On Ice', rotation=270)
    
        pairings_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        pairings_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=pairings_norm)
        pairings_sm.set_array([])
        pairings_color_bar = plt.colorbar(pairings_sm, ax=axarr[1])
        pairings_color_bar.ax.set_yticklabels(['0', '', '', '', '', max_pairings_toi])
        pairings_color_bar.set_label('Time On Ice', rotation=270)
    
        ### save the image to file
        if team == away:
            plt.savefig(charts_units + 'onice_shots_away.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units + 'onice_shots_home.png', bbox_inches='tight', pad_inches=0.2)    
        
        ### show the current figure
        if images == 'show':
            plt.show()
        
        ### close the current figure   
        plt.close(fig)
        
        
        print('Plotting ' + team + ' lines and pairings 5v5 on-ice shots.')   
        
        
    print('Finished plotting the 5v5 on-ice shots for lines and pairings.')