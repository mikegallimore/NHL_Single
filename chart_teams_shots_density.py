# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:41:23 2018

@author: @mikegallimore
"""
import pandas as pd
#import numpy as np
import parameters
import matplotlib.pyplot as plt
import seaborn as sns

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

### creates a variable that points to the .csv teams stats file
stats_teams_file = files_root + 'stats_teams.csv'

stats_teams_df = pd.read_csv(stats_teams_file)


### creates a variable that points to the .csv play-by-play file
pbp_file = files_root + 'pbp.csv'

### creates a dataframe object that reads in info from the .csv play-by-file file
pbp_df = pd.read_csv(pbp_file)
pbp_df['X_1'] *= -1
pbp_df['Y_1'] *= -1
pbp_df['X_2'] *= -1
pbp_df['Y_2'] *= -1

### makes copies of the pbp file in order to generate team-specific subsets
away_df = pbp_df.copy()
home_df = pbp_df.copy()

### sets the color options
away_color = '#e60000'
home_color = '#206a92'
legend_color = 'black'
colors = [away_color, home_color, legend_color]

###
### ALL
###

toi_all_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL')]
toi_all = toi_all_df['TOI'].item()

away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block')].count()[1])
home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block')].count()[1])

### establishes subsets of the overall dataframe for home and away events
away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block')]
away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal')]

home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block')]
home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal')]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))

### styles the plot
sns.set_style("white")
    
### handles the 2D density plots
away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)

### plot the goals for each team
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);

try:
    away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
except:
    pass
try:
    home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.png' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-70, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' Unblocked Shots\n' + str(toi_all) + ' Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
### Sets the plots axis limits
plt.xlim(-100,100)
plt.ylim(-42.5,42.5)
    
### helps eliminate whitespace
away_plot.axes.get_xaxis().set_visible(False)
away_plot.get_yaxis().set_visible(False)
    
### saves plot
plt.savefig(charts_teams + 'shots_density.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)
    
### Displays message
print('Finished density plot for all unblocked shots.')

###
### 5v5
###

toi_5v5_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5')]
toi_5v5 = toi_5v5_df['TOI'].item()

away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])

### establishes subsets of the overall dataframe for home and away events
away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))

### styles the plot
sns.set_style("white")
    
### handles the 2D density plots
try:
    away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
except:
    pass
try:
    home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
except:
    pass

### plot the goals for each team
try:
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
except:
    pass

try:
    away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
except:
    pass
try:
    home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.png' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-70, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' Unblocked Shots\n' + str(toi_5v5) + ' 5v5 Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
### Sets the plots axis limits
plt.xlim(-100,100)
plt.ylim(-42.5,42.5)
    
### helps eliminate whitespace
away_plot.axes.get_xaxis().set_visible(False)
away_plot.get_yaxis().set_visible(False)
    
### saves plot
plt.savefig(charts_teams + 'shots_density_5v5.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)
    
### Displays message
print('Finished density plot for all unblocked 5v5 shots.')

###
### Away PP
###

toi_awayPP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH')]
toi_awayPP = toi_awayPP_df['TOI'].item()

away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])

### establishes subsets of the overall dataframe for home and away events
away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')]
away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP')]

home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')]
home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP')]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))

### styles the plot
sns.set_style("white")
    
### handles the 2D density plots
try:
    away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
except:
    pass
try:
    home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
except:
    pass

### plot the goals for each team
try:
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
except:
    pass

try:
    away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
except:
    pass
try:
    home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.png' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-70, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' Unblocked Shots\n' + str(toi_awayPP) + ' Away PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
### Sets the plots axis limits
plt.xlim(-100,100)
plt.ylim(-42.5,42.5)
    
### helps eliminate whitespace
away_plot.axes.get_xaxis().set_visible(False)
away_plot.get_yaxis().set_visible(False)
    
### saves plot
plt.savefig(charts_teams + 'shots_density_pp_away.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)
    
### Displays message
print('Finished density plot for all unblocked shots during an away PP.')

###
### Home PP
###

toi_homePP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP')]
toi_homePP = toi_homePP_df['TOI'].item()

away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')].count()[1])
home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')].count()[1])

### establishes subsets of the overall dataframe for home and away events
away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')]
away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP')]

home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')]
home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP')]

### creates a figure to plot
fig, ax = plt.subplots(figsize=(8,6))

### styles the plot
sns.set_style("white")
    
### handles the 2D density plots
try:
    away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
except:
    pass
try:
    home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
except:
    pass

### plot the goals for each team
scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);

try:
    away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
except:
    pass
try:
    home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
except:
    pass

### sets the background image of what will be the plot to the 'rink_image.png' file
rink_img = plt.imread("rink_image.png")
plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)

### eliminates the axis labels
plt.axis('off')

### adds text boxes to indicate home and away sides
plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
plt.text(-4, 45, '@', color='black', fontsize=12)
plt.text(-70, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)

### sets the plot title
plt.title(date + ' Unblocked Shots\n' + str(toi_homePP) + ' Home PP Minutes\n')

### sets the location of the plot legend
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
### Sets the plots axis limits
plt.xlim(-100,100)
plt.ylim(-42.5,42.5)
    
### helps eliminate whitespace
away_plot.axes.get_xaxis().set_visible(False)
away_plot.get_yaxis().set_visible(False)
    
### saves plot
plt.savefig(charts_teams + 'shots_density_pp_home.png', bbox_inches='tight', pad_inches=0.2)

### show and then close the current figure
plt.show()
plt.close(fig)
    
### Displays message
print('Finished density plot for all unblocked shots during a home PP.')