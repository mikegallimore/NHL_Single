# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: @mikegallimore
"""
import pandas as pd
import matplotlib.pyplot as plt
import parameters

season_id = parameters.season_id
game_id = parameters.game_id

charts_teams_period = parameters.charts_teams_period

files_root = parameters.files_root

### pulls schedule info
schedule_csv = files_root + season_id + "_schedule.csv"

schedule_df = pd.read_csv(schedule_csv)
#print(schedule_df)
schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
date = schedule_date['DATE'].item()
home = schedule_date['HOME'].item()
away = schedule_date['AWAY'].item()
#print(date)

### creates a variable that points to the .csv teams stats file
stats_teams_file = files_root + 'stats_teams_period.csv'

stats_teams_df = pd.read_csv(stats_teams_file)


### creates a variable that points to the .csv play-by-play file
pbp_file = files_root + 'pbp.csv'

### creates a dataframe object that reads in info from the .csv play-by-file file
pbp_df = pd.read_csv(pbp_file)
pbp_df['X_1'] *= -1
pbp_df['Y_1'] *= -1
pbp_df['X_2'] *= -1
pbp_df['Y_2'] *= -1

### sets the color options
away_color = '#e60000'
home_color = '#206a92'
legend_color = 'black'
colors = [away_color, home_color, legend_color]

###
### 1ST PERIOD
###

period = 1
   
###
### ALL
###

toi_all_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['PERIOD'] == '1st')]
toi_all = toi_all_df['TOI'].item()
#print(toi_all)

away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])
home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])

away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
   
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 1st Period Unblocked Shots\n' + str(toi_all) + ' Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_1st.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 1st period unblocked shots.')
    
###
### 5v5
###

toi_5v5_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['PERIOD'] == '1st')]
toi_5v5 = toi_5v5_df['TOI'].item()
#print(toi_5v5)

away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)].count()[1])
home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
 
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 1st Period Unblocked Shots\n' + str(toi_5v5) + ' 5v5 Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_5v5_1st.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for 1st period unblocked 5v5 shots.')
    
###
### AWAY PP
###

toi_awayPP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['PERIOD'] == '1st')]
toi_awayPP = toi_awayPP_df['TOI'].item()
#print(toi_awayPP)

away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
   
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
plt.text(-95, 45, 'PP', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 1st Period Unblocked Shots\n' + str(toi_awayPP) + ' Away PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_pp_away_1st.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 1st period unblocked shots during an away PP.')
    
###
### HOME PP
###

toi_homePP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['PERIOD'] == '1st')]
toi_homePP = toi_homePP_df['TOI'].item()
#print(toi_homePP)

away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
  
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(85, 45, 'PP', color=colors[1], fontsize=12)
plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 1st Period Unblocked Shots\n' + str(toi_homePP) + ' Home PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_pp_home_1st.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 1st period unblocked shots during a home PP.')

###
### 2ND PERIOD
###

period = 2

###
### ALL
###

toi_all_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['PERIOD'] == '2nd')]
toi_all = toi_all_df['TOI'].item()
#print(all_toi)

away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])
home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])

away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
   
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 2nd Period Unblocked Shots\n' + str(toi_all) + ' Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_2nd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 2nd period unblocked shots.')
    
###
### 5v5
###

toi_5v5_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['PERIOD'] == '2nd')]
toi_5v5 = toi_5v5_df['TOI'].item()
#print(toi_5v5)

away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)].count()[1])
home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
 
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 2nd Period Unblocked Shots\n' + str(toi_5v5) + ' 5v5 Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_5v5_2nd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for 2nd period unblocked 5v5 shots.')
    
###
### AWAY PP
###

toi_awayPP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['PERIOD'] == '2nd')]
toi_awayPP = toi_awayPP_df['TOI'].item()
#print(toi_awayPP)

away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
   
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
plt.text(-95, 45, 'PP', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 2nd Period Unblocked Shots\n' + str(toi_awayPP) + ' Away PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_pp_away_2nd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 2nd period unblocked shots during an away PP.')
    
###
### HOME PP
###

toi_homePP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['PERIOD'] == '2nd')]
toi_homePP = toi_homePP_df['TOI'].item()
#print(toi_homePP)

away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
  
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(85, 45, 'PP', color=colors[1], fontsize=12)
plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 2nd Period Unblocked Shots\n' + str(toi_homePP) + ' Home PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_pp_home_2nd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 2nd period unblocked shots during a home PP.')

###
### 3RD PERIOD
###

period = 3

###
### ALL
###

toi_all_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['PERIOD'] == '3rd')]
toi_all = toi_all_df['TOI'].item()
#print(all_toi)

away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])
home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['PERIOD'] == period)].count()[1])

away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['PERIOD'] == period)]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
   
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 3rd Period Unblocked Shots\n' + str(toi_all) + ' Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_3rd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 3rd period unblocked shots.')
    
###
### 5v5
###

toi_5v5_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['PERIOD'] == '3rd')]
toi_5v5 = toi_5v5_df['TOI'].item()
#print(toi_5v5)

away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)].count()[1])
home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
 
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 3rd Period Unblocked Shots\n' + str(toi_5v5) + ' 5v5 Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_5v5_3rd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for 3rd period unblocked 5v5 shots.')
    
###
### AWAY PP
###

toi_awayPP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['PERIOD'] == '3rd')]
toi_awayPP = toi_awayPP_df['TOI'].item()
#print(toi_awayPP)

away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
   
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
plt.text(-95, 45, 'PP', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 3rd Period Unblocked Shots\n' + str(toi_awayPP) + ' Away PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_pp_away_3rd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 3rd period unblocked shots during an away PP.')
    
###
### HOME PP
###

toi_homePP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['PERIOD'] == '3rd')]
toi_homePP = toi_homePP_df['TOI'].item()
#print(toi_homePP)

away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)].count()[1])
    
away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
   
home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['PERIOD'] == period)]
    
### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))
    
### creates compact dataframes of x and y data from the 'home_df' and 'away_df' objects to generate plots with
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
try:
    away_scored_plot = away_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c='white', edgecolors=colors[0], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    away_saved_plot = away_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[0], linewidth='1', alpha=0.75, ax=ax);
except:
    pass
try:
    away_missed_plot = away_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[0], edgecolors='none', alpha=0.5, ax=ax);
except:
    pass
  
try:
    home_scored_plot = home_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[1], linewidth='2', alpha=1, ax=ax);
except:
    pass
try:
    home_saved_plot = home_df_saved.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='o', s=60, c='white', edgecolors=colors[1], linewidth='1', alpha=0.8, ax=ax);
except:
    pass
try:
    home_missed_plot = home_df_missed.plot.scatter(x='X_1', y='Y_1', zorder=2, marker='x', s=40, c=colors[1], edgecolors='none', alpha=0.8, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.jpeg' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(85, 45, 'PP', color=colors[1], fontsize=12)
plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-75, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' 3rd Period Unblocked Shots\n' + str(toi_homePP) + ' Home PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)

### helps eliminate whitespace
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

### renders the image from the data and image components
plt.savefig(charts_teams_period + 'shots_scatter_pp_home_3rd.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)

### displays message
print('Finished scatter plot for all 3rd period unblocked shots during a home PP.')