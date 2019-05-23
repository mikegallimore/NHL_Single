# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import pandas as pd
import matplotlib.pyplot as plt
import parameters

def parse_ids(season_id, game_id, images):

    ### pull common variables from the parameters file
    charts_teams_situation = parameters.charts_teams_situation
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    ### create variables that point to the .csv processed teams stats file and play-by-play file
    stats_teams_file = files_root + 'stats_teams_situation.csv'
    pbp_file = files_root + 'pbp.csv'
    
    ### create a dataframe object that reads in the team stats info
    stats_teams_df = pd.read_csv(stats_teams_file)
    
    ### create a dataframe object that reads in the play-by-file info; invert the X and Y coordinates
    pbp_df = pd.read_csv(pbp_file)
    pbp_df['X_1'] *= -1
    pbp_df['Y_1'] *= -1
    pbp_df['X_2'] *= -1
    pbp_df['Y_2'] *= -1
    
    ### choose colors for each team and the legend; set them in a list
    away_color = '#e60000'
    home_color = '#206a92'
    legend_color = 'black'
    colors = [away_color, home_color, legend_color]
    
    ###
    ### HOME LEADING, AWAY TRAILING
    ###
    
    home_situation = 'Leading'
    away_situation = 'Trailing'
     
    ###
    ### ALL
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_all_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_all_home = toi_all_df_home['TOI'].item()
    except:
        toi_all_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file 
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_SITUATION'] == home_situation)]
      
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_SITUATION'] == home_situation)]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_all_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unnecessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots.')
    
    
    ###
    ### 5v5
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_5v5_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_5v5_home = toi_5v5_df_home['TOI'].item()
    except:
        toi_5v5_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file   
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team   
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_5v5_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' 5v5 Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unnecessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_5v5_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home + ' + home_situation.lower() + ' unblocked 5v5 shots.')
    
    
    ###
    ### AWAY PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_awayPP_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_awayPP_home = toi_awayPP_df_home['TOI'].item()
    except:
        toi_awayPP_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file  
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
        
    ### plot the distinct types of unblocked shot events for each team
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### adds text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
    plt.text(-95, 45, 'PP', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_awayPP_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' Away PP Minutes\n')
    
    ### sets the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unncessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_pp_away_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots during an away PP.')
       
    ###
    ### HOME PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_homePP_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_homePP_home = toi_homePP_df_home['TOI'].item()
    except:
        toi_homePP_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file   
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team    
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(85, 45, 'PP', color=colors[1], fontsize=12)
    plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_homePP_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' Home PP Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminates unncessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_pp_home_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots during a home PP.')
    
    
    ###
    ### TIED
    ###
     
    home_situation = 'Tied'
    away_situation = 'Tied'
     
    ###
    ### ALL
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_all_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_all_home = toi_all_df_home['TOI'].item()
    except:
        toi_all_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file 
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_SITUATION'] == home_situation)]
      
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_SITUATION'] == home_situation)]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_all_home) + ' Tied Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unnecessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for ' + home_situation.lower() + ' unblocked shots.')
    
    
    ###
    ### 5v5
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_5v5_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_5v5_home = toi_5v5_df_home['TOI'].item()
    except:
        toi_5v5_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file   
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team   
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_5v5_home) + ' Tied 5v5 Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unnecessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_5v5_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home + ' + home_situation.lower() + ' unblocked 5v5 shots.')
    
    
    ###
    ### AWAY PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_awayPP_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_awayPP_home = toi_awayPP_df_home['TOI'].item()
    except:
        toi_awayPP_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file  
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
        
    ### plot the distinct types of unblocked shot events for each team
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### adds text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
    plt.text(-95, 45, 'PP', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_awayPP_home) + ' Tied Away PP Minutes\n')
    
    ### sets the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unncessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_pp_away_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots during an away PP.')
       
    ###
    ### HOME PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_homePP_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_homePP_home = toi_homePP_df_home['TOI'].item()
    except:
        toi_homePP_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file   
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team    
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(85, 45, 'PP', color=colors[1], fontsize=12)
    plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_homePP_home) + ' Tied Home PP Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminates unncessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_pp_home_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots during a home PP.')
    
    
    ###
    ### HOME TRAILING, AWAY LEADING
    ###
     
    home_situation = 'Trailing'
    away_situation = 'Leading'
     
    ###
    ### ALL
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_all_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_all_home = toi_all_df_home['TOI'].item()
    except:
        toi_all_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file 
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_SITUATION'] == home_situation)]
      
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_SITUATION'] == home_situation)]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_all_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unnecessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots.')
    
    
    ###
    ### 5v5
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_5v5_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_5v5_home = toi_5v5_df_home['TOI'].item()
    except:
        toi_5v5_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file   
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team   
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_5v5_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_5v5_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' 5v5 Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unnecessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_5v5_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home + ' + home_situation.lower() + ' unblocked 5v5 shots.')
    
    
    ###
    ### AWAY PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_awayPP_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_awayPP_home = toi_awayPP_df_home['TOI'].item()
    except:
        toi_awayPP_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file  
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['AWAY_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
        
    ### plot the distinct types of unblocked shot events for each team
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### adds text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
    plt.text(-95, 45, 'PP', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_awayPP_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' Away PP Minutes\n')
    
    ### sets the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminate unncessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_pp_away_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots during an away PP.')
       
    ###
    ### HOME PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    try:
        toi_homePP_df_home = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP') & (stats_teams_df['SITUATION'] == home_situation)]
        toi_homePP_home = toi_homePP_df_home['TOI'].item()
    except:
        toi_homePP_home = 0.0
    
    ### get a count of the number of unblocked shots for each team
    away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file   
    away_df_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_saved = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    away_df_missed = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
       
    home_df_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_saved = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Save') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
    home_df_missed = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Miss') & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['HOME_SITUATION'] == home_situation)]
        
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
        
    ### create the markers that will be used for the legend (note the zorder)
    scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c='white', edgecolors=colors[2], linewidth='2', alpha=1, label='Scored', ax=ax);
    saved_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='o', s=60, c='white', edgecolors=colors[2], alpha=1, label='Saved', ax=ax);
    missed_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker='x', s=40, c=colors[2], edgecolors='none', alpha=1, label='Missed', ax=ax);
    
    ### plot the distinct types of unblocked shot events for each team    
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
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(85, 45, 'PP', color=colors[1], fontsize=12)
    plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-75, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_homePP_home) + ' Away ' + away_situation + ', Home ' + home_situation + ' Home PP Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
    
    ### eliminates unncessary whitespace
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    ### save the plot to file
    plt.savefig(charts_teams_situation + 'shots_scatter_pp_home_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
    
    print('Finished scatter plot for home ' + home_situation.lower() + ' unblocked shots during a home PP.')