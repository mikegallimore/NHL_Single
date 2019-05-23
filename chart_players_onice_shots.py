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
    charts_players = parameters.charts_players
    files_root = parameters.files_root

    ### generate date and team information
    schedule_csv = files_root + season_id + "_schedule.csv"

    schedule_df = pd.read_csv(schedule_csv)
    schedule_date = schedule_df[(schedule_df['GAME_ID'] == int(game_id))]
    
    date = schedule_date['DATE'].item()
    home = schedule_date['HOME'].item()
    away = schedule_date['AWAY'].item()
    teams = [away, home]

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
                axis='both',       # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                left=False,        # ticks along the left edge are off
                labelbottom=False) # labels along the bottom edge are off

        ax.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,        # ticks along the left edge are off
            labelbottom=True) # labels along the bottom edge are off

        ### create a list of x-axis tick values contingent on the max values for shots for and against 
        SF_max = team_df['SF']
        SF_max = SF_max.max()
        SA_max = team_df['SA']
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
        if x_tickmax > 25 and x_tickmax <= 30:
            x_ticklabels = [-30, -24, -18, -12, -6, 0, 6, 12, 18, 24, 30]
        if x_tickmax > 30 and x_tickmax <= 35:
            x_ticklabels = [-35, -28, -21, -14, -7, 0, 7, 14, 21, 28, 35]
        if x_tickmax > 35 and x_tickmax <= 40:
            x_ticklabels = [-40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40]
            
        ### use the newly-minted x-ticklabels to ensure the x-axis labels will always display as integers        
        ax.set_xticks(x_ticklabels, minor=False)
        
        ### remove the borders to each subplot
        ax.spines["top"].set_visible(False)   
        ax.spines["bottom"].set_visible(False)    
        ax.spines["right"].set_visible(False)    
        ax.spines["left"].set_visible(False)  
    
        ### insert a time on ice colorbar
        from matplotlib import ticker
        norm = mpl.colors.Normalize(vmin=0,vmax=1)
        sm = plt.cm.ScalarMappable(cmap=team_color_map, norm=norm)
        sm.set_array([])
        color_bar = plt.colorbar(sm, ax=ax)
        tick_locator = ticker.MaxNLocator(nbins=4)
        color_bar.locator = tick_locator
        color_bar.update_ticks()
        color_bar.ax.set_yticklabels(['0', '', '', '', max_toi])
        color_bar.set_label('Time On Ice', rotation=270)
    
        ### save the image to file
        if team == away:
            plt.savefig(charts_players + 'skaters_5v5_onice_shots_away.png', bbox_inches='tight', pad_inches=0.2)
        elif team == home:
            plt.savefig(charts_players + 'skaters_5v5_onice_shots_home.png', bbox_inches='tight', pad_inches=0.2)    
        
        ### show the current figure
        if images == 'show':
            plt.show()
        
        ### close the current figure   
        plt.close(fig)
        
        
        print('Plotting ' + team + ' skaters 5v5 on-ice shots.')   
        
        
    print('Finished plotting the 5v5 on-ice shots for players.')