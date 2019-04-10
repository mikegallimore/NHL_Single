# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: @mikegallimore
"""
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
charts_players = parameters.charts_players
files_root = parameters.files_root

### create variables that point to the .csv processed stats files for players
players_file = files_root + 'stats_players_onice.csv'

### create a dataframe object that reads in info from the .csv files
players_df = pd.read_csv(players_file)

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

    ### create a dataframe; filter for team; sort by team, game state and position; rank by time on ice and then invert the rankings
    team_df = players_df.copy()
    team_df = team_df.sort_values(by=['TOI'], ascending = True)
    team_df = team_df[(team_df['TEAM'] == team) & (team_df['STATE'] == '5v5') & (team_df['POS'] != 'G')]
    team_df['RANK'] = team_df['TOI'].rank(method='first')
    team_df['RANK'] -= 1
    team_df['SA'] *= -1

    ### create a dataframe with just the time on ice column; set a max value; scale each player's time on ice relative to the max
    toi = team_df['TOI']
    
    max_toi = max(toi)

    toi_color = toi / float(max(toi))

    ### connect team and opponent color map colors to each line's scaled time on ice   
    toi_color_map_for = team_color_map(toi_color)
    toi_color_map_against = opponent_color_map(toi_color)    
              
    ### create a figure with two subplots sharing the y-axis
    fig, ax = plt.subplots(figsize=(8,6))
    
     ### set the plot title
    ax.set_title(date + ' Skaters 5v5 On-Ice Shots\n ' + away + ' @ ' + home + '\n' )

    ### create bars for shots and against and line markers (to note the shot differential) for each pair
    try:
        SF_plot = team_df.plot.barh(x='PLAYER', y='SF', stacked=True, color=toi_color_map_for, width=0.75, legend=None, label='', ax=ax);
    except:
        pass
    try:
        SA_plot = team_df.plot.barh(x='PLAYER', y='SA', stacked=True, color=toi_color_map_against, width=0.75, legend=None, label='', ax=ax);
    except:
        pass    
    try:
        SD_plot = team_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=8, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=ax);
    except:
        pass

    ### remove the y-labels for the plot
    ax.set_xlabel('')
    ax.set_ylabel('')

    ### set vertical indicators for break-even shot differential
    ax.axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')

    ### change the tick parameters for each axes
    ax.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=False) # labels along the bottom edge are off
    
    ### remove the borders to each subplot
    ax.spines["top"].set_visible(False)   
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)  

    ### insert a time on ice colorbar
    norm = mpl.colors.Normalize(vmin=0,vmax=1)
    sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=norm)
    sm.set_array([])
    color_bar = plt.colorbar(sm, ax=ax)
    color_bar.ax.set_yticklabels(['0', '', '', '' , '', max_toi])
    color_bar.set_label('Time On Ice', rotation=270)

    ### save the image to file
    if team == away:
        plt.savefig(charts_players + 'skaters_5v5_onice_shots_away.png', bbox_inches='tight', pad_inches=0.2)
    elif team == home:
        plt.savefig(charts_players + 'skaters_5v5_onice_shots_home.png', bbox_inches='tight', pad_inches=0.2)    
    
    ### show and then close the current figure
    plt.show()
    plt.close(fig)
    
    
    print('Plotting ' + team + ' skaters 5v5 on-ice shots.')   
    
    
print('Finished plotting the 5v5 on-ice shots for players.')