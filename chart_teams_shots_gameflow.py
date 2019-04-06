# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: @mikegallimore
"""
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import parameters

season_id = parameters.season_id
game_id = parameters.game_id

charts_teams = parameters.charts_teams
files_root = parameters.files_root

### pulls schedule info
schedule_csv = files_root + season_id + "_schedule.csv"

schedule_df = pd.read_csv(schedule_csv)
#print(schedule_df)
schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
date = schedule_date['DATE'].item()
home = schedule_date['HOME'].item()
away = schedule_date['AWAY'].item()
#print(date, home, away)

### opens the game's livefeed (JSON) file to create a few shared variables
livefeed_file = files_root + 'livefeed.json'
with open(livefeed_file) as livefeed_json:
    livefeed_data = json.load(livefeed_json)
    livefeed_parsed = livefeed_data

    try:
        game_status = livefeed_parsed["liveData"]["linescore"]["currentPeriodTimeRemaining"]
#        print(game_status)
        currentperiod = livefeed_parsed["liveData"]["linescore"]["currentPeriod"]
#        print(currentperiod)

        if game_status != 'Final' and currentperiod < 4:
            game_type = 'Regulation'
        elif game_status != 'Final' and currentperiod > 3:
            game_type = 'Overtime'
        elif game_status == 'Final' and currentperiod < 4:
            game_type = 'Regulation'
        elif game_status == 'Final' and currentperiod > 3:
            game_type = 'Overtime'
    except:
        game_type = ''

#    print(game_type)

### creates a variable that points to the .csv TOI matrix file
toi_file = files_root + 'TOI_matrix.csv'

### creates a dataframe object that reads in info from the .csv play-by-file file
toi_df = pd.read_csv(toi_file)

### creates a variable that points to the .csv play-by-play file
pbp_file = files_root + 'pbp.csv'

### creates a dataframe object that reads in info from the .csv play-by-file file
pbp_df = pd.read_csv(pbp_file)

### sets the color options
away_color = '#e60000'
home_color = '#206a92'
legend_color = 'black'
colors = [away_color, home_color, legend_color]

### create a separate dataframe for seconds spent with teams on a power play in order to generate shaded bars indicating so on the chart
pp_toi = toi_df.copy()

pp_toi_df = pp_toi[(pp_toi['HOME_STATE'] == 'PP') | (pp_toi['AWAY_STATE'] == 'PP')]

home_pp = pp_toi_df[(pp_toi_df['HOME_STATE'] == 'PP')]
away_pp = pp_toi_df[(pp_toi_df['AWAY_STATE'] == 'PP')]

###
### ALL
###

### condenses and modifies the play-by-play dataframe
gameflow = pbp_df.copy()

gameflow_df = gameflow[(gameflow['EVENT'] == 'Shot')]
gameflow_df = gameflow_df.drop(columns=['HOME_SITUATION', 'AWAY_SITUATION', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'X_1', 'Y_1', 'X_2', 'Y_2', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])

home_unblocked_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
gameflow_df['HOME_UNBLOCKED_SHOTS'] = home_unblocked_shots.cumsum()
away_unblocked_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
gameflow_df['AWAY_UNBLOCKED_SHOTS'] = away_unblocked_shots.cumsum()

home_unblocked_shotsdiff = home_unblocked_shots - away_unblocked_shots
away_unblocked_shotsdiff = away_unblocked_shots - home_unblocked_shots
gameflow_df['HOME_UNBLOCKED_SHOTSDIFF'] = home_unblocked_shotsdiff.cumsum()
gameflow_df['AWAY_UNBLOCKED_SHOTSDIFF'] = away_unblocked_shotsdiff.cumsum()

home_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
gameflow_df['HOME_SHOTS'] = home_shots.cumsum()
away_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
gameflow_df['AWAY_SHOTS'] = away_shots.cumsum()

home_shotsdiff = home_shots - away_shots
away_shotsdiff = away_shots - home_shots
gameflow_df['HOME_SHOTSDIFF'] = home_shotsdiff.cumsum()
gameflow_df['AWAY_SHOTSDIFF'] = away_shotsdiff.cumsum()

### write new dataframe to file
gameflow_df.to_csv(files_root + 'gameflow.csv', encoding='utf-8', index=False)

### create a separate dataframe exclusively for goals
goals = gameflow_df.copy()

goals_df = goals[(goals['EVENT_TYPE'] == 'Goal')]

home_goals = goals_df[(goals_df['TEAM'] == home)]
#print(home_goals)
away_goals = goals_df[(goals_df['TEAM'] == away)]
#print(away_goals)

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))

### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with  
try:
    home_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] >= 0)]
except:
    pass
try:
    away_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] <= 0)]
except:
    pass

### plotting
    
try:
    home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, label='', ax=ax);
except:
    pass
try:
    away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, label='', ax=ax);
except:
    pass

try:
    home_advantage_plot_step = plt.step(x=home_advantage['SECONDS_GONE'], y=home_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[1], label='');
except:
    pass

try:
    away_advantage_plot_step = plt.step(x=away_advantage['SECONDS_GONE'], y=away_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[0], label='');
except:
    pass

try:
    home_goals_plot = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
except:
    pass

try:
    away_goals_plot = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[0], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
except:
    pass

if home_goals.empty == False:
    goals_label = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)
elif home_goals.empty == True and away_goals.empty == False:
    goals_label = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)   


### sets the break-even line
if game_type == 'Regulation':
    breakeven_x, breakeven_y = [-0,3600],[0,0]
elif game_type == 'Overtime':
    breakeven_x, breakeven_y = [-0,3900],[0,0]
clear_breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = 'white', alpha=1)
breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = colors[2], alpha=0.15)

### sets vertical indicators for the end of each period
ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=1, color=colors[2], linewidth=0, label='Power Play')
ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=0.15, color=colors[2])
ax.axvspan(2400, 2401, ymin=0, ymax=1, alpha=0.15, color=colors[2])
ax.axvspan(3600, 3601, ymin=0, ymax=1, alpha=0.15, color=colors[2])
if game_type == 'Overtime':
    ax.axvspan(3900, 3901, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    
### sets vertical shaded areas indcating power play and empty-net situations
for second in home_pp['SECONDS_GONE']:
#   print(second)
    ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[1])
    
for second in away_pp['SECONDS_GONE']:
    ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[0])

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(True)

### adjustments to the first axex
ax.spines["top"].set_visible(False)   
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False)  

### remove ticks to the first axes
ax.tick_params(axis='y', which="both", left=False, right=False, length=0)

### create a second axes that shares the same x-axis
ax2 = ax.twinx()

### adds another round of non-visible lines to flesh out the right y-axis scale
home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, ax=ax2);
away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, ax=ax2);

### helps eliminate whitespace
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(True)

### adjustments to the second axes
ax2.spines["top"].set_visible(False)   
ax2.spines["bottom"].set_visible(False)    
ax2.spines["right"].set_visible(False)    
ax2.spines["left"].set_visible(False)  

### get the maximum and minimum values in the shot differential column in order to set the y-values for the period labels
max_home_shotdiff = gameflow_df['HOME_SHOTSDIFF'].max()
min_home_shotdiff = gameflow_df['HOME_SHOTSDIFF'].min()

max_away_shotdiff = gameflow_df['AWAY_SHOTSDIFF'].max()
min_away_shotdiff = gameflow_df['AWAY_SHOTSDIFF'].min()

### remove ticks to the second axes
ax2.tick_params(axis='y', which="both", left=False, right=False, length=0)

### inverts the second y-axis
ax2.invert_yaxis()


### sets the team labels

if max_home_shotdiff > max_away_shotdiff and game_type == 'Regulation':
    plt.text(-660, min_away_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
    plt.text(4060, max_home_shotdiff, away, fontsize=12, color=colors[0], alpha=1)
elif max_home_shotdiff < max_away_shotdiff and game_type == 'Regulation':
    plt.text(-660, min_home_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
    plt.text(4060, max_away_shotdiff, away, fontsize=12, color=colors[0], alpha=1)

if max_home_shotdiff > max_away_shotdiff and game_type == 'Overtime':
    plt.text(-660, min_away_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
    plt.text(4350, max_home_shotdiff, away, fontsize=12, color=colors[0], alpha=1)
elif max_home_shotdiff < max_away_shotdiff and game_type == 'Overtime':
    plt.text(-660, min_home_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
    plt.text(4350, max_away_shotdiff, away, fontsize=12, color=colors[0], alpha=1)

### sets the period names as labels
if game_type == 'Regulation':
    plt.text(0.33, -0.05, '1st', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.63, -0.05, '2nd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.93, -0.05, '3rd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)

if game_type == 'Overtime':
    plt.text(0.31, -0.05, '1st', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.58, -0.05, '2nd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.86, -0.05, '3rd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.94, -0.05, 'OT', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)

### sets the plot title
plt.title(date + ' Shot Differential\n' + away + ' @ ' + home + '\n')

### sets the location of the plot legend
ax.legend(loc='center', bbox_to_anchor=(.5, 1.025), ncol=2).get_frame().set_linewidth(0.0)

### saves the image to file
plt.savefig(charts_teams + 'shots_gameflow.png', bbox_inches='tight', pad_inches=0.2)

plt.show()
plt.close(fig)

print('Finished plotting the shot differential game flow for all situations.')

###
### 5v5
###

### condenses and modifies the play-by-play dataframe
gameflow = pbp_df.copy()

gameflow_df = gameflow[(gameflow['EVENT'] == 'Shot') & (gameflow['HOME_STRENGTH'] == '5v5')]
gameflow_df = gameflow_df.drop(columns=['HOME_SITUATION', 'AWAY_SITUATION', 'HOME_STATE', 'AWAY_STATE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'X_1', 'Y_1', 'X_2', 'Y_2', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])

home_unblocked_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
gameflow_df['HOME_UNBLOCKED_SHOTS'] = home_unblocked_shots.cumsum()
away_unblocked_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
gameflow_df['AWAY_UNBLOCKED_SHOTS'] = away_unblocked_shots.cumsum()

home_unblocked_shotsdiff = home_unblocked_shots - away_unblocked_shots
away_unblocked_shotsdiff = away_unblocked_shots - home_unblocked_shots
gameflow_df['HOME_UNBLOCKED_SHOTSDIFF'] = home_unblocked_shotsdiff.cumsum()
gameflow_df['AWAY_UNBLOCKED_SHOTSDIFF'] = away_unblocked_shotsdiff.cumsum()

home_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
gameflow_df['HOME_SHOTS'] = home_shots.cumsum()
away_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
gameflow_df['AWAY_SHOTS'] = away_shots.cumsum()

home_shotsdiff = home_shots - away_shots
away_shotsdiff = away_shots - home_shots
gameflow_df['HOME_SHOTSDIFF'] = home_shotsdiff.cumsum()
gameflow_df['AWAY_SHOTSDIFF'] = away_shotsdiff.cumsum()

### write new dataframe to file
gameflow_df.to_csv(files_root + 'gameflow_5v5.csv', encoding='utf-8', index=False)

### create a separate dataframe exclusively for goals
goals = gameflow_df.copy()

goals_df = goals[(goals['EVENT_TYPE'] == 'Goal')]

home_goals = goals_df[(goals_df['TEAM'] == home)]
#print(home_goals)
away_goals = goals_df[(goals_df['TEAM'] == away)]
#print(away_goals)

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))

### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with  
try:
    home_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] >= 0)]
except:
    pass
try:
    away_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] <= 0)]
except:
    pass

### plotting
    
try:
    home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, label='', ax=ax);
except:
    pass
try:
    away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, label='', ax=ax);
except:
    pass

try:
    home_advantage_plot_step = plt.step(x=home_advantage['SECONDS_GONE'], y=home_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[1], label='');
except:
    pass

try:
    away_advantage_plot_step = plt.step(x=away_advantage['SECONDS_GONE'], y=away_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[0], label='');
except:
    pass

try:
    home_goals_plot = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
except:
    pass
try:
    away_goals_plot = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[0], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
except:
    pass

if home_goals.empty == False:
    goals_label = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)
elif home_goals.empty == True and away_goals.empty == False:
    goals_label = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)   

    
### sets the break-even line
breakeven_x, breakeven_y = [-0,3600],[0,0]
clear_breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = 'white', alpha=1)
breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = colors[2], alpha=0.15)

### sets vertical indicators for the end of each period
ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=1, color=colors[2], linewidth=0, label='Power Play')
ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=0.15, color=colors[2])
ax.axvspan(2400, 2401, ymin=0, ymax=1, alpha=0.15, color=colors[2])
ax.axvspan(3600, 3601, ymin=0, ymax=1, alpha=0.15, color=colors[2])

### sets vertical shaded areas indcating power play and empty-net situations
for second in home_pp['SECONDS_GONE']:
#   print(second)
    ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[1])
    
for second in away_pp['SECONDS_GONE']:
    ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[0])

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(True)

### adjustments to the first axex
ax.spines["top"].set_visible(False)   
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False)  

### remove ticks to the first axes
ax.tick_params(axis='y', which="both", left=False, right=False, length=0)

### create a second axes that shares the same x-axis
ax2 = ax.twinx()

### adds another round of non-visible lines to flesh out the right y-axis scale
try:
    home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, ax=ax2);
except:
    pass
try:
    away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, ax=ax2);
except:
    pass

### helps eliminate whitespace
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(True)

### adjustments to the second axes
ax2.spines["top"].set_visible(False)   
ax2.spines["bottom"].set_visible(False)    
ax2.spines["right"].set_visible(False)    
ax2.spines["left"].set_visible(False)  

### get the maximum and minimum values in the shot differential column in order to set the y-values for the period labels
max_home_shotdiff = gameflow_df['HOME_SHOTSDIFF'].max()
min_home_shotdiff = gameflow_df['HOME_SHOTSDIFF'].min()

max_away_shotdiff = gameflow_df['AWAY_SHOTSDIFF'].max()
min_away_shotdiff = gameflow_df['AWAY_SHOTSDIFF'].min()

### remove ticks to the second axes
ax2.tick_params(axis='y', which="both", left=False, right=False, length=0)

### inverts the second y-axis
ax2.invert_yaxis()

### sets the team labels
if max_home_shotdiff > max_away_shotdiff:
    plt.text(-660, min_away_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
    plt.text(4060, max_home_shotdiff, away, fontsize=12, color=colors[0], alpha=1)
elif max_home_shotdiff < max_away_shotdiff:
    plt.text(-660, min_home_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
    plt.text(4060, max_away_shotdiff, away, fontsize=12, color=colors[0], alpha=1)

### sets the period names as labels
plt.text(0.33, -0.05, '1st', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
plt.text(0.63, -0.05, '2nd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
plt.text(0.93, -0.05, '3rd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)

### sets the plot title
plt.title(date + ' 5v5 Shot Differential\n' + away + ' @ ' + home + '\n')

### sets the location of the plot legend
ax.legend(loc='center', bbox_to_anchor=(.5, 1.025), ncol=2).get_frame().set_linewidth(0.0)

### saves the image to file
plt.savefig(charts_teams + 'shots_gameflow_5v5.png', bbox_inches='tight', pad_inches=0.2)

plt.show()
plt.close(fig)

print('Finished plotting the 5v5 shot differential game flow.')