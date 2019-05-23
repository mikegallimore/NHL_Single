# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import pandas as pd
import parameters
import matplotlib.pyplot as plt
import seaborn as sns

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

    ### create variables that point to the .csv team stats file and play-by-play file
    stats_teams_file = files_root + 'stats_teams.csv'
    pbp_file = files_root + 'pbp.csv'
    
    ### create a dataframe object that reads in the team stats file
    stats_teams_df = pd.read_csv(stats_teams_file)
    
    ### create a dataframe object that reads in the play-by-file info; invert the X and Y coordinates
    pbp_df = pd.read_csv(pbp_file)
    pbp_df['X_1'] *= -1
    pbp_df['Y_1'] *= -1
    pbp_df['X_2'] *= -1
    pbp_df['Y_2'] *= -1
    
    ### make copies of the pbp file for later generation of team-specific subsets
    away_df = pbp_df.copy()
    home_df = pbp_df.copy()
    
    ### choose colors for each team and the legend; set them in a list
    away_color = '#e60000'
    home_color = '#206a92'
    legend_color = 'black'
    colors = [away_color, home_color, legend_color]
    
    ###
    ### ALL
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    toi_all_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'ALL')]
    toi_all = toi_all_df['TOI'].item()
    
    ### get a count of the number of unblocked shots for each team
    away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block')].count()[1])
    home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block')].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each teeam from the play-by-play file  
    away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block')]
    away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
    away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal')]
    
    home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block')]
    home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
    home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal')]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### style the plot using seaborn
    sns.set_style("white")
        
    ### make 2D density plots for each team with their unblocked shots
    away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
    home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
    
    ### create goal markers that will be used for the legend (note the zorder)
    try:
        scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
    except:
        pass
    
    ### plot the goals for each team
    try:
        away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
    except:
        pass
    try:
        home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
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
    plt.text(-70, 45, away + ' (' + away_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_all) + ' Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
        
    ### set plot axis limits
    plt.xlim(-100,100)
    plt.ylim(-42.5,42.5)
        
    ### eliminate unnecessary whitespace
    away_plot.axes.get_xaxis().set_visible(False)
    away_plot.get_yaxis().set_visible(False)
        
    ### save the plot to file
    plt.savefig(charts_teams + 'shots_density.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
        
    print('Finished density plot for all unblocked shots.')
    
    
    ###
    ### 5v5
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    toi_5v5_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == '5v5')]
    toi_5v5 = toi_5v5_df['TOI'].item()
    
    ### get a count of the number of unblocked shots for each team
    away_5v5_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
    home_5v5_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each team from the play-by-play file  
    away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
    away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
    away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
    
    home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
    home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
    home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### style the plot with seaborn
    sns.set_style("white")
        
    ### make 2D density plots for each team with their unblocked shots
    try:
        away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
    except:
        pass
    try:
        home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
    except:
        pass
    
    ### create goal markers that will be used for the legend (note the zorder)
    try:
        scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
    except:
        pass
    
    ### plot the goals for each team
    try:
        away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
    except:
        pass
    try:
        home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
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
    plt.text(-70, 45, away + ' (' + away_5v5_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_5v5) + ' 5v5 Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
        
    ### set plot axis limits
    plt.xlim(-100,100)
    plt.ylim(-42.5,42.5)
        
    ### eliminate unnecessary whitespace
    away_plot.axes.get_xaxis().set_visible(False)
    away_plot.get_yaxis().set_visible(False)
        
    ### save the plot to file
    plt.savefig(charts_teams + 'shots_density_5v5.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
        
    print('Finished density plot for all unblocked 5v5 shots.')
    
    
    ###
    ### Away PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    toi_awayPP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'SH')]
    toi_awayPP = toi_awayPP_df['TOI'].item()
    
    ### get a count of the number of unblocked shots for each team
    away_PP_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
    home_SH_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each team from the play-by-play file  
    away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')]
    away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
    away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP')]
    
    home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (pbp_df['AWAY_STATE'] == 'PP')]
    home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
    home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['AWAY_STATE'] == 'PP')]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### style the plot with seaborn
    sns.set_style("white")
        
    ### make 2D density plots for each team with their unblocked shots
    try:
        away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
    except:
        pass
    try:
        home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
    except:
        pass
    
    ### create goal markers that will be used for the legend (note the zorder)
    try:
        scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
    except:
        pass
    
    ### plot the goals for each team
    try:
        away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
    except:
        pass
    try:
        home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
    except:
        pass
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_SH_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-70, 45, away + ' (' + away_PP_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_awayPP) + ' Away PP Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
        
    ### set plot axis limits
    plt.xlim(-100,100)
    plt.ylim(-42.5,42.5)
        
    ### eliminate unncessary whitespace
    away_plot.axes.get_xaxis().set_visible(False)
    away_plot.get_yaxis().set_visible(False)
        
    ### saves the plot to file
    plt.savefig(charts_teams + 'shots_density_pp_away.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
    
        
    print('Finished density plot for all unblocked shots during an away PP.')
    
    
    ###
    ### Home PP
    ###
    
    ### pull the time on ice recorded for the home team from the team stats file
    toi_homePP_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == 'PP')]
    toi_homePP = toi_homePP_df['TOI'].item()
    
    ### get a count of the number of unblocked shots for each team
    away_SH_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')].count()[1])
    home_PP_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')].count()[1])
    
    ### create subsets of the distinct types of unblocked shots for each team from the play-by-play file  
    away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')]
    away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
    away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP')]
    
    home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_STATE'] == 'PP')]
    home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
    home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (pbp_df['HOME_STATE'] == 'PP')]
    
    ### create a figure to plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    ### style the plot with seaborn
    sns.set_style("white")
        
    ### make 2D density plots for each team with their unblocked shots
    try:
        away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Reds', ax=ax)
    except:
        pass
    try:
        home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap='Blues', ax=ax)
    except:
        pass
    
    ### create goal markers that will be used for the legend (note the zorder)
    try:
        scored_plot = pbp_df.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
    except:
        pass
    
    ### plot the goals for each team
    try:
        away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
    except:
        pass
    try:
        home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
    except:
        pass
    
    ### set the background image of what will be the plot to the 'rink_image.png' file
    rink_img = plt.imread("rink_image.png")
    plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
    
    ### eliminate the axis labels
    plt.axis('off')
    
    ### add text boxes to indicate home and away sides
    plt.text(45, 45, home + ' (' + home_PP_count + ')', color=colors[1], fontsize=12)
    plt.text(-4, 45, '@', color='black', fontsize=12)
    plt.text(-70, 45, away + ' (' + away_SH_count + ')', color=colors[0], fontsize=12)
    
    ### set the plot title
    plt.title(date + ' Unblocked Shots\n' + str(toi_homePP) + ' Home PP Minutes\n')
    
    ### set the location of the plot legend
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
        
    ### set plot axis limits
    plt.xlim(-100,100)
    plt.ylim(-42.5,42.5)
        
    ### eliminates unncessary whitespace
    away_plot.axes.get_xaxis().set_visible(False)
    away_plot.get_yaxis().set_visible(False)
        
    ### save the plot to file
    plt.savefig(charts_teams + 'shots_density_pp_home.png', bbox_inches='tight', pad_inches=0.2)
    
    ### show the current figure
    if images == 'show':
        plt.show()
    
    ### close the current figure   
    plt.close(fig)
       
     
    print('Finished density plot for all unblocked shots during a home PP.')