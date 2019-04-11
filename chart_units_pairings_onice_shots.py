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

### pull common variables from the parameters file
season_id = parameters.season_id
game_id = parameters.game_id
date = parameters.date
home = parameters.home
away = parameters.away
teams = parameters.teams
charts_units = parameters.charts_units
files_root = parameters.files_root

### create variables that point to the .csv processed stats file for pairings
pairings_file = files_root + 'stats_units_pairings_onice.csv'

### create dataframe objects that read in info from the .csv files
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
        
    ### create a pairings dataframe; filter for team; sort by time on ice; keep the pairs with the 3 highest totals; rank and then invert the rankings   
    team_pairings_df = pairings_df.copy()
    team_pairings_df = team_pairings_df[(team_pairings_df['TEAM'] == team)]
    team_pairings_df = team_pairings_df.sort_values(by=['TOI'], ascending = True)
    team_pairings_df = team_pairings_df.iloc[-6:]    
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
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### create bars for shots for and against as well as line markers (to note the shot differential) for each pair
    try:
        pairings_SF_plot = team_pairings_df.plot.barh(x='PAIRING', y='SF', stacked=True, color=pairings_toi_color_map_for, width=0.5, legend=None, label='', ax=ax);
    except:
        pass
    try:
        pairings_SA_plot = team_pairings_df.plot.barh(x='PAIRING', y='SA', stacked=True, color=pairings_toi_color_map_against, width=0.5, legend=None, label='', ax=ax);
    except:
        pass
    try:
        pairings_SD_plot = team_pairings_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=8, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=ax);
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
            labelbottom=False)

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
    lines_color_bar.ax.set_yticklabels(['0', '', '', '' , '', max_pairings_toi])
    lines_color_bar.set_label('Time On Ice', rotation=270)

    ### set the plot title
    plt.title(date + ' Defense Pairings 5v5 On-Ice Shots\n ' + away + ' @ ' + home + '\n')


    ### save the image to file
    if team == away:
        plt.savefig(charts_units + 'onice_shots_away_pairings.png', bbox_inches='tight', pad_inches=0.2)
    elif team == home:
        plt.savefig(charts_units + 'onice_shots_home_pairings.png', bbox_inches='tight', pad_inches=0.2)    
    
    ### show and then close the current figure
    plt.show()
    plt.close(fig)
    
    
    print('Plotting ' + team + ' pairings 5v5 on-ice shots.')   
    
    
print('Finished plotting the 5v5 on-ice shots for lines and pairings.')