# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""
import pandas as pd
import parameters
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as clr
import dict_team_colors
import mod_switch_colors

def parse_ids(season_id, game_id, images):

    # pull common variables from the parameters file
    charts_teams_situation = parameters.charts_teams_situation
    files_root = parameters.files_root

    # generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()

    # create variables that point to the .csv team stats file and play-by-play file
    stats_teams_file = files_root + 'stats_teams_situation.csv'
    pbp_file = files_root + 'pbp.csv'
    
    # create a dataframe object that reads in the team stats file
    stats_teams_df = pd.read_csv(stats_teams_file)
    
    # create a dataframe object that reads in the play-by-file info; invert the X and Y coordinates
    pbp_df = pd.read_csv(pbp_file)
    pbp_df = pbp_df[(pbp_df['PERIOD'] <= 4)]    
    
    pbp_df['X_1'] *= -1
    pbp_df['Y_1'] *= -1
    pbp_df['X_2'] *= -1
    pbp_df['Y_2'] *= -1
    
    # make copies of the pbp file for later generation of team-specific subsets
    away_df = pbp_df.copy()
    home_df = pbp_df.copy()
    
    # choose colors for each team; set them in a list; generate a custom colormap for each team
    legend_color = 'black'

    away_color = dict_team_colors.team_color_1st[away]
    home_color = dict_team_colors.team_color_1st[home]
    
    # change one team's color from its primary option to, depending on the opponent, either a second, third or fourth option
    try:
        away_color = mod_switch_colors.switch_team_colors(away, home)[0]
        home_color = mod_switch_colors.switch_team_colors(away, home)[1]
    except:
        pass
    
    colors = [away_color, home_color, legend_color]
    
    away_cmap = clr.LinearSegmentedColormap.from_list('custom away', [(0, '#ffffff'), (1, away_color)], N=256)  
    home_cmap = clr.LinearSegmentedColormap.from_list('custom home', [(0, '#ffffff'), (1, home_color)], N=256)

    situations = ['Leading', 'Tied', 'Trailing']

    for situation in situations:
        
        if situation == 'Leading':
            home_situation = 'Leading'
            away_situation = 'Trailing'
        if situation == 'Tied':
            home_situation = 'Tied'
            away_situation = 'Tied'
        if situation == 'Trailing':
            home_situation = 'Trailing'
            away_situation = 'Leading'
            
        states = ['ALL', '5v5', 'PP', 'SH']
        
        for state in states:
            
            # pull the time on ice recorded for the home team from the team stats file
            try:
                toi_df = stats_teams_df[(stats_teams_df['TEAM'] == home) & (stats_teams_df['STATE'] == state) & (stats_teams_df['SITUATION'] == home_situation)]
                toi = toi_df['TOI'].item()
            except:
                toi = 0.0
            
            # get a count of the number of unblocked shots for each team
            if state == 'ALL':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation)].count()[1])
            if state == '5v5':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')].count()[1])
            if state == 'PP':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')].count()[1])
            if state == 'SH':
                away_count = str(pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
                home_count = str(pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] != 'Block') & (pbp_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')].count()[1])
                
            # create subsets of the distinct types of unblocked shots for each team from the play-by-play file  
            if state == 'ALL':
                away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation)]
                away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
                away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation)]
            
                home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation)]
                home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
                home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation)]

            if state == '5v5':
                away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
                away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
            
                home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]
                home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
                home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STRENGTH'] == '5v5') & (pbp_df['AWAY_STRENGTH'] == '5v5')]

            if state == 'PP':
                away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
                away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
                away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
            
                home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]
                home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
                home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'PP') & (pbp_df['AWAY_STATE'] == 'SH')]

            if state == 'SH':
                away_shots = away_df[(away_df['TEAM'] == away) & (away_df['EVENT'] == 'Shot') & (away_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
                away_shots = away_shots.dropna(subset=['X_1', 'Y_1'])
                away_scored = pbp_df[(pbp_df['TEAM'] == away) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
            
                home_shots = home_df[(home_df['TEAM'] == home) & (home_df['EVENT'] == 'Shot') & (home_df['EVENT_TYPE'] != 'Block') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
                home_shots = home_shots.dropna(subset=['X_1', 'Y_1'])
                home_scored = pbp_df[(pbp_df['TEAM'] == home) & (pbp_df['EVENT'] == 'Shot') & (pbp_df['EVENT_TYPE'] == 'Goal') & (away_df['HOME_SITUATION'] == home_situation) & (pbp_df['HOME_STATE'] == 'SH') & (pbp_df['AWAY_STATE'] == 'PP')]
            
            # create a figure to plot
            fig, ax = plt.subplots(figsize=(8,6))
            
            # style the plot using seaborn
            sns.set_style("white")
                
            # make 2D density plots for each team with their unblocked shots
            try:
                away_plot = sns.kdeplot(away_shots.X_1, away_shots.Y_1, shade=True, bw=5, clip=((-88,0),(-42,42)), shade_lowest=False, alpha=0.5, cmap=away_cmap, ax=ax)
            except:
                pass
            try:
                home_plot = sns.kdeplot(home_shots.X_1, home_shots.Y_1, shade=True, bw=5, clip=((0,88),(-42,42)), shade_lowest=False, alpha=0.5, cmap=home_cmap, ax=ax)
            except:
                pass
                        
            # create the marker that will be used for the legend (note the zorder)
            teams_df_scored = pd.concat([away_scored, home_scored])

            try:
                scored_marker = teams_df_scored.plot.scatter(x='X_1', y='Y_1', zorder=0, marker=u'$\u2609$', s=120, c=colors[2], edgecolors=colors[2], linewidth='1', alpha=1, label='Scored', ax=ax);
            except:
                pass
            
            # plot the goals for each team
            try:
                away_scored_plot = away_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[0], linewidth='1', alpha=1, ax=ax);
            except:
                pass
            try:
                home_scored_plot = home_scored.plot.scatter(x='X_1', y='Y_1', zorder=3, marker=u'$\u2609$', s=100, c=colors[2], edgecolors=colors[1], linewidth='1', alpha=1, ax=ax);
            except:
                pass
            
            # set the background image of what will be the plot to the 'rink_image.png' file
            rink_img = plt.imread("rink_image.png")
            plt.imshow(rink_img, extent=[-100,100,-42.5,42.5], zorder=0)
            
            # eliminate the axis labels
            plt.axis('off')
            
            # add text boxes to indicate home and away sides
            plt.text(58, 45, home_count + ' USF', color=colors[1], fontsize=12, ha='center')
            plt.text(-58, 45, away_count + ' USF', color=colors[0], fontsize=12, ha='center')
            
            # add text boxes with team names in white and with the team's color in the background  
            fig.text(.435, 0.744, ' ' + away + ' ', fontsize='12', color='white', bbox=dict(facecolor=away_color, edgecolor='None'))
            fig.text(.535, 0.744, ' ' + home + ' ', fontsize='12', color='white', bbox=dict(facecolor=home_color, edgecolor='None'))
            fig.text(.500, 0.744, '@', fontsize='12', color='black', bbox=dict(facecolor='white', edgecolor='None'))
            
            # set the plot title
            if state == 'ALL' and situation != 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Away ' + away_situation + ', Home ' + home_situation + ' Minutes\n\n')
            elif state == 'ALL' and situation == 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Tied Minutes\n\n')

            if state == '5v5' and situation != 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Away ' + away_situation + ', Home ' + home_situation + ' 5v5 Minutes\n\n')
            elif state == '5v5' and situation == 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Tied 5v5 Minutes\n\n')

            if state == 'PP' and situation != 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Away ' + away_situation + ', Home ' + home_situation + ' Home PP Minutes\n\n')
            elif state == 'PP' and situation == 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Tied Home PP Minutes\n\n')

            if state == 'SH' and situation != 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Away ' + away_situation + ', Home ' + home_situation + ' Away PP Minutes\n\n')
            elif state == 'SH' and situation == 'Tied':
                plt.title(date + ' Unblocked Shots\n' + str(toi) + ' Tied Away PP Minutes\n\n')
                
            # set the location of the plot legend
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), scatterpoints=1, ncol=3).get_frame().set_linewidth(0.0)
                
            # set plot axis limits
            plt.xlim(-100,100)
            plt.ylim(-42.5,42.5)
                
            # eliminate unnecessary whitespace
            away_plot.axes.get_xaxis().set_visible(False)
            away_plot.get_yaxis().set_visible(False)
        
        
            ###    
            ### SAVE TO FILE
            ###

            if state == 'ALL':
                plt.savefig(charts_teams_situation + 'shots_density_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
            if state == '5v5':
                plt.savefig(charts_teams_situation + 'shots_density_5v5_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
            if state == 'PP':
                plt.savefig(charts_teams_situation + 'shots_density_pp_home_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
            if state == 'SH':
                plt.savefig(charts_teams_situation + 'shots_density_pp_away_' + home_situation.lower() + '.png', bbox_inches='tight', pad_inches=0.2)
                
            # exercise a command-line option to show the current figure
            if images == 'show':
                plt.show()
        
        
            ###
            ### CLOSE
            ###
            
            plt.close(fig)
            
            # status update
            if state == 'ALL':
                print('Finished density plot for home ' + home_situation.lower() + ' unblocked shots.')
            if state == '5v5':
                print('Finished density plot for home ' + home_situation.lower() + ' unblocked 5v5 shots.')
            if state == 'PP':
                print('Finished density plot for home ' + home_situation.lower() + ' unblocked shots during a home PP.')
            if state == 'SH':
                print('Finished density plot for home ' + home_situation.lower() + ' unblocked shots during an away PP.')