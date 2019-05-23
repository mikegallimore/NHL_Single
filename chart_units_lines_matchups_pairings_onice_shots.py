# -*- coding: utf-8 -*-
"""
@author: @mikegallimore
"""

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

    ### create variables that point to the .csv processed stats file for lines
    lines_file = files_root + 'stats_units_lines_onice.csv'
    lines_matchups_pairings_file = files_root + 'stats_units_lines_onice_matchups_pairings.csv'
    
    ### create dataframe objects that read in info from the .csv files
    lines_df = pd.read_csv(lines_file)

    lines_matchups_pairings_df = pd.read_csv(lines_matchups_pairings_file)
 
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
        
        team_lines_list = team_lines_df.LINE.unique()

        ### create a lines dataframe; filter for team; make shots against negative values 
        team_lines_matchups_pairings_df = lines_matchups_pairings_df.copy()
        team_lines_matchups_pairings_df = team_lines_matchups_pairings_df[(team_lines_matchups_pairings_df['TEAM'] == team)]
        team_lines_matchups_pairings_df['SA'] *= -1

        ### create dataframes for specific lines; sort by time on ice; rank and then invert the rankings  
        team_line1_matchups_pairings_df = team_lines_matchups_pairings_df.copy()
        team_line1_matchups_pairings_df = team_line1_matchups_pairings_df[(team_line1_matchups_pairings_df['LINE'] == team_lines_list[3])]
        team_line1_matchups_pairings_df.sort_values(by=['TOI'], inplace=True)
        team_line1_matchups_pairings_df['RANK'] = team_line1_matchups_pairings_df['TOI'].rank(method='first')
        team_line1_matchups_pairings_df['RANK'] -= 1
        
        team_line2_matchups_pairings_df = team_lines_matchups_pairings_df.copy()
        team_line2_matchups_pairings_df = team_line2_matchups_pairings_df[(team_line2_matchups_pairings_df['LINE'] == team_lines_list[2])]
        team_line2_matchups_pairings_df.sort_values(by=['TOI'], inplace=True)
        team_line2_matchups_pairings_df['RANK'] = team_line2_matchups_pairings_df['TOI'].rank(method='first')
        team_line2_matchups_pairings_df['RANK'] -= 1

        team_line3_matchups_pairings_df = team_lines_matchups_pairings_df.copy()
        team_line3_matchups_pairings_df = team_line3_matchups_pairings_df[(team_line3_matchups_pairings_df['LINE'] == team_lines_list[1])]
        team_line3_matchups_pairings_df.sort_values(by=['TOI'], inplace=True)
        team_line3_matchups_pairings_df['RANK'] = team_line3_matchups_pairings_df['TOI'].rank(method='first')
        team_line3_matchups_pairings_df['RANK'] -= 1

        team_line4_matchups_pairings_df = team_lines_matchups_pairings_df.copy()
        team_line4_matchups_pairings_df = team_line4_matchups_pairings_df[(team_line4_matchups_pairings_df['LINE'] == team_lines_list[0])]
        team_line4_matchups_pairings_df.sort_values(by=['TOI'], inplace=True)
        team_line4_matchups_pairings_df['RANK'] = team_line4_matchups_pairings_df['TOI'].rank(method='first')
        team_line4_matchups_pairings_df['RANK'] -= 1

        ### create more lines dataframe with just the time on ice column; set a max value; scale each line's time on ice relative to the max  
        line1_matchups_pairings_toi = team_line1_matchups_pairings_df['TOI']
        max_line1_matchups_pairings_toi = max(line1_matchups_pairings_toi)    
        line1_matchups_pairings_toi_color = line1_matchups_pairings_toi / float(max(line1_matchups_pairings_toi))

        line2_matchups_pairings_toi = team_line2_matchups_pairings_df['TOI']
        max_line2_matchups_pairings_toi = max(line2_matchups_pairings_toi)    
        line2_matchups_pairings_toi_color = line2_matchups_pairings_toi / float(max(line2_matchups_pairings_toi))

        line3_matchups_pairings_toi = team_line3_matchups_pairings_df['TOI']
        max_line3_matchups_pairings_toi = max(line3_matchups_pairings_toi)    
        line3_matchups_pairings_toi_color = line3_matchups_pairings_toi / float(max(line3_matchups_pairings_toi))

        line4_matchups_pairings_toi = team_line4_matchups_pairings_df['TOI']
        max_line4_matchups_pairings_toi = max(line4_matchups_pairings_toi)    
        line4_matchups_pairings_toi_color = line4_matchups_pairings_toi / float(max(line4_matchups_pairings_toi))
    
        ### connect team and opponent color map colors to each line's scaled time on ice 
        line1_matchups_pairings_toi_color_map_for = team_color_map(line1_matchups_pairings_toi_color)
        line1_matchups_pairings_toi_color_map_against = opponent_color_map(line1_matchups_pairings_toi_color)

        line2_matchups_pairings_toi_color_map_for = team_color_map(line2_matchups_pairings_toi_color)
        line2_matchups_pairings_toi_color_map_against = opponent_color_map(line2_matchups_pairings_toi_color)

        line3_matchups_pairings_toi_color_map_for = team_color_map(line3_matchups_pairings_toi_color)
        line3_matchups_pairings_toi_color_map_against = opponent_color_map(line3_matchups_pairings_toi_color)

        line4_matchups_pairings_toi_color_map_for = team_color_map(line4_matchups_pairings_toi_color)
        line4_matchups_pairings_toi_color_map_against = opponent_color_map(line4_matchups_pairings_toi_color)

        ### create a figure with two subplots sharing the y-axis
        fig, axarr = plt.subplots(4, sharex=True)
              
        ### set the plot title; display a line as the title for each subplot
        axarr[0].set_title(date + ' Lines vs Pairings 5v5 On-Ice Shots\n' + away + ' @ ' + home + '\n\n' + team_lines_list[3], size=10, loc='center')
        axarr[1].set_title(team_lines_list[2], size=10, loc='center')
        axarr[2].set_title(team_lines_list[1], size=10, loc='center')
        axarr[3].set_title(team_lines_list[0], size=10, loc='center')
        
        ### create bars for shots for and against as well as line markers (to note the shot differential) for each line
        try:
            line1_SF_plot = team_line1_matchups_pairings_df.plot.barh(x='MATCHUP', y='SF', stacked=True, color=line1_matchups_pairings_toi_color_map_for, width=0.5, legend=None, label='', ax=axarr[0]);
        except:
            pass
        try:
            line1_SA_plot = team_line1_matchups_pairings_df.plot.barh(x='MATCHUP', y='SA', stacked=True, color=line1_matchups_pairings_toi_color_map_against, width=0.5, legend=None, label='', ax=axarr[0]);
        except:
            pass
        try:
            line1_SD_plot = team_line1_matchups_pairings_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=7, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=axarr[0]);
        except:
            pass

        try:
            line2_SF_plot = team_line2_matchups_pairings_df.plot.barh(x='MATCHUP', y='SF', stacked=True, color=line2_matchups_pairings_toi_color_map_for, width=0.5, legend=None, label='', ax=axarr[1]);
        except:
            pass
        try:
            line2_SA_plot = team_line2_matchups_pairings_df.plot.barh(x='MATCHUP', y='SA', stacked=True, color=line2_matchups_pairings_toi_color_map_against, width=0.5, legend=None, label='', ax=axarr[1]);
        except:
            pass
        try:
            line2_SD_plot = team_line2_matchups_pairings_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=7, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=axarr[1]);
        except:
            pass

        try:
            line3_SF_plot = team_line3_matchups_pairings_df.plot.barh(x='MATCHUP', y='SF', stacked=True, color=line3_matchups_pairings_toi_color_map_for, width=0.5, legend=None, label='', ax=axarr[2]);
        except:
            pass
        try:
            line3_SA_plot = team_line3_matchups_pairings_df.plot.barh(x='MATCHUP', y='SA', stacked=True, color=line3_matchups_pairings_toi_color_map_against, width=0.5, legend=None, label='', ax=axarr[2]);
        except:
            pass
        try:
            line3_SD_plot = team_line3_matchups_pairings_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=7, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=axarr[2]);
        except:
            pass

        try:
            line4_SF_plot = team_line4_matchups_pairings_df.plot.barh(x='MATCHUP', y='SF', stacked=True, color=line4_matchups_pairings_toi_color_map_for, width=0.5, legend=None, label='', ax=axarr[3]);
        except:
            pass
        try:
            line4_SA_plot = team_line4_matchups_pairings_df.plot.barh(x='MATCHUP', y='SA', stacked=True, color=line4_matchups_pairings_toi_color_map_against, width=0.5, legend=None, label='', ax=axarr[3]);
        except:
            pass
        try:
            line4_SD_plot = team_line4_matchups_pairings_df.plot(x='SD', y='RANK', marker='o', color='white', markersize=7, markeredgecolor='black', linewidth=0, alpha=1, legend=None, label='', ax=axarr[3]);
        except:
            pass

        fig.subplots_adjust(hspace=0.4)

        ### remove the labels for each subplot
        axarr[0].set_xlabel('')
        axarr[0].set_ylabel('')

        axarr[1].set_xlabel('')
        axarr[1].set_ylabel('')

        axarr[2].set_xlabel('')
        axarr[2].set_ylabel('')

        axarr[3].set_xlabel('')
        axarr[3].set_ylabel('')
    
        ### set vertical indicators for break-even shot differential
        axarr[0].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
        axarr[1].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
        axarr[2].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
        axarr[3].axvspan(0, 0, ymin=0, ymax=1, alpha=0.5, color='black')
    
        ### change the tick parameters
        axarr[0].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=False,
            labelsize=10)

        axarr[1].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=False,
            labelsize=10)

        axarr[2].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=False,
            labelsize=10)

        axarr[3].tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            left=False,
            labelbottom=True,
            labelsize=10)

        ### create a list of x-axis tick values contingent on the max values for shots for and against 
        SF_max = team_lines_matchups_pairings_df['SF']
        SF_max = SF_max.max()
        SA_max = team_lines_matchups_pairings_df['SA']
        SA_max *= -1
        SA_max = SA_max.max()

        if SF_max >= SA_max:
            x_tickmax = SF_max
        elif SF_max < SA_max:
            x_tickmax = SA_max

        if x_tickmax <= 5:
            x_ticklabels = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        if x_tickmax > 5 and x_tickmax <= 10:
            x_ticklabels = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
        if x_tickmax > 10 and x_tickmax <= 15:
            x_ticklabels = [-15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15]        
        if x_tickmax > 15 and x_tickmax <= 20:
            x_ticklabels = [-20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20]       
        if x_tickmax > 20 and x_tickmax <= 25:
            x_ticklabels = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
        
        ### use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        axarr[0].set_xticks(x_ticklabels, minor=False)
        axarr[1].set_xticks(x_ticklabels, minor=False)
        axarr[2].set_xticks(x_ticklabels, minor=False)         
        axarr[3].set_xticks(x_ticklabels, minor=False) 
    
        ### remove the borders to each subplot
        axarr[0].spines["top"].set_visible(False)   
        axarr[0].spines["bottom"].set_visible(False)    
        axarr[0].spines["right"].set_visible(False)    
        axarr[0].spines["left"].set_visible(False)

        axarr[1].spines["top"].set_visible(False)   
        axarr[1].spines["bottom"].set_visible(False)    
        axarr[1].spines["right"].set_visible(False)    
        axarr[1].spines["left"].set_visible(False)

        axarr[2].spines["top"].set_visible(False)   
        axarr[2].spines["bottom"].set_visible(False)    
        axarr[2].spines["right"].set_visible(False)    
        axarr[2].spines["left"].set_visible(False)

        axarr[3].spines["top"].set_visible(False)   
        axarr[3].spines["bottom"].set_visible(False)    
        axarr[3].spines["right"].set_visible(False)    
        axarr[3].spines["left"].set_visible(False)
    
        ### insert time on ice colorbars for each axis
        line1_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        line1_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=line1_norm)
        line1_sm.set_array([])
        line1_color_bar = plt.colorbar(line1_sm, ax=axarr[0])
        line1_color_bar.ax.set_yticklabels(['0', '', max_line1_matchups_pairings_toi], fontsize=10)
        line1_color_bar.set_label('TOI', rotation=270, fontsize=10)

        line2_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        line2_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=line2_norm)
        line2_sm.set_array([])
        line2_color_bar = plt.colorbar(line2_sm, ax=axarr[1])
        line2_color_bar.ax.set_yticklabels(['0', '', max_line2_matchups_pairings_toi], fontsize=10)
        line2_color_bar.set_label('TOI', rotation=270, fontsize=10)

        line3_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        line3_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=line3_norm)
        line3_sm.set_array([])
        line3_color_bar = plt.colorbar(line3_sm, ax=axarr[2])
        line3_color_bar.ax.set_yticklabels(['0', '', max_line3_matchups_pairings_toi], fontsize=10)
        line3_color_bar.set_label('TOI', rotation=270, fontsize=10)

        line4_norm = mpl.colors.Normalize(vmin=0,vmax=1)
        line4_sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=line4_norm)
        line4_sm.set_array([])
        line4_color_bar = plt.colorbar(line4_sm, ax=axarr[3])
        line4_color_bar.ax.set_yticklabels(['0', '', max_line4_matchups_pairings_toi], fontsize=10)
        line4_color_bar.set_label('TOI', rotation=270, fontsize=10)
   
        ### save the image to file
        if team == away:
            plt.savefig(charts_units + 'onice_shots_away_lines_matchups_pairings.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_units + 'onice_shots_home_lines_matchups_pairings.png', bbox_inches='tight', pad_inches=0.2)    
        
        ### show the current figure
        if images == 'show':
            plt.show()
        
        ### close the current figure   
        plt.close(fig)
        
        
        print('Plotting ' + team + ' lines vs pairings 5v5 on-ice shots.')   
        
        
    print('Finished plotting the 5v5 on-ice shots for lines vs pairings.')