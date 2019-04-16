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

def parse_ids(season_id, game_id, images):

    ### pull common variables from the parameters file
    charts_teams = parameters.charts_teams
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    ### create variables that point to the .csv livefeed, play-by-play and time-on-ice files
    livefeed_file = files_root + 'livefeed.json'
    pbp_file = files_root + 'pbp.csv'
    toi_file = files_root + 'TOI_matrix.csv'
    
    ### opens the game's livefeed (JSON) file to create a few shared variables
    with open(livefeed_file) as livefeed_json:
        livefeed_data = json.load(livefeed_json)
        livefeed_parsed = livefeed_data
    
        try:
            game_status = livefeed_parsed["liveData"]["linescore"]["currentPeriodTimeRemaining"]
            currentperiod = livefeed_parsed["liveData"]["linescore"]["currentPeriod"]
    
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
    
    ### create a dataframe object that reads in the play-by-play file
    pbp_df = pd.read_csv(pbp_file)
    
    ### create a dataframe object that reads in the time on ice file; filter a copy for seconds of special teams play (for later generation of shaded bars)
    toi_df = pd.read_csv(toi_file)
    
    pp_toi = toi_df.copy()
    pp_toi_df = pp_toi[(pp_toi['HOME_STATE'] == 'PP') | (pp_toi['AWAY_STATE'] == 'PP')]
    home_pp = pp_toi_df[(pp_toi_df['HOME_STATE'] == 'PP')]
    away_pp = pp_toi_df[(pp_toi_df['AWAY_STATE'] == 'PP')]
    
    ### choose colors for each team and the legend; set them in a list
    away_color = '#e60000'
    home_color = '#206a92'
    legend_color = 'black'
    colors = [away_color, home_color, legend_color]
    
    ###
    ### ALL
    ###
    
    ### create a copy of the play-by-play dataframe; filter for shots; remove extraneous columns
    gameflow = pbp_df.copy()
    
    gameflow_df = gameflow[(gameflow['EVENT'] == 'Shot')]
    gameflow_df = gameflow_df.drop(columns=['HOME_SITUATION', 'AWAY_SITUATION', 'HOME_STRENGTH', 'AWAY_STRENGTH', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'X_1', 'Y_1', 'X_2', 'Y_2', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
    ### give instances of unblocked shots a value of 1; add a dataframe column with the cumulative number
    home_unblocked_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
    gameflow_df['HOME_UNBLOCKED_SHOTS'] = home_unblocked_shots.cumsum()
    
    away_unblocked_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
    gameflow_df['AWAY_UNBLOCKED_SHOTS'] = away_unblocked_shots.cumsum()
    
    ### for each instance of an unblocked shot, find the difference in unblocked shots for each team; add a dataframe column with the cumulative differential
    home_unblocked_shotsdiff = home_unblocked_shots - away_unblocked_shots
    gameflow_df['HOME_UNBLOCKED_SHOTSDIFF'] = home_unblocked_shotsdiff.cumsum()
    
    away_unblocked_shotsdiff = away_unblocked_shots - home_unblocked_shots
    gameflow_df['AWAY_UNBLOCKED_SHOTSDIFF'] = away_unblocked_shotsdiff.cumsum()
    
    ### give instances of any type of shot a value of 1; add a dataframe column with the cumulative number
    home_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
    gameflow_df['HOME_SHOTS'] = home_shots.cumsum()
    
    away_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
    gameflow_df['AWAY_SHOTS'] = away_shots.cumsum()
    
    ### for each instance of any type of shot, find the difference in shots for each team; add a dataframe column with the cumulative differential
    home_shotsdiff = home_shots - away_shots
    gameflow_df['HOME_SHOTSDIFF'] = home_shotsdiff.cumsum()
    
    away_shotsdiff = away_shots - home_shots
    gameflow_df['AWAY_SHOTSDIFF'] = away_shotsdiff.cumsum()
    
    ### copy the gameflow dataframe; filter for goals
    goals = gameflow_df.copy()
    
    goals_df = goals[(goals['EVENT_TYPE'] == 'Goal')]
    
    home_goals = goals_df[(goals_df['TEAM'] == home)]
    away_goals = goals_df[(goals_df['TEAM'] == away)]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### create a subset for each team, contingent on the home team's cumulative shot differential, of the amended gameflow dataframe
    try:
        home_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] >= 0)]
    except:
        pass
    try:
        away_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] <= 0)]
    except:
        pass
    
    ### plot each team's cumulative shot differential; make these lines transparent as they are only needed to create the y-axis scale
    try:
        home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, label='', ax=ax);
    except:
        pass
    try:
        away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, label='', ax=ax);
    except:
        pass
    
    
    ### plot stepped lines for each team's subset
    try:
        home_advantage_plot_step = plt.step(x=home_advantage['SECONDS_GONE'], y=home_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[1], label='');
    except:
        pass
    
    try:
        away_advantage_plot_step = plt.step(x=away_advantage['SECONDS_GONE'], y=away_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[0], label='');
    except:
        pass
    
    ### plot goal events in such a way that they will render exclusively as markers overlaying the stepped line plots 
    try:
        home_goals_plot = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
    except:
        pass
    
    try:
        away_goals_plot = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[0], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
    except:
        pass
    
    ### create a contingency for situations in which one team has yet to or, if the game is final, did not score
    if home_goals.empty == False:
        goals_label = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)
    elif home_goals.empty == True and away_goals.empty == False:
        goals_label = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)   
    
    
    ### set the break-even line
    if game_type == 'Regulation':
        breakeven_x, breakeven_y = [-0,3600],[0,0]
    elif game_type == 'Overtime':
        breakeven_x, breakeven_y = [-0,3900],[0,0]
    clear_breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = 'white', alpha=1)
    breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = colors[2], alpha=0.15)
    
    ### set vertical indicators for the end of each period
    ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=1, color=colors[2], linewidth=0, label='Power Play')
    ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    ax.axvspan(2400, 2401, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    ax.axvspan(3600, 3601, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    if game_type == 'Overtime':
        ax.axvspan(3900, 3901, ymin=0, ymax=1, alpha=0.15, color=colors[2])
        
    ### set vertical shaded areas indcating power play situations
    for second in home_pp['SECONDS_GONE']:
        ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[1])
        
    for second in away_pp['SECONDS_GONE']:
        ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[0])
    
    ### eliminate unnecessary whitespace on the first axes
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(True)
    
    ### adjust the visibility of the first axes spines
    ax.spines["top"].set_visible(False)   
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)  
    
    ### remove ticks belonging to the first axes
    ax.tick_params(axis='y', which="both", left=False, right=False, length=0)
    
    ### create a second axes that shares the same x-axis
    ax2 = ax.twinx()
    
    ### plot each team's cumulative shot differential; make these lines transparent as they are only needed to create the second y-axis scale
    home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, ax=ax2);
    away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, ax=ax2);
    
    ### eliminate unnecessary whitespace on the second axes
    ax2.axes.get_xaxis().set_visible(False)
    ax2.axes.get_yaxis().set_visible(True)
    
    ### adjust the visibility of the second axes spines
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
    
    ### invert the second y-axis
    ax2.invert_yaxis()
    
    ### set the team label
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
    
    ### set the period names as labels
    if game_type == 'Regulation':
        plt.text(0.33, -0.05, '1st', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
        plt.text(0.63, -0.05, '2nd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
        plt.text(0.93, -0.05, '3rd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    
    if game_type == 'Overtime':
        plt.text(0.31, -0.05, '1st', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
        plt.text(0.58, -0.05, '2nd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
        plt.text(0.86, -0.05, '3rd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
        plt.text(0.94, -0.05, 'OT', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    
    ### set the plot title
    plt.title(date + ' Shot Differential\n' + away + ' @ ' + home + '\n')
    
    ### set the location of the plot legend
    ax.legend(loc='center', bbox_to_anchor=(.5, 1.025), ncol=2).get_frame().set_linewidth(0.0)
    
    ### save the image to file
    plt.savefig(charts_teams + 'shots_gameflow.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished plotting the shot differential game flow for all situations.')
    
    
    ###
    ### 5v5
    ###
    
    ### create a copy of the play-by-play dataframe; filter for shots and game state; remove extraneous columns
    gameflow = pbp_df.copy()
    
    gameflow_df = gameflow[(gameflow['EVENT'] == 'Shot') & (gameflow['HOME_STRENGTH'] == '5v5')]
    gameflow_df = gameflow_df.drop(columns=['HOME_SITUATION', 'AWAY_SITUATION', 'HOME_STATE', 'AWAY_STATE', 'HOME_GOALS', 'AWAY_GOALS', 'HOME_SCOREDIFF', 'AWAY_SCOREDIFF', 'EVENT_DETAIL', 'HOME_ZONE', 'AWAY_ZONE', 'PLAYER_A', 'PLAYER_B', 'PLAYER_C', 'X_1', 'Y_1', 'X_2', 'Y_2', 'HOMEON_1', 'HOMEON_2', 'HOMEON_3', 'HOMEON_4', 'HOMEON_5', 'HOMEON_6', 'AWAYON_1', 'AWAYON_2', 'AWAYON_3', 'AWAYON_4', 'AWAYON_5', 'AWAYON_6'])
    
    ### give instances of unblocked shots a value of 1; add a dataframe column with the cumulative number
    home_unblocked_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
    gameflow_df['HOME_UNBLOCKED_SHOTS'] = home_unblocked_shots.cumsum()
    
    away_unblocked_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT_TYPE'] != 'Block'), int(1), 0))
    gameflow_df['AWAY_UNBLOCKED_SHOTS'] = away_unblocked_shots.cumsum()
    
    ### for each instance of an unblocked shot, find the difference in unblocked shots for each team; add a dataframe column with the cumulative differential
    home_unblocked_shotsdiff = home_unblocked_shots - away_unblocked_shots
    gameflow_df['HOME_UNBLOCKED_SHOTSDIFF'] = home_unblocked_shotsdiff.cumsum()
    
    away_unblocked_shotsdiff = away_unblocked_shots - home_unblocked_shots
    gameflow_df['AWAY_UNBLOCKED_SHOTSDIFF'] = away_unblocked_shotsdiff.cumsum()
    
    ### give instances of any type of shot a value of 1; add a dataframe column with the cumulative number
    home_shots = (np.where((gameflow_df['TEAM'] == home) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
    gameflow_df['HOME_SHOTS'] = home_shots.cumsum()
    
    away_shots = (np.where((gameflow_df['TEAM'] == away) & (gameflow_df['EVENT'] == 'Shot'), int(1), 0))
    gameflow_df['AWAY_SHOTS'] = away_shots.cumsum()
    
    ### for each instance of any type of shot, find the difference in shots for each team; add a dataframe column with the cumulative differential
    home_shotsdiff = home_shots - away_shots
    gameflow_df['HOME_SHOTSDIFF'] = home_shotsdiff.cumsum()
    
    away_shotsdiff = away_shots - home_shots
    gameflow_df['AWAY_SHOTSDIFF'] = away_shotsdiff.cumsum()
    
    ### copy the gameflow dataframe; filter for goals
    goals = gameflow_df.copy()
    
    goals_df = goals[(goals['EVENT_TYPE'] == 'Goal')]
    
    home_goals = goals_df[(goals_df['TEAM'] == home)]
    away_goals = goals_df[(goals_df['TEAM'] == away)]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### create a subset for each team, contingent on the home team's cumulative shot differential, of the amended gameflow dataframe
    try:
        home_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] >= 0)]
    except:
        pass
    try:
        away_advantage = gameflow_df[(gameflow_df['HOME_SHOTSDIFF'] <= 0)]
    except:
        pass
    
    ### plot each team's cumulative shot differential; make these lines transparent as they are only needed to create the y-axis scale
    try:
        home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, label='', ax=ax);
    except:
        pass
    try:
        away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, label='', ax=ax);
    except:
        pass
    
    ### plot stepped lines for each team's subset
    try:
        home_advantage_plot_step = plt.step(x=home_advantage['SECONDS_GONE'], y=home_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[1], label='');
    except:
        pass
    
    try:
        away_advantage_plot_step = plt.step(x=away_advantage['SECONDS_GONE'], y=away_advantage['HOME_SHOTSDIFF'], linewidth='1', alpha=1, color=colors[0], label='');
    except:
        pass
    
    ### plot goal events in such a way that they will render exclusively as markers overlaying the stepped line plots 
    try:
        home_goals_plot = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
    except:
        pass
    try:
        away_goals_plot = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[0], linewidth=0, alpha=1, legend=False, label='', marker=u'$\u2609$', markersize=12, ax=ax)
    except:
        pass
    
    ### create a contingency for situations in which one team has yet to or, if the game is final, did not score
    if home_goals.empty == False:
        goals_label = home_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)
    elif home_goals.empty == True and away_goals.empty == False:
        goals_label = away_goals.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', zorder=0, color=colors[2], linewidth=0, alpha=1, marker=u'$\u2609$', markersize=12, label='Goal', ax=ax)   
       
    ### set the break-even line
    breakeven_x, breakeven_y = [-0,3600],[0,0]
    clear_breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = 'white', alpha=1)
    breakeven = plt.plot(breakeven_x, breakeven_y, linewidth=1, color = colors[2], alpha=0.15)
    
    ### set vertical indicators for the end of each period
    ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=1, color=colors[2], linewidth=0, label='Power Play')
    ax.axvspan(1200, 1201, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    ax.axvspan(2400, 2401, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    ax.axvspan(3600, 3601, ymin=0, ymax=1, alpha=0.15, color=colors[2])
    
    ### set vertical shaded areas indcating power play and empty-net situations
    for second in home_pp['SECONDS_GONE']:
        ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[1])
        
    for second in away_pp['SECONDS_GONE']:
        ax.axvspan(second, second + 1, ymin=0, ymax=1, alpha=0.025, color=colors[0])
    
    ### eliminate unnecessary whitespace on the first axes
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(True)
    
    ### adjust the visibility of the first axes spines
    ax.spines["top"].set_visible(False)   
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)  
    
    ### remove ticks to the first axes
    ax.tick_params(axis='y', which="both", left=False, right=False, length=0)
    
    ### create a second axes that shares the same x-axis
    ax2 = ax.twinx()
    
    ### plot each team's cumulative shot differential; make these lines transparent as they are only needed to create the second y-axis scale
    try:
        home_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='HOME_SHOTSDIFF', color=colors[1], linewidth='2', alpha=0, legend=False, ax=ax2);
    except:
        pass
    try:
        away_shotdiff_plot = gameflow_df.plot(x='SECONDS_GONE', y='AWAY_SHOTSDIFF', color=colors[0], linewidth='2', alpha=0, legend=False, ax=ax2);
    except:
        pass
    
    ### eliminate unnecessary whitespace on the second axes
    ax2.axes.get_xaxis().set_visible(False)
    ax2.axes.get_yaxis().set_visible(True)
    
    ### adjust the visibility of the second axes spines
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
    
    ### invert the second y-axis
    ax2.invert_yaxis()
    
    ### set the team labels
    if max_home_shotdiff > max_away_shotdiff:
        plt.text(-660, min_away_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
        plt.text(4060, max_home_shotdiff, away, fontsize=12, color=colors[0], alpha=1)
    elif max_home_shotdiff < max_away_shotdiff:
        plt.text(-660, min_home_shotdiff, home, fontsize=12, color=colors[1], alpha=1)
        plt.text(4060, max_away_shotdiff, away, fontsize=12, color=colors[0], alpha=1)
    
    ### set the period names as labels
    plt.text(0.33, -0.05, '1st', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.63, -0.05, '2nd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    plt.text(0.93, -0.05, '3rd', fontsize=12, color=colors[2], alpha=1, transform=ax.transAxes)
    
    ### set the plot title
    plt.title(date + ' 5v5 Shot Differential\n' + away + ' @ ' + home + '\n')
    
    ### set the location of the plot legend
    ax.legend(loc='center', bbox_to_anchor=(.5, 1.025), ncol=2).get_frame().set_linewidth(0.0)
    
    ### save the image to file
    plt.savefig(charts_teams + 'shots_gameflow_5v5.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished plotting the 5v5 shot differential game flow.')